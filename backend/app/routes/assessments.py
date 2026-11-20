from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.models import (
    User, Skill, StudentSkill, Assessment, AssessmentQuestion,
    AssessmentAnswer, ActivityLog
)
from app.schemas.schemas import (
    AssessmentQuestionOut, AssessmentSubmitRequest, AssessmentOut, AssessmentResultDetail
)

router = APIRouter(prefix="/assessments", tags=["Skill Assessments"])

ASSESSMENT_CATEGORIES = [
    {
        "id": "Programming Skills",
        "title": "Programming Skills",
        "description": "Core language fundamentals, OOP paradigms, JVM architecture, and concurrency.",
        "icon": "Code",
        "total_questions": 4
    },
    {
        "id": "Data Structures and Algorithms",
        "title": "Data Structures & Algorithms",
        "description": "Binary trees, graphs, sorting, searching, time/space complexity.",
        "icon": "Binary",
        "total_questions": 3
    },
    {
        "id": "Database Management",
        "title": "Database Management",
        "description": "SQL joins, ACID transaction semantics, indexing, query optimization, and JDBC.",
        "icon": "Database",
        "total_questions": 3
    },
    {
        "id": "Web Development",
        "title": "Web Development",
        "description": "React lifecycle/hooks, REST architecture, HTTP methods, and Spring Boot APIs.",
        "icon": "Globe",
        "total_questions": 3
    },
    {
        "id": "Software Engineering",
        "title": "Software Engineering",
        "description": "Git branching/rebasing, CI/CD, design patterns, and agile methodologies.",
        "icon": "Cpu",
        "total_questions": 2
    },
    {
        "id": "Artificial Intelligence / Machine Learning",
        "title": "AI & Machine Learning",
        "description": "Supervised learning, regularization, evaluation metrics, and neural architectures.",
        "icon": "Brain",
        "total_questions": 2
    },
    {
        "id": "Communication Skills",
        "title": "Communication Skills",
        "description": "Technical presentation, active listening, code reviews, and stakeholder management.",
        "icon": "MessageSquare",
        "total_questions": 2
    },
    {
        "id": "Problem-Solving",
        "title": "Problem-Solving",
        "description": "Root-cause diagnostics, production debugging, and algorithmic reasoning.",
        "icon": "Lightbulb",
        "total_questions": 1
    }
]

@router.get("/categories")
def get_categories():
    """Returns available assessment categories."""
    return ASSESSMENT_CATEGORIES

@router.get("/questions", response_model=List[AssessmentQuestionOut])
def get_questions_by_category(category: str, db: Session = Depends(get_db)):
    """Returns questions for an assessment category (options without exposing correct answers)."""
    questions = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.category == category)
        .all()
    )
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No questions found for category: {category}"
        )
    return questions

@router.post("/submit", response_model=AssessmentOut)
def submit_assessment(
    submission: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates submitted answers, calculates score, updates verified assessment score for skills,
    and returns detailed results with explanations.
    """
    question_ids = [a.question_id for a in submission.answers]
    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.id.in_(question_ids)).all()
    question_map = {q.id: q for q in questions}

    if not questions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid questions submitted.")

    correct_count = 0
    total = len(submission.answers)
    answer_details: List[AssessmentResultDetail] = []
    
    # Skill-specific tracking for updating student skills
    skill_scores: Dict[str, Dict[str, int]] = {}

    for item in submission.answers:
        q = question_map.get(item.question_id)
        if not q:
            continue

        is_correct = (item.selected_answer.strip().upper() == q.correct_option.strip().upper())
        if is_correct:
            correct_count += 1

        # Track by skill
        if q.skill_name not in skill_scores:
            skill_scores[q.skill_name] = {"correct": 0, "total": 0}
        skill_scores[q.skill_name]["total"] += 1
        if is_correct:
            skill_scores[q.skill_name]["correct"] += 1

        answer_details.append(
            AssessmentResultDetail(
                question_id=q.id,
                question_text=q.question_text,
                selected_answer=item.selected_answer.strip().upper(),
                correct_option=q.correct_option,
                is_correct=is_correct,
                explanation=q.explanation,
                skill_name=q.skill_name
            )
        )

    score_pct = round((correct_count / total) * 100, 1) if total > 0 else 0.0

    # 1. Save Assessment record
    assessment = Assessment(
        user_id=current_user.id,
        category=submission.category,
        total_questions=total,
        score=score_pct,
        completed_at=datetime.utcnow()
    )
    db.add(assessment)
    db.flush()

    # 2. Save Assessment Answers
    for item in submission.answers:
        q = question_map.get(item.question_id)
        if q:
            is_correct = (item.selected_answer.strip().upper() == q.correct_option.strip().upper())
            db.add(
                AssessmentAnswer(
                    assessment_id=assessment.id,
                    question_id=q.id,
                    selected_answer=item.selected_answer.strip().upper(),
                    is_correct=is_correct
                )
            )

    # 3. Update verified assessment_score on student's skills
    for skill_name, stats in skill_scores.items():
        skill_pct = round((stats["correct"] / stats["total"]) * 100, 1)
        skill_record = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        if skill_record:
            student_skill = (
                db.query(StudentSkill)
                .filter(StudentSkill.user_id == current_user.id, StudentSkill.skill_id == skill_record.id)
                .first()
            )
            if not student_skill:
                # Add skill to student's profile as verified
                student_skill = StudentSkill(
                    user_id=current_user.id,
                    skill_id=skill_record.id,
                    self_reported_level="Intermediate",
                    assessment_score=skill_pct,
                    updated_at=datetime.utcnow()
                )
                db.add(student_skill)
            else:
                student_skill.assessment_score = skill_pct
                student_skill.updated_at = datetime.utcnow()

    # 4. Log activity
    log = ActivityLog(
        user_id=current_user.id,
        activity_type="assessment",
        description=f"Completed '{submission.category}' assessment: {score_pct:.0f}% ({correct_count}/{total} correct)",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return AssessmentOut(
        id=assessment.id,
        category=assessment.category,
        total_questions=assessment.total_questions,
        score=assessment.score,
        completed_at=assessment.completed_at,
        answers=answer_details
    )

@router.get("/results", response_model=List[AssessmentOut])
def get_assessment_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns student's historical assessments."""
    return (
        db.query(Assessment)
        .filter(Assessment.user_id == current_user.id)
        .order_by(Assessment.completed_at.desc())
        .all()
    )
