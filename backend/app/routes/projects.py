from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, Project, CareerGoal
from app.schemas.schemas import ProjectCreate, ProjectUpdate, ProjectOut, RecommendedProjectOut, AdoptProjectRequest
from app.services.project_recommendation import get_recommended_projects, adopt_project_to_profile

router = APIRouter(prefix="/projects", tags=["Projects & Recommendations"])

@router.get("", response_model=List[ProjectOut])
def get_user_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns all projects created by or adopted by the current student."""
    return db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.id.desc()).all()

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
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
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=ProjectOut)
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

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    db.delete(project)
    db.commit()
    return None

@router.get("/recommendations")
def get_recommendations(target_role: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns curated project ideas targeting the student's identified skill gaps and target career role.
    """
    role = target_role
    if not role:
        goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
        role = goal.target_role if goal else "Java Developer"

    return get_recommended_projects(db, current_user, role)

@router.post("/adopt", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def adopt_project(
    req: AdoptProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Adopts a recommended project idea into the student's personal project list.
    """
    return adopt_project_to_profile(
        db=db,
        user=current_user,
        title=req.title,
        description=req.description,
        technologies=req.technologies
    )
