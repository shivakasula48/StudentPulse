from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import (
    User, Skill, StudentSkill, RoleSkillRequirement,
    SkillGapAnalysis, CareerGoal, ActivityLog
)
from app.schemas.schemas import SkillGapItem, SkillGapResponse
from app.services.ai_service import ai_service

LEVEL_VALUES = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

def analyze_skill_gap(db: Session, user: User, target_role: str) -> SkillGapResponse:
    """
    Performs deterministic, evidence-based skill gap analysis for a given user and target role.
    """
    # 1. Fetch requirements for the target role
    requirements = (
        db.query(RoleSkillRequirement)
        .join(Skill, RoleSkillRequirement.skill_id == Skill.id)
        .filter(RoleSkillRequirement.role_name == target_role)
        .all()
    )

    if not requirements:
        # Fallback to general requirements if custom role not found
        requirements = (
            db.query(RoleSkillRequirement)
            .join(Skill, RoleSkillRequirement.skill_id == Skill.id)
            .filter(RoleSkillRequirement.role_name == "Software Engineer")
            .all()
        )

    # 2. Fetch student's existing skills
    student_skills = (
        db.query(StudentSkill)
        .join(Skill, StudentSkill.skill_id == Skill.id)
        .filter(StudentSkill.user_id == user.id)
        .all()
    )
    user_skill_map = {
        ss.skill.name.lower(): ss
        for ss in student_skills
    }

    strong_skills: List[SkillGapItem] = []
    needs_improvement_skills: List[SkillGapItem] = []
    missing_skills: List[SkillGapItem] = []

    for req in requirements:
        skill_name = req.skill.name
        skill_category = req.skill.category
        req_level = req.required_level
        req_level_val = LEVEL_VALUES.get(req_level.lower(), 2)
        priority = req.priority

        student_skill = user_skill_map.get(skill_name.lower())

        if not student_skill:
            missing_skills.append(
                SkillGapItem(
                    skill_name=skill_name,
                    category=skill_category,
                    required_level=req_level,
                    current_level=None,
                    assessment_score=None,
                    priority=priority,
                    status="Missing",
                    gap_reason=f"Skill not yet in profile. {target_role} requires {req_level} proficiency."
                )
            )
        else:
            curr_level = student_skill.self_reported_level
            curr_level_val = LEVEL_VALUES.get(curr_level.lower(), 1)
            score = student_skill.assessment_score

            if curr_level_val >= req_level_val:
                # Check if verified assessment revealed weak score (< 60)
                if score is not None and score < 60.0:
                    needs_improvement_skills.append(
                        SkillGapItem(
                            skill_name=skill_name,
                            category=skill_category,
                            required_level=req_level,
                            current_level=curr_level,
                            assessment_score=score,
                            priority=priority,
                            status="Needs Improvement",
                            gap_reason=f"Self-reported {curr_level}, but verified assessment score is {score:.0f}%, indicating concept gaps."
                        )
                    )
                else:
                    strong_skills.append(
                        SkillGapItem(
                            skill_name=skill_name,
                            category=skill_category,
                            required_level=req_level,
                            current_level=curr_level,
                            assessment_score=score,
                            priority=priority,
                            status="Strong",
                            gap_reason=f"Meets or exceeds required {req_level} level for this role."
                        )
                    )
            else:
                needs_improvement_skills.append(
                    SkillGapItem(
                        skill_name=skill_name,
                        category=skill_category,
                        required_level=req_level,
                        current_level=curr_level,
                        assessment_score=score,
                        priority=priority,
                        status="Needs Improvement",
                        gap_reason=f"Current level ({curr_level}) is below target requirement ({req_level})."
                    )
                )

    total_reqs = len(requirements)
    if total_reqs > 0:
        match_percentage = round(
            ((len(strong_skills) * 1.0 + len(needs_improvement_skills) * 0.5) / total_reqs) * 100, 1
        )
    else:
        match_percentage = 0.0

    # AI or Rule-Based Explanation
    ai_summary, is_fallback = ai_service.explain_skill_gap(
        target_role=target_role,
        student_name=user.name,
        match_percentage=match_percentage,
        strong_skills=[s.skill_name for s in strong_skills],
        needs_improvement=[s.skill_name for s in needs_improvement_skills],
        missing_skills=[s.skill_name for s in missing_skills]
    )

    now = datetime.utcnow()

    # Save Career Goal if not set or update
    career_goal = db.query(CareerGoal).filter(CareerGoal.user_id == user.id).first()
    if not career_goal:
        career_goal = CareerGoal(user_id=user.id, target_role=target_role)
        db.add(career_goal)
        db.flush()
    else:
        career_goal.target_role = target_role
        db.flush()

    # Store analysis record
    analysis_record = SkillGapAnalysis(
        user_id=user.id,
        career_goal_id=career_goal.id,
        analysis_json={
            "target_role": target_role,
            "match_percentage": match_percentage,
            "total_required_skills": total_reqs,
            "strong_count": len(strong_skills),
            "needs_improvement_count": len(needs_improvement_skills),
            "missing_count": len(missing_skills),
            "ai_summary": ai_summary,
            "is_fallback": is_fallback
        },
        created_at=now
    )
    db.add(analysis_record)

    # Log activity
    log = ActivityLog(
        user_id=user.id,
        activity_type="skill_gap",
        description=f"Generated skill gap analysis for {target_role} ({match_percentage:.0f}% match)",
        created_at=now
    )
    db.add(log)
    db.commit()

    return SkillGapResponse(
        target_role=target_role,
        match_percentage=match_percentage,
        total_required_skills=total_reqs,
        strong_skills=strong_skills,
        needs_improvement_skills=needs_improvement_skills,
        missing_skills=missing_skills,
        ai_summary=ai_summary,
        ai_is_fallback=is_fallback,
        created_at=now
    )
