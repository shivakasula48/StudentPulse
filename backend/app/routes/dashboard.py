from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import (
    User, StudentProfile, StudentSkill, Skill, Assessment, Project,
    CareerGoal, LearningRoadmap, RoadmapTask, InterviewSession, ActivityLog,
    RoleSkillRequirement
)
from app.schemas.schemas import DashboardSummaryOut, ActivityLogOut

router = APIRouter(prefix="/dashboard", tags=["Career Readiness Dashboard"])

@router.get("/summary", response_model=DashboardSummaryOut)
def get_dashboard_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Calculates genuine career readiness metrics strictly from saved database records.
    """
    # 1. Profile Completion Calculation
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    profile_fields = [
        profile.college if profile else None,
        profile.degree if profile else None,
        profile.semester if profile else None,
        profile.graduation_year if profile else None,
        profile.career_interest if profile else None
    ]
    filled_fields = sum(1 for f in profile_fields if f is not None and str(f).strip() != "")
    profile_pct = round((filled_fields / len(profile_fields)) * 100, 1)

    # 2. Career Goal
    career_goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
    target_role = career_goal.target_role if career_goal else (profile.career_interest if profile and profile.career_interest else "Java Developer")

    # 3. Skills Analysis
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    total_skills_count = len(skills)
    verified_skills_count = sum(1 for s in skills if s.assessment_score is not None)

    # 4. Compare with target role requirements
    reqs = (
        db.query(RoleSkillRequirement)
        .join(Skill, RoleSkillRequirement.skill_id == Skill.id)
        .filter(RoleSkillRequirement.role_name == target_role)
        .all()
    )
    user_skill_names = {s.skill.name.lower() for s in skills}
    user_skill_map = {s.skill.name.lower(): s for s in skills}

    strong_count = 0
    needs_improvement_count = 0
    missing_count = 0

    if reqs:
        for r in reqs:
            s_name = r.skill.name.lower()
            if s_name not in user_skill_names:
                missing_count += 1
            else:
                sk = user_skill_map[s_name]
                if sk.assessment_score is not None and sk.assessment_score < 60:
                    needs_improvement_count += 1
                elif sk.self_reported_level.lower() == "beginner" and r.required_level.lower() in ["intermediate", "advanced"]:
                    needs_improvement_count += 1
                else:
                    strong_count += 1
    else:
        strong_count = verified_skills_count
        needs_improvement_count = max(0, total_skills_count - verified_skills_count)
        missing_count = 0

    # 5. Assessment Metrics
    assessments = db.query(Assessment).filter(Assessment.user_id == current_user.id).all()
    completed_assessments_count = len(assessments)
    avg_assessment_score = (
        round(sum(a.score for a in assessments) / completed_assessments_count, 1)
        if completed_assessments_count > 0 else 0.0
    )

    # 6. Roadmap Metrics
    roadmaps = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == current_user.id).all()
    roadmap_tasks = []
    for r in roadmaps:
        roadmap_tasks.extend(r.tasks)
    
    total_tasks = len(roadmap_tasks)
    completed_tasks = sum(1 for t in roadmap_tasks if t.status == "Completed")
    roadmap_progress_pct = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0.0

    # 7. Projects Metrics
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    active_projects = sum(1 for p in projects if p.status in ["In Progress", "Planned"])
    completed_projects = sum(1 for p in projects if p.status == "Completed")

    # 8. Holistic Career Readiness Score (Formula derived strictly from evidence)
    # Weights:
    # - Profile Completeness: 10%
    # - Skill Alignment for Target Role: 35%
    # - Assessment Performance: 25%
    # - Learning Roadmap Progress: 15%
    # - Project Practical Portfolio: 15%
    role_alignment_ratio = (
        (strong_count * 1.0 + needs_improvement_count * 0.5) / len(reqs)
        if reqs and len(reqs) > 0 else (0.5 if total_skills_count > 0 else 0.0)
    )
    project_factor = min(1.0, (len(projects) * 0.4 + completed_projects * 0.6))

    readiness_calc = (
        (profile_pct / 100.0) * 10.0 +
        role_alignment_ratio * 35.0 +
        (avg_assessment_score / 100.0) * 25.0 +
        (roadmap_progress_pct / 100.0) * 15.0 +
        project_factor * 15.0
    )
    readiness_score = round(max(0.0, min(100.0, readiness_calc)), 1)

    # 9. Dynamic Recommended Next Action
    if total_skills_count == 0:
        next_action = {
            "title": "Add Your Current Skills",
            "description": "Catalog your existing programming languages, frameworks, and tools to unlock your skill gap analysis.",
            "link": "/skills",
            "action_text": "Add Skills"
        }
    elif completed_assessments_count == 0:
        next_action = {
            "title": "Verify Your Skills via Assessment",
            "description": "Take your first skill assessment to validate your self-reported skills with verifiable scores.",
            "link": "/assessments",
            "action_text": "Take Assessment"
        }
    elif total_tasks == 0:
        next_action = {
            "title": "Generate Your Personalized Roadmap",
            "description": f"Create a step-by-step learning roadmap tailored to your skill gaps for {target_role}.",
            "link": "/roadmap",
            "action_text": "Generate Roadmap"
        }
    elif len(projects) == 0:
        next_action = {
            "title": "Build a Portfolio Project",
            "description": "Demonstrate your abilities by adopting an industry-aligned project recommendation.",
            "link": "/projects",
            "action_text": "Explore Projects"
        }
    else:
        next_action = {
            "title": "Practice Mock Technical Interviews",
            "description": f"Prepare for technical interviews for {target_role} with AI-assisted rubric evaluation.",
            "link": "/interview",
            "action_text": "Practice Interview"
        }

    # 10. Category Proficiency (for Recharts Radar Chart)
    categories = ["Programming", "Web Development", "Database", "Framework", "AI/ML", "Professional Skills"]
    category_proficiency = []
    
    for cat in categories:
        cat_skills = [s for s in skills if s.skill.category.lower() == cat.lower()]
        if not cat_skills:
            score = 20.0  # baseline placeholder if no skills
        else:
            scores = []
            for s in cat_skills:
                if s.assessment_score is not None:
                    scores.append(s.assessment_score)
                else:
                    lvl = s.self_reported_level.lower()
                    scores.append(50.0 if lvl == "beginner" else (75.0 if lvl == "intermediate" else 90.0))
            score = round(sum(scores) / len(scores), 1)

        category_proficiency.append({
            "category": cat,
            "score": score,
            "full_mark": 100
        })

    # 11. Recent Activities
    recent_activities = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == current_user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(8)
        .all()
    )

    return DashboardSummaryOut(
        user_name=current_user.name,
        profile_completion_pct=profile_pct,
        target_role=target_role,
        readiness_score=readiness_score,
        total_skills_count=total_skills_count,
        verified_skills_count=verified_skills_count,
        skill_gap_summary={
            "strong": strong_count,
            "needs_improvement": needs_improvement_count,
            "missing": missing_count
        },
        roadmap_progress_pct=roadmap_progress_pct,
        active_projects_count=active_projects,
        completed_projects_count=completed_projects,
        completed_assessments_count=completed_assessments_count,
        average_assessment_score=avg_assessment_score,
        recommended_next_action=next_action,
        category_proficiency=category_proficiency,
        recent_activities=recent_activities
    )
