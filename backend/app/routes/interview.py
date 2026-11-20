from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import User, InterviewSession, InterviewResponse, CareerGoal
from app.schemas.schemas import (
    InterviewGenerateRequest, InterviewQuestionItem, InterviewEvaluateRequest, InterviewEvaluateResponse
)
from app.services.interview_service import get_interview_questions, evaluate_and_record_answer

router = APIRouter(prefix="/interview", tags=["Interview Preparation"])

INTERVIEW_CATEGORIES = [
    {"id": "Technical Interview", "name": "Technical Interview", "desc": "System architecture, full-stack concepts, protocols, design"},
    {"id": "Programming", "name": "Programming Fundamentals", "desc": "Core language syntax, memory management, concurrency"},
    {"id": "DSA", "name": "DSA & Algorithms", "desc": "Time/space complexity, arrays, trees, graphs, dynamic programming"},
    {"id": "Database", "name": "Database & SQL", "desc": "Indexing, normalization, ACID properties, query optimization"},
    {"id": "OOP", "name": "OOP Principles", "desc": "Polymorphism, abstraction, SOLID design principles, design patterns"},
    {"id": "Project Discussion", "name": "Project Deep-Dive", "desc": "Defending project architecture, bottlenecks, and design decisions"},
    {"id": "HR Interview", "name": "HR & Behavioral", "desc": "Situational questions, leadership, conflict resolution, STAR format"},
    {"id": "Communication Skills", "name": "Professional Communication", "desc": "Translating technical debt to stakeholders, code reviews"}
]

@router.get("/categories")
def get_categories():
    return INTERVIEW_CATEGORIES

@router.post("/generate", response_model=List[InterviewQuestionItem])
def generate_questions(
    req: InterviewGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates targeted interview questions based on role, category, and difficulty.
    """
    role = req.target_role
    if not role:
        goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()
        role = goal.target_role if goal else "Java Developer"

    questions = get_interview_questions(
        target_role=role,
        category=req.category,
        difficulty=req.difficulty or "Intermediate"
    )
    return questions

@router.post("/evaluate", response_model=InterviewEvaluateResponse)
def evaluate_answer(
    req: InterviewEvaluateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates the student's answer using AI or deterministic rubric, providing strengths,
    missing concepts, constructive feedback, and an exemplar model answer.
    """
    if not req.student_answer or len(req.student_answer.strip()) < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a more complete answer.")

    result = evaluate_and_record_answer(
        db=db,
        user=current_user,
        target_role=req.target_role,
        category=req.category,
        question=req.question,
        student_answer=req.student_answer
    )
    return result

@router.get("/history")
def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the student's past mock interview practice responses and scores.
    """
    sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == current_user.id)
        .order_by(InterviewSession.created_at.desc())
        .limit(10)
        .all()
    )
    results = []
    for s in sessions:
        for r in s.responses:
            results.append({
                "session_id": s.id,
                "target_role": s.target_role,
                "category": s.category,
                "question": r.question,
                "student_answer": r.student_answer,
                "score": r.score,
                "strengths": r.strengths,
                "missing_concepts": r.missing_concepts,
                "feedback": r.feedback,
                "model_answer": r.model_answer,
                "created_at": r.created_at
            })
    return results
