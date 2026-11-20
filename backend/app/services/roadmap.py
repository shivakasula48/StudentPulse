from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.models.models import (
    User, LearningRoadmap, RoadmapTask, ActivityLog
)
from app.services.skill_gap import analyze_skill_gap

def generate_learning_roadmap(db: Session, user: User, target_role: str) -> LearningRoadmap:
    """
    Generates a personalized, phased learning roadmap based on identified skill gaps.
    """
    # 1. Analyze skill gaps to customize roadmap focus
    gap_result = analyze_skill_gap(db, user, target_role)
    missing_skill_names = [s.skill_name for s in gap_result.missing_skills]
    improve_skill_names = [s.skill_name for s in gap_result.needs_improvement_skills]

    # Delete or archive previous roadmap for this role to avoid duplicate confusion
    old_roadmaps = (
        db.query(LearningRoadmap)
        .filter(LearningRoadmap.user_id == user.id, LearningRoadmap.target_role == target_role)
        .all()
    )
    for r in old_roadmaps:
        db.delete(r)
    db.flush()

    # Create new roadmap
    roadmap = LearningRoadmap(
        user_id=user.id,
        title=f"{target_role} Personalized Acceleration Roadmap",
        target_role=target_role,
        created_at=datetime.utcnow()
    )
    db.add(roadmap)
    db.flush()

    tasks_to_add: List[RoadmapTask] = []
    base_date = datetime.utcnow()

    # Define phased curriculum tailored to target_role
    if "java" in target_role.lower():
        tasks_to_add = [
            # Phase 1: Core Java & OOP
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 1: Foundations",
                title="Master Core Java & OOP Principles",
                description="Deep dive into JVM memory, encapsulation, inheritance, polymorphism, and Java 17+ records.",
                priority="Critical" if "Java" in missing_skill_names or "OOP" in missing_skill_names else "Medium",
                difficulty="Beginner to Intermediate",
                estimated_duration="1 week",
                learning_objective="Implement clean class hierarchies, handle checked exceptions, and write unit tests.",
                recommended_resources="Oracle Java Tutorials, Head First Java",
                due_date=(base_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                status="In Progress"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 1: Foundations",
                title="Java Collections Framework & Generics",
                description="Study ArrayList, LinkedList, HashMap, ConcurrentHashMap, and custom Comparator/Comparable.",
                priority="Critical" if "Collections Framework" in missing_skill_names else "High",
                difficulty="Intermediate",
                estimated_duration="5 days",
                learning_objective="Select optimal data collections based on algorithmic complexity and thread-safety.",
                recommended_resources="Baeldung Java Collections Guide",
                due_date=(base_date + timedelta(days=12)).strftime("%Y-%m-%d"),
                status="Pending"
            ),

            # Phase 2: Database & Backend Integration
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 2: Backend Integration",
                title="Relational SQL & JDBC / JPA Persistence",
                description="Practice complex joins, indexing, transactions, and connect Java using JDBC PreparedStatement.",
                priority="High" if "SQL" in missing_skill_names or "JDBC" in missing_skill_names else "Medium",
                difficulty="Intermediate",
                estimated_duration="1 week",
                learning_objective="Write parameterized SQL queries, understand connection pooling, and avoid N+1 queries.",
                recommended_resources="PostgreSQL Docs, Baeldung JDBC Tutorials",
                due_date=(base_date + timedelta(days=19)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 2: Backend Integration",
                title="Spring Boot & RESTful Microservices",
                description="Build REST controllers, configure dependency injection (@Service, @Repository), and manage DTOs.",
                priority="Critical" if "Spring Boot" in missing_skill_names or "REST APIs" in missing_skill_names else "High",
                difficulty="Intermediate",
                estimated_duration="10 days",
                learning_objective="Expose clean REST endpoints with validation, global exception handling, and OpenAPI documentation.",
                recommended_resources="Spring Guides, Spring Boot in Action",
                due_date=(base_date + timedelta(days=29)).strftime("%Y-%m-%d"),
                status="Pending"
            ),

            # Phase 3: Project Development
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 3: Portfolio Project",
                title="Build Full-Stack Student or Employee Management System",
                description="Architect an enterprise backend using Spring Boot, Spring Data JPA, PostgreSQL, and JWT auth.",
                priority="High",
                difficulty="Advanced",
                estimated_duration="2 weeks",
                learning_objective="Demonstrate production-grade code with automated tests and a live deployment demo.",
                recommended_resources="Spring Boot + React Architecture Guide",
                due_date=(base_date + timedelta(days=43)).strftime("%Y-%m-%d"),
                status="Pending"
            ),

            # Phase 4: Placement & Interview Prep
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 4: Placement Prep",
                title="DSA & Java Concurrency Interview Practice",
                description="Practice top 50 LeetCode patterns in Java, multithreading, and rehearse Java interview questions.",
                priority="Critical",
                difficulty="Advanced",
                estimated_duration="10 days",
                learning_objective="Confidently solve medium DSA problems and explain Java concurrency mechanisms in interviews.",
                recommended_resources="NeetCode 150, StudentPulse AI Interview Simulator",
                due_date=(base_date + timedelta(days=53)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
        ]
    elif "python" in target_role.lower():
        tasks_to_add = [
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 1: Foundations",
                title="Advanced Python Programming & Best Practices",
                description="Generators, decorators, context managers, type hinting, and modern Python 3.12+ features.",
                priority="Critical" if "Python" in missing_skill_names else "High",
                difficulty="Intermediate",
                estimated_duration="1 week",
                learning_objective="Write idiomatic, modular Python code adhering to PEP 8 standards.",
                recommended_resources="Fluent Python, Official Python Docs",
                due_date=(base_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                status="In Progress"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 2: Backend Integration",
                title="FastAPI Web Framework & Async Programming",
                description="Async route handlers, Pydantic data schemas, dependency injection, and JWT authentication.",
                priority="Critical" if "FastAPI" in missing_skill_names else "High",
                difficulty="Intermediate",
                estimated_duration="10 days",
                learning_objective="Build high-throughput REST APIs with automated interactive OpenAPI documentation.",
                recommended_resources="FastAPI Official Tutorials",
                due_date=(base_date + timedelta(days=17)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 3: Portfolio Project",
                title="Build Scalable Microservices Architecture with Docker",
                description="Containerize a multi-service FastAPI app with Redis caching and PostgreSQL persistence.",
                priority="High",
                difficulty="Advanced",
                estimated_duration="2 weeks",
                learning_objective="Demonstrate production containerization, database migrations, and CI pipeline.",
                recommended_resources="Docker Documentation, FastAPI Microservices",
                due_date=(base_date + timedelta(days=31)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 4: Placement Prep",
                title="Python System Design & Coding Interview Mastery",
                description="Master Python data structures, big-O analysis, and technical problem-solving patterns.",
                priority="Critical",
                difficulty="Advanced",
                estimated_duration="10 days",
                learning_objective="Crack technical coding rounds and explain distributed system trade-offs.",
                recommended_resources="NeetCode, StudentPulse AI Interview Studio",
                due_date=(base_date + timedelta(days=41)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
        ]
    else:
        # General Software / Full Stack Roadmap
        tasks_to_add = [
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 1: Foundations",
                title=f"Core Competencies for {target_role}",
                description=f"Strengthen baseline skills: {', '.join(missing_skill_names[:3]) if missing_skill_names else 'Core programming principles'}.",
                priority="Critical",
                difficulty="Intermediate",
                estimated_duration="1 week",
                learning_objective="Achieve working proficiency in foundational syntax, structures, and Git version control.",
                recommended_resources="Official Language Docs & Tutorials",
                due_date=(base_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                status="In Progress"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 2: System Architecture",
                title="Database Design & API Development",
                description="Design normalized schemas, index critical tables, and create robust RESTful endpoints.",
                priority="High",
                difficulty="Intermediate",
                estimated_duration="10 days",
                learning_objective="Build secure backend services with proper input validation and error handling.",
                recommended_resources="REST API Best Practices, SQL Optimization",
                due_date=(base_date + timedelta(days=17)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 3: Applied Project",
                title=f"Full-Featured Portfolio Project for {target_role}",
                description="Build and deploy a complete project solving a real student or industry problem.",
                priority="High",
                difficulty="Advanced",
                estimated_duration="2 weeks",
                learning_objective="Deliver a working application with GitHub documentation and live deployment link.",
                recommended_resources="Full Stack Project Blueprint",
                due_date=(base_date + timedelta(days=31)).strftime("%Y-%m-%d"),
                status="Pending"
            ),
            RoadmapTask(
                roadmap_id=roadmap.id,
                phase="Phase 4: Placement Prep",
                title="Technical Assessment & Interview Readiness",
                description="Solve role-specific algorithmic challenges and practice interview responses.",
                priority="Critical",
                difficulty="Advanced",
                estimated_duration="10 days",
                learning_objective="Achieve readiness in live coding rounds and technical design discussions.",
                recommended_resources="StudentPulse AI Interview Practice Studio",
                due_date=(base_date + timedelta(days=41)).strftime("%Y-%m-%d"),
                status="Pending"
            )
        ]

    for t in tasks_to_add:
        db.add(t)

    # Activity log
    log = ActivityLog(
        user_id=user.id,
        activity_type="roadmap",
        description=f"Generated personalized learning roadmap for {target_role} ({len(tasks_to_add)} tasks)",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(roadmap)
    return roadmap
