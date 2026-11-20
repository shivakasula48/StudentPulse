from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import (
    User, InterviewSession, InterviewResponse, ActivityLog
)
from app.services.ai_service import ai_service

CURATED_INTERVIEW_QUESTIONS = {
    "Java Developer": {
        "OOP": [
            {
                "id": "q-java-oop-1",
                "question": "Explain the difference between method overloading and method overriding in Java. When is each resolved by the compiler or JVM?",
                "category": "OOP",
                "difficulty": "Intermediate",
                "hint": "Think about compile-time vs run-time polymorphism and method signatures.",
                "sample_answer_outline": "Overloading occurs in the same class with same name but different parameter list, resolved at compile-time (static binding). Overriding occurs in a subclass providing specific logic for an inherited method, resolved at runtime via dynamic method dispatch."
            },
            {
                "id": "q-java-oop-2",
                "question": "What is an abstract class versus an interface in Java 8+? In what scenario would you prefer an abstract class over an interface?",
                "category": "OOP",
                "difficulty": "Intermediate",
                "hint": "Consider state (instance variables), constructor requirements, and default methods.",
                "sample_answer_outline": "Interfaces define contracts and support multiple inheritance of type; since Java 8 they support default and static methods. Abstract classes can declare instance state (fields), constructors, and package-private visibility, preferred when related classes share common state."
            }
        ],
        "Database": [
            {
                "id": "q-java-db-1",
                "question": "What is the N+1 select problem in ORM frameworks like Hibernate/JPA, and how do you resolve it?",
                "category": "Database",
                "difficulty": "Intermediate",
                "hint": "Consider lazy loading of child collections and JOIN FETCH or @EntityGraph.",
                "sample_answer_outline": "N+1 occurs when fetching a parent collection of N entities triggers N additional queries to load each child collection. Resolved using JOIN FETCH in JPQL, @EntityGraph, or batch fetching."
            }
        ],
        "Programming": [
            {
                "id": "q-java-prog-1",
                "question": "How does HashMap work internally in Java 8+? What happens when two keys produce the same hash code?",
                "category": "Programming",
                "difficulty": "Intermediate",
                "hint": "Discuss buckets, linked lists, hash collisions, and balanced trees (Red-Black Trees).",
                "sample_answer_outline": "HashMap uses an array of Node buckets. On collision, entries form a linked list. In Java 8, when a bucket exceeds 8 entries and table capacity is >= 64, it converts to a Red-Black Tree, improving lookup from O(N) to O(log N)."
            }
        ]
    },
    "Python Developer": {
        "Programming": [
            {
                "id": "q-py-prog-1",
                "question": "What is the Global Interpreter Lock (GIL) in CPython, and what are its implications for CPU-bound versus I/O-bound concurrency?",
                "category": "Programming",
                "difficulty": "Intermediate",
                "hint": "Discuss thread safety, multi-threading vs multiprocessing, and asyncio.",
                "sample_answer_outline": "The GIL is a mutex preventing multiple native threads from executing Python bytecode simultaneously. For I/O-bound tasks, threading and asyncio work well because the GIL is released during I/O. For CPU-bound tasks, multiprocessing or C-extensions bypass the GIL to utilize multiple CPU cores."
            }
        ]
    },
    "Full Stack Developer": {
        "Technical Interview": [
            {
                "id": "q-fs-tech-1",
                "question": "Describe how JWT (JSON Web Token) authentication works in a Single Page Application (SPA). Where should tokens be stored, and how do you prevent XSS/CSRF?",
                "category": "Technical Interview",
                "difficulty": "Intermediate",
                "hint": "Compare localStorage vs httpOnly Secure cookies, CSRF protection, and token expiration.",
                "sample_answer_outline": "The client sends credentials, the server validates and signs a JWT containing claims. Storing tokens in httpOnly Secure SameSite cookies shields them from JavaScript XSS attacks. For CSRF protection, SameSite cookies or CSRF tokens should be employed."
            }
        ]
    },
    "General": {
        "HR Interview": [
            {
                "id": "q-hr-1",
                "question": "Describe a challenging technical obstacle you faced in a software project and how you systematically diagnosed and resolved it.",
                "category": "HR Interview",
                "difficulty": "General",
                "hint": "Use the STAR method: Situation, Task, Action, Result.",
                "sample_answer_outline": "Structure using STAR: Describe the project context and bug, explain the diagnostic process (logs, debugging, profiling), detail your solution, and quantify the result."
            }
        ],
        "Communication Skills": [
            {
                "id": "q-comm-1",
                "question": "How do you explain the concept of technical debt to a product manager who wants to prioritize new features over refactoring?",
                "category": "Communication Skills",
                "difficulty": "Intermediate",
                "hint": "Use financial metaphors, velocity risks, and bug frequency trends.",
                "sample_answer_outline": "Frame technical debt like financial debt: taking shortcuts incurs 'interest' that progressively slows feature delivery and spikes customer bugs. Propose a balanced 80/20 allocation to maintain sustainable team velocity."
            }
        ]
    }
}

