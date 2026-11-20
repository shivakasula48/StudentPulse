from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, LearningRoadmap, RoadmapTask, CareerGoal, ActivityLog
from app.schemas.schemas import LearningRoadmapOut, RoadmapTaskOut, RoadmapTaskUpdate
from app.services.roadmap import generate_learning_roadmap

router = APIRouter(prefix="/roadmap", tags=["Learning Roadmap"])

class GenerateRoadmapRequest(BaseModel):
    target_role: Optional[str] = None

@router.post("/generate", response_model=LearningRoadmapOut)
def generate_roadmap_endpoint(
    req: GenerateRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates a personalized, phased learning roadmap based on student's current skill gaps.
    """
    role = req.target_role
    if not role:
        # Check current goal
        goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
        if goal:
            role = goal.target_role
        else:
            role = "Java Developer"

    roadmap = generate_learning_roadmap(db, current_user, role)
    return roadmap

@router.get("", response_model=Optional[LearningRoadmapOut])
def get_current_roadmap(
    target_role: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches the active learning roadmap for the student.
    """
    query = db.query(LearningRoadmap).filter(LearningRoadmap.user_id == current_user.id)
    if target_role:
        query = query.filter(LearningRoadmap.target_role == target_role)
    roadmap = query.order_by(LearningRoadmap.created_at.desc()).first()
    return roadmap

@router.put("/tasks/{task_id}", response_model=RoadmapTaskOut)
def update_task(
    task_id: int,
    task_in: RoadmapTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the status or due date of a learning task (Pending, In Progress, Completed).
    """
    task = (
        db.query(RoadmapTask)
        .join(LearningRoadmap, RoadmapTask.roadmap_id == LearningRoadmap.id)
        .filter(RoadmapTask.id == task_id, LearningRoadmap.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap task not found.")

    old_status = task.status
    if task_in.status is not None:
        task.status = task_in.status
    if task_in.due_date is not None:
        task.due_date = task_in.due_date

    if task_in.status == "Completed" and old_status != "Completed":
        log = ActivityLog(
            user_id=current_user.id,
            activity_type="roadmap",
            description=f"Completed roadmap task: '{task.title}'",
            created_at=datetime.utcnow()
        )
        db.add(log)

    db.commit()
    db.refresh(task)
    return task
