import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database.session import Base, get_db
from app.database.seed_data import seed_database
from app.services.ai_service import ai_service

# Use file-based SQLite database in tmp or memory for test suite
TEST_DATABASE_URL = "sqlite:///./test_studentpulse.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_database(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_studentpulse.db"):
        os.remove("./test_studentpulse.db")

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def student_auth_token(client):
    """Registers test student once for the test session."""
    user_data = {
        "name": "Alex Mercer",
        "email": "alex.mercer@byteforce.edu",
        "password": "Password123!",
        "college": "National Institute of Technology",
        "degree": "B.Tech Computer Science",
        "semester": "6th Semester",
        "career_interest": "Java Developer"
    }
    res = client.post("/api/auth/register", json=user_data)
    if res.status_code == 201:
        token = res.json()["access_token"]
    else:
        login_res = client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
        token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def second_student_token(client):
    """Registers second student for isolation tests."""
    user_data = {
        "name": "Samantha Ray",
        "email": "samantha.ray@byteforce.edu",
        "password": "Password123!",
        "college": "Tech University",
        "degree": "B.Tech Information Technology",
        "semester": "4th Semester",
        "career_interest": "Python Developer"
    }
    res = client.post("/api/auth/register", json=user_data)
    if res.status_code == 201:
        token = res.json()["access_token"]
    else:
        login_res = client.post("/api/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
        token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- SCENARIO 1: Student Registration and Login ---
def test_scenario_01_student_registration_and_login(client):
    new_user = {
        "name": "David Miller",
        "email": "david.miller@byteforce.edu",
        "password": "Password123!",
        "college": "IIT Delhi",
        "degree": "B.Tech Electrical",
        "semester": "5th Semester",
        "career_interest": "Full Stack Developer"
    }
    reg_res = client.post("/api/auth/register", json=new_user)
    assert reg_res.status_code == 201
    assert "access_token" in reg_res.json()

    login_res = client.post("/api/auth/login", json={
        "email": "david.miller@byteforce.edu",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    assert login_res.json()["user"]["email"] == "david.miller@byteforce.edu"

# --- SCENARIO 2: Profile Creation and Editing ---
def test_scenario_02_profile_creation_and_editing(client, student_auth_token):
    res = client.get("/api/profile", headers=student_auth_token)
    assert res.status_code == 200
    data = res.json()
    assert data["basic_info"]["college"] == "National Institute of Technology"
    assert data["target_role"] == "Java Developer"

    update_data = {
        "name": "Alex Mercer Updated",
        "college": "National Institute of Technology (NIT)",
        "semester": "7th Semester",
        "graduation_year": 2026
    }
    update_res = client.put("/api/profile", json=update_data, headers=student_auth_token)
    assert update_res.status_code == 200

    res2 = client.get("/api/auth/me", headers=student_auth_token)
    assert res2.status_code == 200
    assert res2.json()["name"] == "Alex Mercer Updated"
    assert res2.json()["semester"] == "7th Semester"
    assert res2.json()["graduation_year"] == 2026

# --- SCENARIO 3: Add and Update Technical Skills ---
def test_scenario_03_add_and_update_technical_skills(client, student_auth_token):
    res = client.post("/api/skills/my-skills", json={"skill_name": "Java", "self_reported_level": "Intermediate"}, headers=student_auth_token)
    assert res.status_code == 201
    skill_id = res.json()["id"]

    res_oop = client.post("/api/skills/my-skills", json={"skill_name": "OOP", "self_reported_level": "Beginner"}, headers=student_auth_token)
    assert res_oop.status_code == 201

    res_update = client.put(f"/api/skills/my-skills/{skill_id}", json={"self_reported_level": "Advanced"}, headers=student_auth_token)
    assert res_update.status_code == 200
    assert res_update.json()["self_reported_level"] == "Advanced"

    my_skills_res = client.get("/api/skills/my-skills", headers=student_auth_token)
    assert my_skills_res.status_code == 200
    names = [s["skill"]["name"] for s in my_skills_res.json()]
    assert "Java" in names
    assert "OOP" in names

# --- SCENARIO 4 & 5: Submit Skill Assessment & Calculate Score ---
def test_scenario_04_05_submit_assessment_and_calculate_score(client, student_auth_token):
    q_res = client.get("/api/assessments/questions?category=Programming Skills")
    assert q_res.status_code == 200
    questions = q_res.json()
    assert len(questions) > 0

    submission_answers = []
    for q in questions:
        if q["skill_name"] == "Java":
            submission_answers.append({"question_id": q["id"], "selected_answer": "A"})
        elif q["skill_name"] == "OOP":
            submission_answers.append({"question_id": q["id"], "selected_answer": "B"})
        else:
            submission_answers.append({"question_id": q["id"], "selected_answer": "B"})

    submit_res = client.post("/api/assessments/submit", json={
        "category": "Programming Skills",
        "answers": submission_answers
    }, headers=student_auth_token)

    assert submit_res.status_code == 200
    result = submit_res.json()
    assert result["category"] == "Programming Skills"
    assert result["total_questions"] == len(submission_answers)
    assert result["score"] > 0.0
    assert len(result["answers"]) == len(submission_answers)

    skills_res = client.get("/api/skills/my-skills", headers=student_auth_token)
    assert skills_res.status_code == 200
    java_skill = next((s for s in skills_res.json() if s["skill"]["name"] == "Java"), None)
    assert java_skill is not None
    assert java_skill["assessment_score"] is not None

# --- SCENARIO 6 & 7: Select Java Developer & Identify Missing Skills ---
def test_scenario_06_07_select_java_developer_and_identify_missing_skills(client, student_auth_token):
    goal_res = client.post("/api/profile/career-goals", json={"target_role": "Java Developer"}, headers=student_auth_token)
    assert goal_res.status_code == 200

    gap_res = client.post("/api/analysis/skill-gap", json={"target_role": "Java Developer"}, headers=student_auth_token)
    assert gap_res.status_code == 200
    gap_data = gap_res.json()

    assert gap_data["target_role"] == "Java Developer"
    assert gap_data["total_required_skills"] > 0
    assert "match_percentage" in gap_data
    
    missing_names = [s["skill_name"] for s in gap_data["missing_skills"]]
    assert "Spring Boot" in missing_names
    assert "SQL" in missing_names or "JDBC" in missing_names
    assert len(gap_data["ai_summary"]) > 20

# --- SCENARIO 8: Generate Personalized Learning Roadmap ---
def test_scenario_08_generate_personalized_roadmap(client, student_auth_token):
    res = client.post("/api/roadmap/generate", json={"target_role": "Java Developer"}, headers=student_auth_token)
    assert res.status_code == 200
    roadmap = res.json()
    assert roadmap["target_role"] == "Java Developer"
    assert len(roadmap["tasks"]) >= 4

    phases = {t["phase"] for t in roadmap["tasks"]}
    assert "Phase 1: Foundations" in phases

# --- SCENARIO 9: Recommend Projects Based on Skill Gaps ---
def test_scenario_09_recommend_projects_based_on_gaps(client, student_auth_token):
    res = client.get("/api/projects/recommendations?target_role=Java Developer", headers=student_auth_token)
    assert res.status_code == 200
    projects = res.json()
    assert len(projects) >= 1
    p = projects[0]
    assert "title" in p
    assert "problem_statement" in p
    assert "technologies" in p
    assert "skills_developed" in p
    assert "implementation_steps" in p

    adopt_res = client.post("/api/projects/adopt", json={
        "title": p["title"],
        "description": p["description"],
        "technologies": ", ".join(p["technologies"])
    }, headers=student_auth_token)
    assert adopt_res.status_code == 201
    assert adopt_res.json()["title"] == p["title"]

# --- SCENARIO 10: Generate Interview Questions ---
def test_scenario_10_generate_interview_questions(client, student_auth_token):
    res = client.post("/api/interview/generate", json={
        "target_role": "Java Developer",
        "category": "OOP",
        "difficulty": "Intermediate"
    }, headers=student_auth_token)
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) > 0
    assert "question" in questions[0]
    assert "hint" in questions[0]

# --- SCENARIO 11: Evaluate Student Answers ---
def test_scenario_11_evaluate_student_answers(client, student_auth_token):
    eval_payload = {
        "target_role": "Java Developer",
        "category": "OOP",
        "question": "Explain method overloading vs method overriding in Java.",
        "student_answer": "Overloading is compile-time polymorphism where methods in the same class have the same name but different argument lists. Overriding is runtime polymorphism where a subclass provides a specific implementation of a superclass method using @Override."
    }
    res = client.post("/api/interview/evaluate", json=eval_payload, headers=student_auth_token)
    assert res.status_code == 200
    eval_data = res.json()
    assert eval_data["rating"] >= 50.0
    assert len(eval_data["strengths"]) > 5
    assert len(eval_data["model_answer"]) > 10

# --- SCENARIO 12: Update Roadmap Task Status ---
def test_scenario_12_update_roadmap_task_status(client, student_auth_token):
    roadmap_res = client.get("/api/roadmap", headers=student_auth_token)
    assert roadmap_res.status_code == 200
    tasks = roadmap_res.json()["tasks"]
    task_id = tasks[0]["id"]

    update_res = client.put(f"/api/roadmap/tasks/{task_id}", json={"status": "Completed"}, headers=student_auth_token)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "Completed"

# --- SCENARIO 13: Update Dashboard Metrics with Real Calculated Data ---
def test_scenario_13_update_dashboard_metrics(client, student_auth_token):
    res = client.get("/api/dashboard/summary", headers=student_auth_token)
    assert res.status_code == 200
    data = res.json()
    assert data["user_name"] == "Alex Mercer Updated"
    assert data["readiness_score"] > 0.0
    assert data["total_skills_count"] >= 2
    assert data["completed_assessments_count"] >= 1
    assert data["roadmap_progress_pct"] > 0.0
    assert "category_proficiency" in data
    assert len(data["recent_activities"]) > 0

# --- SCENARIO 14 & 15: Gemini API Unavailable & Fallback Engine ---
def test_scenario_14_15_gemini_unavailable_and_fallback_engine(client, student_auth_token):
    orig_client = ai_service.client
    ai_service.client = None

    try:
        gap_res = client.post("/api/analysis/skill-gap", json={"target_role": "Java Developer"}, headers=student_auth_token)
        assert gap_res.status_code == 200
        data = gap_res.json()
        assert data["ai_is_fallback"] is True
        assert "Career Readiness Assessment for Java Developer" in data["ai_summary"]

        int_res = client.post("/api/interview/evaluate", json={
            "target_role": "Java Developer",
            "category": "OOP",
            "question": "What is polymorphism?",
            "student_answer": "Polymorphism enables an object to take many forms."
        }, headers=student_auth_token)
        assert int_res.status_code == 200
        assert int_res.json()["is_ai_generated"] is False
        assert int_res.json()["rating"] > 0
    finally:
        ai_service.client = orig_client

# --- SCENARIO 16: Cross-User Isolation (User cannot access another student's private records) ---
def test_scenario_16_cross_user_isolation(client, student_auth_token, second_student_token):
    proj_res = client.post("/api/profile/projects", json={
        "title": "Private Project of Alex",
        "description": "Sensitive student project data",
        "technologies": "Java, Spring"
    }, headers=student_auth_token)
    assert proj_res.status_code == 201
    alex_project_id = proj_res.json()["id"]

    hack_attempt = client.put(f"/api/profile/projects/{alex_project_id}", json={
        "title": "Hacked Title"
    }, headers=second_student_token)
    assert hack_attempt.status_code == 404

    delete_attempt = client.delete(f"/api/profile/projects/{alex_project_id}", headers=second_student_token)
    assert delete_attempt.status_code == 404

    s2_projects = client.get("/api/projects", headers=second_student_token)
    assert s2_projects.status_code == 200
    s2_ids = [p["id"] for p in s2_projects.json()]
    assert alex_project_id not in s2_ids
