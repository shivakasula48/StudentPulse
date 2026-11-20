from datetime import datetime
from app.database.session import SessionLocal, Base, engine
from app.database.seed_data import seed_database
from app.models.models import (
    User, StudentProfile, StudentSkill, Skill, Assessment,
    AssessmentAnswer, AssessmentQuestion, Project, Certification, CareerGoal, ActivityLog
)
from app.core.security import get_password_hash
from app.services.roadmap import generate_learning_roadmap
from app.services.skill_gap import analyze_skill_gap

def create_demo_student():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    try:
        existing = db.query(User).filter(User.email == "alex.mercer@byteforce.edu").first()
        if existing:
            print("Demo student already exists.")
            return

        print("Seeding demo student: Alex Mercer...")
        user = User(
            name="Alex Mercer",
            email="alex.mercer@byteforce.edu",
            password_hash=get_password_hash("Password123!"),
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.flush()

        # Profile
        profile = StudentProfile(
            user_id=user.id,
            college="National Institute of Technology",
            degree="B.Tech Computer Science & Engineering",
            semester="6th Semester",
            graduation_year=2026,
            career_interest="Java Developer"
        )
        db.add(profile)

        # Career Goal
        goal = CareerGoal(
            user_id=user.id,
            target_role="Java Developer",
            preferred_domain="FinTech & Cloud Enterprise",
            created_at=datetime.utcnow()
        )
        db.add(goal)

        # Add Skills (Both self-reported and verified)
        skill_map = {s.name: s.id for s in db.query(Skill).all()}
        
        sample_skills = [
            ("Java", "Advanced", 85.0),
            ("OOP", "Intermediate", 75.0),
            ("SQL", "Intermediate", 65.0),
            ("Spring Boot", "Beginner", None),
            ("Data Structures and Algorithms", "Intermediate", 70.0),
            ("Git and GitHub", "Intermediate", None),
            ("Problem Solving", "Intermediate", 80.0),
            ("Communication", "Advanced", None)
        ]

        for s_name, lvl, score in sample_skills:
            if s_name in skill_map:
                sk = StudentSkill(
                    user_id=user.id,
                    skill_id=skill_map[s_name],
                    self_reported_level=lvl,
                    assessment_score=score,
                    updated_at=datetime.utcnow()
                )
                db.add(sk)

        # Sample Project
        proj = Project(
            user_id=user.id,
            title="Campus Placement Management System",
            description="Full-stack portal for student recruitment, interview scheduling, and eligibility shortlisting using Spring Boot and PostgreSQL.",
            technologies="Java, Spring Boot, PostgreSQL, React, REST APIs",
            github_url="https://github.com/byteforce/placement-portal",
            live_url="https://placement-portal-demo.byteforce.edu",
            status="In Progress"
        )
        db.add(proj)

        # Sample Certification
        cert = Certification(
            user_id=user.id,
            title="Oracle Certified Professional: Java SE 17 Developer",
            issuing_organization="Oracle University",
            completion_date="August 2026",
            credential_url="https://catalog-education.oracle.com/"
        )
        db.add(cert)

        # Sample Assessment Record
        asm = Assessment(
            user_id=user.id,
            category="Programming Skills",
            total_questions=4,
            score=75.0,
            completed_at=datetime.utcnow()
        )
        db.add(asm)
        db.flush()

        # Activity Logs
        logs = [
            ActivityLog(user_id=user.id, activity_type="profile", description="Completed baseline student profile and academic details", created_at=datetime.utcnow()),
            ActivityLog(user_id=user.id, activity_type="skill", description="Cataloged technical skills in Java, OOP, SQL, and Spring Boot", created_at=datetime.utcnow()),
            ActivityLog(user_id=user.id, activity_type="assessment", description="Scored 75% on Programming Skills verified assessment", created_at=datetime.utcnow()),
            ActivityLog(user_id=user.id, activity_type="project", description="Created project 'Campus Placement Management System'", created_at=datetime.utcnow())
        ]
        for l in logs:
            db.add(l)

        db.commit()

        # Generate roadmap for demo student
        generate_learning_roadmap(db, user, "Java Developer")
        print("Demo student seeded successfully with complete capability profile and roadmap!")

    finally:
        db.close()

if __name__ == "__main__":
    create_demo_student()