def get_interview_questions(target_role: str, category: str, difficulty: str = "Intermediate") -> List[Dict[str, Any]]:
    """Returns interview questions for the specified role and category."""
    role_dict = CURATED_INTERVIEW_QUESTIONS.get(target_role, {})
    questions = role_dict.get(category, [])
    
    if not questions:
        # Check General
        questions = CURATED_INTERVIEW_QUESTIONS.get("General", {}).get(category, [])

    if not questions:
        # Fallback question tailored to role and category
        questions = [
            {
                "id": f"q-dynamic-{abs(hash(target_role + category)) % 1000}",
                "question": f"In {target_role} roles, what are the key architectural best practices you follow in {category}?",
                "category": category,
                "difficulty": difficulty,
                "hint": "Focus on modularity, clean architecture, performance, and maintainability.",
                "sample_answer_outline": f"Discuss core principles in {category}, industry design patterns, testing strategies, and production reliability."
            }
        ]

    return questions

def evaluate_and_record_answer(
    db: Session,
    user: User,
    target_role: str,
    category: str,
    question: str,
    student_answer: str
) -> Dict[str, Any]:
    """
    Evaluates student answer, creates interview session and response records.
    """
    # 1. Create session
    session = InterviewSession(
        user_id=user.id,
        category=category,
        target_role=target_role,
        difficulty="Intermediate",
        created_at=datetime.utcnow()
    )
    db.add(session)
    db.flush()

    # 2. Evaluate answer via AI Service (with deterministic fallback)
    eval_result = ai_service.evaluate_interview_response(
        target_role=target_role,
        category=category,
        question=question,
        student_answer=student_answer
    )

    rating = float(eval_result.get("rating", 70.0))
    strengths = eval_result.get("strengths", "")
    missing_concepts = eval_result.get("missing_concepts", "")
    feedback = eval_result.get("feedback", "")
    model_answer = eval_result.get("model_answer", "")
    is_ai = eval_result.get("is_ai_generated", False)

    # 3. Store response
    response_record = InterviewResponse(
        session_id=session.id,
        question=question,
        student_answer=student_answer,
        feedback=feedback,
        strengths=strengths,
        missing_concepts=missing_concepts,
        model_answer=model_answer,
        score=rating,
        created_at=datetime.utcnow()
    )
    db.add(response_record)

    # 4. Log activity
    log = ActivityLog(
        user_id=user.id,
        activity_type="interview",
        description=f"Completed {category} interview practice for {target_role} (Score: {rating:.0f}/100)",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return {
        "session_id": session.id,
        "question": question,
        "student_answer": student_answer,
        "rating": rating,
        "strengths": strengths,
        "missing_concepts": missing_concepts,
        "feedback": feedback,
        "model_answer": model_answer,
        "is_ai_generated": is_ai
    }
