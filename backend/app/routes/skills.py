from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, Skill, StudentSkill, ActivityLog
from app.schemas.schemas import SkillOut, StudentSkillCreate, StudentSkillUpdate, StudentSkillOut

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("", response_model=List[SkillOut])
def get_all_skills(db: Session = Depends(get_db)):
    """Returns the full master catalog of skills."""
    return db.query(Skill).order_by(Skill.category, Skill.name).all()

@router.get("/my-skills", response_model=List[StudentSkillOut])
def get_my_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns all skills currently attached to the authenticated student."""
    return (
        db.query(StudentSkill)
        .filter(StudentSkill.user_id == current_user.id)
        .join(Skill, StudentSkill.skill_id == Skill.id)
        .order_by(Skill.category, Skill.name)
        .all()
    )

@router.post("/my-skills", response_model=StudentSkillOut, status_code=status.HTTP_201_CREATED)
def add_or_update_my_skill(skill_in: StudentSkillCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Adds a skill to the student's profile or updates self-reported level."""
    # Find skill by name or create if new
    skill = db.query(Skill).filter(Skill.name.ilike(skill_in.skill_name.strip())).first()
    if not skill:
        skill = Skill(name=skill_in.skill_name.strip(), category="Technical")
        db.add(skill)
        db.flush()

    # Check if student already has this skill
    student_skill = (
        db.query(StudentSkill)
        .filter(StudentSkill.user_id == current_user.id, StudentSkill.skill_id == skill.id)
        .first()
    )

    if student_skill:
        student_skill.self_reported_level = skill_in.self_reported_level
        student_skill.updated_at = datetime.utcnow()
    else:
        student_skill = StudentSkill(
            user_id=current_user.id,
            skill_id=skill.id,
            self_reported_level=skill_in.self_reported_level,
            updated_at=datetime.utcnow()
        )
        db.add(student_skill)

    log = ActivityLog(
        user_id=current_user.id,
        activity_type="skill",
        description=f"Added/updated skill '{skill.name}' at {skill_in.self_reported_level} level",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(student_skill)
    return student_skill

@router.put("/my-skills/{student_skill_id}", response_model=StudentSkillOut)
def update_my_skill_level(student_skill_id: int, skill_in: StudentSkillUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student_skill = (
        db.query(StudentSkill)
        .filter(StudentSkill.id == student_skill_id, StudentSkill.user_id == current_user.id)
        .first()
    )
    if not student_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student skill not found.")

    student_skill.self_reported_level = skill_in.self_reported_level
    student_skill.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(student_skill)
    return student_skill

@router.delete("/my-skills/{student_skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_skill(student_skill_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student_skill = (
        db.query(StudentSkill)
        .filter(StudentSkill.id == student_skill_id, StudentSkill.user_id == current_user.id)
        .first()
    )
    if not student_skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student skill not found.")

    db.delete(student_skill)
    db.commit()
    return None
