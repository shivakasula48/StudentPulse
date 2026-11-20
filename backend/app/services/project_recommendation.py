from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import User, Skill, StudentSkill, Project, ActivityLog
from app.schemas.schemas import RecommendedProjectOut

PROJECT_CATALOGUE = {
    "Java Developer": [
        {
            "id": "proj-java-1",
            "title": "Enterprise Employee & Payroll Management System",
            "description": "A multi-tiered enterprise backend application with role-based access control, automated payroll computation, and audit logging.",
            "problem_statement": "Manual corporate payroll processing leads to computation errors, compliance issues, and data inconsistency across departments.",
            "technologies": ["Java 17+", "Spring Boot", "Spring Data JPA", "PostgreSQL", "JWT", "Docker"],
            "features": [
                "Role-based authentication (Admin, HR, Employee)",
                "Salary slip generation with PDF export",
                "Automated scheduled batch payroll processing",
                "Transactional database updates with optimistic locking"
            ],
            "difficulty": "Intermediate",
            "skills_developed": ["Core Java", "Spring Boot", "SQL", "JDBC", "REST APIs", "Git and GitHub"],
            "implementation_steps": [
                "Step 1: Design normalized ER diagram for Employees, Departments, and PayrollRecords in PostgreSQL.",
                "Step 2: Initialize Spring Boot project with Spring Web, Security, and JPA dependencies.",
                "Step 3: Implement JWT authentication filter and UserDetails service.",
                "Step 4: Build REST endpoints for CRUD operations and salary calculations with unit tests.",
                "Step 5: Write automated JUnit/Mockito tests and package as Docker container."
            ],
            "expected_outcome": "A fully functional enterprise REST API with 85%+ test coverage, Swagger docs, and Dockerfile."
        },
        {
            "id": "proj-java-2",
            "title": "High-Throughput Banking Transaction Service",
            "description": "A resilient financial ledger service managing simulated bank accounts, atomic fund transfers, and ledger reconciliation.",
            "problem_statement": "Concurrent financial transactions can cause race conditions, double-spending, and inconsistent account balances under peak load.",
            "technologies": ["Core Java", "Spring Boot", "PostgreSQL", "Redis", "JUnit 5"],
            "features": [
                "Pessimistic and optimistic locking on account balances",
                "Idempotent fund transfer REST endpoint with deduplication tokens",
                "Audit ledger table recording every debit/credit event",
                "Swagger OpenAPI interactive documentation"
            ],
            "difficulty": "Advanced",
            "skills_developed": ["OOP", "Collections Framework", "SQL", "Spring Boot", "Concurrency"],
            "implementation_steps": [
                "Step 1: Set up account schema with strict check constraints.",
                "Step 2: Implement TransferService using @Transactional(isolation = Isolation.SERIALIZABLE).",
                "Step 3: Add Redis distributed lock or DB pessimistic row lock for balance updates.",
                "Step 4: Write JMeter or concurrent multithreaded test suite verifying zero race conditions.",
                "Step 5: Document architecture and publish repository to GitHub."
            ],
            "expected_outcome": "A robust financial backend engine capable of handling concurrent transactions without double spending."
        }
    ],
    "Python Developer": [
        {
            "id": "proj-py-1",
            "title": "Async Task Processing & Webhook Dispatcher",
            "description": "An asynchronous worker service built with FastAPI and Redis to queue, execute, and retry webhook notifications with exponential backoff.",
            "problem_statement": "Synchronous webhook delivery blocks web servers, degrades response latency, and loses messages when external endpoints fail.",
            "technologies": ["Python", "FastAPI", "Redis", "PostgreSQL", "Pydantic", "Docker"],
            "features": [
                "Async endpoint to enqueue webhook payloads with signature validation",
                "Background worker with exponential backoff retries",
                "Delivery status dashboard with success/failure analytics",
                "Full OpenAPI documentation and metrics tracking"
            ],
            "difficulty": "Intermediate",
            "skills_developed": ["Python", "FastAPI", "REST APIs", "Docker", "Data Structures and Algorithms"],
            "implementation_steps": [
                "Step 1: Scaffold FastAPI application with Pydantic validation schemas.",
                "Step 2: Integrate Redis task queue or background worker pool.",
                "Step 3: Implement HMAC-SHA256 payload signing for recipient security.",
                "Step 4: Build PostgreSQL audit model for webhook delivery logs.",
                "Step 5: Deploy with Docker Compose."
            ],
            "expected_outcome": "A production-grade async service with sub-5ms enqueue latency and guaranteed webhook retries."
        }
    ],
    "Full Stack Developer": [
        {
            "id": "proj-fs-1",
            "title": "StudentPulse AI - Student Career & Readiness Hub",
            "description": "Full-stack EdTech SaaS application connecting academic performance, automated skill gap assessments, personalized roadmaps, and AI interview prep.",
            "problem_statement": "Students struggle to navigate disjointed learning resources and lack evidence-backed visibility into their actual job readiness.",
            "technologies": ["React", "FastAPI", "PostgreSQL", "Tailwind CSS", "Recharts", "Gemini API"],
            "features": [
                "Unified student profile with technical and soft skills inventory",
                "Interactive MCQ assessments with verified skill score computation",
                "Role-based skill gap matrix and readiness index radar charts",
                "Dynamic multi-phase learning roadmap with status tracking",
                "AI-powered interview practice simulator with rubric feedback"
            ],
            "difficulty": "Advanced",
            "skills_developed": ["React", "JavaScript", "FastAPI", "SQL", "REST APIs", "Git and GitHub"],
            "implementation_steps": [
                "Step 1: Design database schema for users, skills, assessments, roadmaps, and logs.",
                "Step 2: Build FastAPI REST backend with JWT authentication and deterministic scoring.",
                "Step 3: Create modern React dashboard with Tailwind CSS and Recharts visualizations.",
                "Step 4: Integrate AI service with deterministic fallback for roadmap and feedback.",
                "Step 5: Write unit tests and deploy full-stack app."
            ],
            "expected_outcome": "A complete commercial-grade SaaS platform showcasing full-stack competency from UI to database."
        }
    ],
    "Frontend Developer": [
        {
            "id": "proj-fe-1",
            "title": "Interactive Algorithm & Data Structure Visualizer",
            "description": "A high-performance visual simulator in React illustrating sorting algorithms, graph traversals (BFS/DFS, Dijkstra), and tree balancing.",
            "problem_statement": "Abstract computer science algorithms are notoriously difficult for students to understand without dynamic step-by-step visual feedback.",
            "technologies": ["React", "TypeScript", "Tailwind CSS", "HTML/CSS Canvas", "Lucide React"],
            "features": [
                "Step-by-step playback controls (Play, Pause, Step Forward, Speed slider)",
                "Real-time visual comparison of QuickSort vs MergeSort",
                "Interactive graph canvas with custom node and edge addition",
                "Live code viewer highlighting currently executing line"
            ],
            "difficulty": "Intermediate",
            "skills_developed": ["JavaScript", "React", "TypeScript", "HTML/CSS", "Data Structures and Algorithms"],
            "implementation_steps": [
                "Step 1: Set up React + Vite project with TypeScript.",
                "Step 2: Implement generator-based sorting algorithms yielding state snapshots.",
                "Step 3: Build responsive visual bar canvas and animation hook.",
                "Step 4: Add graph traversal interactive canvas.",
                "Step 5: Deploy on Vercel/Netlify with CI pipeline."
            ],
            "expected_outcome": "A polished, responsive portfolio web app demonstrating mastery of React rendering cycles and algorithmic intuition."
        }
    ],
    "Data Analyst": [
        {
            "id": "proj-da-1",
            "title": "E-Commerce Customer Churn & Cohort Analysis Engine",
            "description": "An end-to-end analytics project analyzing transactional retail data to identify customer churn risk and lifetime value cohorts.",
            "problem_statement": "Subscription businesses lose revenue because they fail to identify early signals of customer disengagement.",
            "technologies": ["Python", "SQL", "PostgreSQL", "Pandas", "NumPy", "Matplotlib/Seaborn"],
            "features": [
                "SQL-driven RFM (Recency, Frequency, Monetary) segmentation",
                "Monthly cohort retention heatmaps",
                "Feature importance analysis for churn indicators",
                "Executive summary dashboard with actionable retention strategies"
            ],
            "difficulty": "Intermediate",
            "skills_developed": ["SQL", "Python", "Data Analysis", "Problem Solving", "Communication"],
            "implementation_steps": [
                "Step 1: Clean and ingest 500k+ transactional records into PostgreSQL.",
                "Step 2: Write complex SQL window functions to calculate retention cohorts.",
                "Step 3: Perform EDA and cohort analysis using Pandas.",
                "Step 4: Generate visual heatmaps and retention curves.",
                "Step 5: Draft technical and executive report outlining 3 key retention initiatives."
            ],
            "expected_outcome": "A reproducible data analysis notebook and executive presentation with validated business insights."
        }
    ],
    "AI/ML Engineer": [
        {
            "id": "proj-ml-1",
            "title": "Predictive Equipment Maintenance & Anomaly Detection Pipeline",
            "description": "An end-to-end machine learning pipeline detecting anomalous sensor telemetry to predict machinery failures before they occur.",
            "problem_statement": "Unscheduled industrial downtime costs factories millions; preventive maintenance models save costs by predicting early failures.",
            "technologies": ["Python", "Machine Learning", "Scikit-Learn", "FastAPI", "Docker", "Pandas"],
            "features": [
                "Time-series feature engineering (rolling averages, Fourier transforms)",
                "Trained and cross-validated Random Forest & Isolation Forest models",
                "FastAPI inference microservice accepting real-time sensor streams",
                "Drift detection and model evaluation metrics (F1, ROC-AUC)"
            ],
            "difficulty": "Advanced",
            "skills_developed": ["Python", "Machine Learning", "Data Analysis", "Deep Learning", "Git and GitHub"],
            "implementation_steps": [
                "Step 1: Preprocess raw sensor data with Pandas and handle sensor dropouts.",
                "Step 2: Train baseline models and evaluate with Stratified K-Fold cross-validation.",
                "Step 3: Tune hyperparameters and optimize threshold for high precision.",
                "Step 4: Wrap inference model into FastAPI endpoint with input validation.",
                "Step 5: Containerize with Docker and document model card."
            ],
            "expected_outcome": "A deployed ML inference API with documented model performance, evaluation notebooks, and reproducible Docker container."
        }
    ]
}

def get_recommended_projects(db: Session, user: User, target_role: str) -> List[Dict[str, Any]]:
    """
    Returns curated project recommendations tailored to the student's target role and skill gaps.
    """
    # Check catalogue
    matched_projects = PROJECT_CATALOGUE.get(target_role)
    if not matched_projects:
        # Default fallback to Full Stack / Software Engineer
        matched_projects = PROJECT_CATALOGUE.get("Full Stack Developer", [])

    return matched_projects

def adopt_project_to_profile(db: Session, user: User, title: str, description: str, technologies: str) -> Project:
    """
    Adopts a recommended project idea into the student's personal project list.
    """
    project = Project(
        user_id=user.id,
        title=title,
        description=description,
        technologies=technologies,
        status="Planned"
    )
    db.add(project)

    log = ActivityLog(
        user_id=user.id,
        activity_type="project",
        description=f"Adopted new project to portfolio: '{title}'",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(project)
    return project
