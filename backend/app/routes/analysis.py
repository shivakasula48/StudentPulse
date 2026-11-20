from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, Skill, RoleSkillRequirement, SkillGapAnalysis
from app.schemas.schemas import SkillGapResponse
from app.services.skill_gap import analyze_skill_gap

router = APIRouter(prefix="/analysis", tags=["Skill Gap Analysis"])

class SkillGapRequest(BaseModel):
    target_role: str

@router.get("/roles")
def get_available_roles(db: Session = Depends(get_db)):
    """Returns available target roles with their skill requirements."""
    roles = (
        db.query(RoleSkillRequirement.role_name)
        .distinct()
        .all()
    )
    role_names = [r[0] for r in roles]

    detailed_roles = []
    for r_name in role_names:
        reqs = (
            db.query(RoleSkillRequirement)
            .join(Skill, RoleSkillRequirement.skill_id == Skill.id)
            .filter(RoleSkillRequirement.role_name == r_name)
            .all()
        )
        detailed_roles.append({
            "role_name": r_name,
            "required_skills_count": len(reqs),
            "skills": [
                {
                    "name": req.skill.name,
                    "category": req.skill.category,
                    "required_level": req.required_level,
                    "priority": req.priority
                }
                for req in reqs
            ]
        })
    return detailed_roles

@router.post("/skill-gap", response_model=SkillGapResponse)
def run_skill_gap_analysis(
    req: SkillGapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Computes a deterministic skill gap analysis for the given target role,
    compares student skills and assessment scores, and calls AI for explanation.
    """
    if not req.target_role or not req.target_role.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target role is required.")

    return analyze_skill_gap(db, current_user, req.target_role.strip())

@router.get("/skill-gap/history")
def get_skill_gap_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns past skill gap analysis reports."""
    records = (
        db.query(SkillGapAnalysis)
        .filter(SkillGapAnalysis.user_id == current_user.id)
        .order_by(SkillGapAnalysis.created_at.desc())
        .limit(10)
        .all()
    )
    return [
        {
            "id": r.id,
            "created_at": r.created_at,
            "analysis": r.analysis_json
        }
        for r in records
    ]
