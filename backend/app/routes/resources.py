from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, LearningResource, RoleSkillRequirement, StudentSkill, Skill, CareerGoal
from app.schemas.schemas import LearningResourceOut

router = APIRouter(prefix="/resources", tags=["Learning Resources"])

@router.get("", response_model=List[LearningResourceOut])
def get_all_resources(
    skill_category: Optional[str] = None,
    resource_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Returns curated learning resources with optional filtering."""
    query = db.query(LearningResource)
    if skill_category:
        query = query.filter(LearningResource.skill_category.ilike(f"%{skill_category}%"))
    if resource_type:
        query = query.filter(LearningResource.resource_type.ilike(f"%{resource_type}%"))
    return query.order_by(LearningResource.title).all()

@router.get("/recommended", response_model=List[LearningResourceOut])
def get_recommended_resources(
    target_role: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns learning resources specifically targeting the student's identified skill gaps.
    """
    role = target_role
    if not role:
        goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
        role = goal.target_role if goal else "Java Developer"

    # Identify missing or weak skills for this role
    reqs = (
        db.query(RoleSkillRequirement)
        .join(Skill, RoleSkillRequirement.skill_id == Skill.id)
        .filter(RoleSkillRequirement.role_name == role)
        .all()
    )
    user_skills = {s.skill.name.lower() for s in db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()}

    gap_names = [r.skill.name for r in reqs if r.skill.name.lower() not in user_skills]
    if not gap_names:
        gap_names = [r.skill.name for r in reqs]

    # Find resources matching any gap skill name
    recommended = []
    all_resources = db.query(LearningResource).all()
    for res in all_resources:
        for gap in gap_names:
            if gap.lower() in res.skill_category.lower() or gap.lower() in res.title.lower():
                recommended.append(res)
                break

    if not recommended:
        recommended = all_resources[:6]

    return recommended
