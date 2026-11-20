from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import (
    User, StudentProfile, StudentSkill, Project, Certification, CareerGoal, Assessment, ActivityLog
)
from app.schemas.schemas import (
    StudentProfileUpdate, ProjectCreate, ProjectUpdate, ProjectOut,
    CertificationCreate, CertificationUpdate, CertificationOut,
    CareerGoalCreate, CareerGoalOut
)

router = APIRouter(prefix="/profile", tags=["Student Profile"])

@router.get("")
def get_unified_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the unified student capability profile containing:
    - Basic Information
    - Technical & Professional Skills
    - Projects
    - Certifications
    - Career Goals
    - Assessment History
    """
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    certifications = db.query(Certification).filter(Certification.user_id == current_user.id).all()
    career_goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
    assessments = db.query(Assessment).filter(Assessment.user_id == current_user.id).order_by(Assessment.completed_at.desc()).all()

    # Formatted skills
    formatted_skills = []
    for s in skills:
        formatted_skills.append({
            "id": s.id,
            "skill_id": s.skill.id,
            "name": s.skill.name,
            "category": s.skill.category,
            "self_reported_level": s.self_reported_level,
            "assessment_score": s.assessment_score,
            "is_verified": s.assessment_score is not None
        })

    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "created_at": current_user.created_at
        },
        "basic_info": {
            "college": profile.college if profile else None,
            "degree": profile.degree if profile else None,
            "semester": profile.semester if profile else None,
            "graduation_year": profile.graduation_year if profile else None,
            "career_interest": profile.career_interest if profile else None
        },
        "target_role": career_goal.target_role if career_goal else (profile.career_interest if profile else None),
        "skills": formatted_skills,
        "projects": projects,
        "certifications": certifications,
        "assessments": assessments
    }

@router.put("")
def update_profile(profile_in: StudentProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    if profile_in.name:
        current_user.name = profile_in.name
    if profile_in.college is not None:
        profile.college = profile_in.college
    if profile_in.degree is not None:
        profile.degree = profile_in.degree
    if profile_in.semester is not None:
        profile.semester = profile_in.semester
    if profile_in.graduation_year is not None:
        profile.graduation_year = profile_in.graduation_year
    if profile_in.career_interest is not None:
        profile.career_interest = profile_in.career_interest

    log = ActivityLog(
        user_id=current_user.id,
        activity_type="profile",
        description="Updated student profile information",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return {"message": "Profile updated successfully"}

# --- Project Endpoints ---
@router.post("/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(
        user_id=current_user.id,
        title=project_in.title,
        description=project_in.description,
        technologies=project_in.technologies,
        github_url=project_in.github_url,
        live_url=project_in.live_url,
        status=project_in.status or "In Progress"
    )
    db.add(project)
    
    log = ActivityLog(
        user_id=current_user.id,
        activity_type="project",
        description=f"Added project '{project_in.title}'",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(project)
    return project

@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, project_in: ProjectUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

    if project_in.title is not None:
        project.title = project_in.title
    if project_in.description is not None:
        project.description = project_in.description
    if project_in.technologies is not None:
        project.technologies = project_in.technologies
    if project_in.github_url is not None:
        project.github_url = project_in.github_url
    if project_in.live_url is not None:
        project.live_url = project_in.live_url
    if project_in.status is not None:
        project.status = project_in.status

    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    db.delete(project)
    db.commit()
    return None

# --- Certification Endpoints ---
@router.post("/certifications", response_model=CertificationOut, status_code=status.HTTP_201_CREATED)
def create_certification(cert_in: CertificationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cert = Certification(
        user_id=current_user.id,
        title=cert_in.title,
        issuing_organization=cert_in.issuing_organization,
        completion_date=cert_in.completion_date,
        credential_url=cert_in.credential_url
    )
    db.add(cert)
    
    log = ActivityLog(
        user_id=current_user.id,
        activity_type="certification",
        description=f"Added certification '{cert_in.title}' from {cert_in.issuing_organization}",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(cert)
    return cert

@router.delete("/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(cert_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.id == cert_id, Certification.user_id == current_user.id).first()
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found.")
    db.delete(cert)
    db.commit()
    return None

# --- Career Goals Endpoints ---
@router.post("/career-goals", response_model=CareerGoalOut)
def set_career_goal(goal_in: CareerGoalCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).first()
    if not goal:
        goal = CareerGoal(
            user_id=current_user.id,
            target_role=goal_in.target_role,
            preferred_domain=goal_in.preferred_domain,
            created_at=datetime.utcnow()
        )
        db.add(goal)
    else:
        goal.target_role = goal_in.target_role
        if goal_in.preferred_domain is not None:
            goal.preferred_domain = goal_in.preferred_domain

    log = ActivityLog(
        user_id=current_user.id,
        activity_type="career_goal",
        description=f"Updated target career role to '{goal_in.target_role}'",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(goal)
    return goal
