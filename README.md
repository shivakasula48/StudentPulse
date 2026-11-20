# StudentPulse AI
### AI-Powered Student Success, Skill & Career Readiness Platform
**Team Name:** Byte Force  
**Core Philosophy:** EVIDENCE → INSIGHT → ACTION

---

## 📖 Overview

**StudentPulse AI** is a modern, full-stack educational technology SaaS platform designed to help college students understand their current capabilities, identify objective skill gaps against industry benchmarks, build relevant portfolio projects, and prepare for placement interviews.

Unlike platforms that rely on static advice or unverified claims, StudentPulse AI follows a strict **Evidence → Insight → Action** methodology:
- **Evidence**: Collects student academic records, self-reported skills, verified MCQ assessment results, real portfolio projects, and certifications.
- **Insight**: Deterministically evaluates student competencies against role-based requirements frameworks (e.g., Java Developer, Python Developer, Full Stack Developer, Data Analyst) and uses Google Gemini to explain gaps without hallucination.
- **Action**: Generates personalized, phased learning roadmaps, recommends gap-targeted project blueprints with 1-click adoption, and provides AI-assisted mock technical interview evaluations.

---

## 🛠 Technology Stack

### Frontend
- **React.js 18** with **Vite**
- **Tailwind CSS** (Modern Dark Navy / Charcoal theme with Cyan, Teal, and Violet accents)
- **React Router DOM v6** (Protected & Public routing)
- **Axios** (With automated JWT Bearer authorization interceptor)
- **Lucide React Icons**
- **Recharts** (Capability Radar Chart, Skill Gap Breakdown, Progress Metrics)

### Backend
- **Python 3.12+ / 3.14**
- **FastAPI** (Async REST API with interactive Swagger / OpenAPI docs)
- **Pydantic v2** (Strict data validation and serialization)
- **SQLAlchemy 2.0** (ORM with relational foreign keys and cascade rules)
- **JWT & Bcrypt** (Stateless authentication and secure password encryption)

### Database
- **PostgreSQL** (Production-ready) / **SQLite** (Zero-configuration local development)

### AI & Machine Learning
- **Google GenAI SDK** (`google-genai>=3.2.0`) with model `gemini-4-hydrogen`
- **Transparent Fallback Engine**: Fully functional deterministic rule-based analysis and rubric evaluation when no Gemini API key is provided or when offline.
- No fabricated ML claims or simulated employer ratings.

---

## 🚀 Quick Start & Setup

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Git**

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install email-validator

# Copy environment variables
cp .env.example .env

# Optional: Add your Google Gemini API key to .env if available
# GEMINI_API_KEY="your-gemini-api-key"

# Seed base skills, assessment questions, resources, and demo student
python -m app.database.demo_student

# Start the FastAPI backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Backend API will be running at: `http://127.0.0.1:8000`  
Interactive Swagger UI: `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup

In a new terminal window:

```bash
# Navigate to the frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend web application will be accessible at: `http://localhost:5173`

---

## 🔑 Pre-Loaded Demo Student Account

You can immediately sign in with the pre-seeded student account (or create a new account):

- **Email:** `alex.mercer@byteforce.edu`
- **Password:** `Password123!`
- **Target Role:** Java Developer
- **Pre-Loaded Records:** Verified Programming assessment score (75%), Academic profile, Adopted portfolio project, Oracle certification, and 4-Phase Learning Roadmap.

*(A 1-click "Click here to load Demo Student account" button is also provided on the Login page).*

---

## 🧪 Automated Test Suite (Pytest)

StudentPulse AI includes an automated test suite verifying all 16 core scenarios:

1. Student registration and login
2. Profile creation and editing
3. Add and update technical skills
4. Submit skill assessment
5. Calculate assessment score & update verified skill score
6. Select Java Developer as target career role
7. Identify missing Java Developer skills
8. Generate personalized learning roadmap
9. Recommend projects based on skill gaps & 1-click adoption
10. Generate interview questions
11. Evaluate student answers via rubric
12. Update roadmap task status
13. Update dashboard metrics with calculated data
14. Gemini API unavailable (graceful fallback check)
15. Invalid AI response handling
16. Cross-user isolation (Tenant privacy enforcement)

To execute the test suite:

```bash
cd backend
.venv/bin/pytest tests/test_api.py -v
```

All 16 test scenarios pass with zero regressions.

---

## 📂 Project Structure

```
studentpulse-ai/
│
├── frontend/                     # React + Vite + Tailwind CSS Application
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── context/              # AuthContext (JWT auth & state)
│   │   ├── layouts/              # SidebarLayout & Top Bar
│   │   ├── pages/                # All module pages
│   │   │   ├── LandingPage.jsx   # Public landing page with Evidence->Insight->Action
│   │   │   ├── LoginPage.jsx     # Student login
│   │   │   ├── RegisterPage.jsx  # Student onboarding
│   │   │   ├── DashboardPage.jsx # Career Readiness Dashboard & Recharts
│   │   │   ├── ProfilePage.jsx   # Unified Student Capability Profile
│   │   │   ├── SkillsPage.jsx    # Self-Reported vs. Verified Inventory
│   │   │   ├── AssessmentsPage.jsx # MCQ Assessment Studio & Review
│   │   │   ├── AnalysisPage.jsx  # Role-Based Skill Gap Matrix & AI Summary
│   │   │   ├── RoadmapPage.jsx   # Multi-Phase Learning Roadmap
│   │   │   ├── ProjectsPage.jsx  # Gap-Targeted Project Recommendations
│   │   │   ├── InterviewPage.jsx # AI Mock Technical Interview Studio
│   │   │   └── ResourcesPage.jsx # Curated Learning Documentation
│   │   ├── services/             # Axios API client
│   │   ├── App.jsx               # Route definitions & guards
│   │   ├── main.jsx              # React entrypoint
│   │   └── index.css             # Tailwind base styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── backend/                      # Python FastAPI Application
│   ├── app/
│   │   ├── core/                 # Config & JWT/bcrypt security
│   │   ├── database/             # SQLAlchemy engine, session & seeds
│   │   ├── models/               # Relational SQLAlchemy models
│   │   ├── schemas/              # Pydantic v2 schemas
│   │   ├── routes/               # Modular REST API endpoints
│   │   ├── services/             # Business intelligence & AI logic
│   │   │   ├── ai_service.py     # Gemini SDK + Deterministic fallback
│   │   │   ├── skill_gap.py      # Deterministic gap matrix engine
│   │   │   ├── roadmap.py        # Phased curriculum generator
│   │   │   ├── project_recommendation.py # Portfolio project catalogue
│   │   │   └── interview_service.py # Rubric evaluation engine
│   │   └── main.py               # FastAPI application entrypoint
│   ├── tests/                    # Pytest integration test suite
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── .env                      # Local configuration
│
├── docs/                         # Technical Documentation
│   ├── architecture/             # Architecture specification
│   └── api/                      # REST API endpoint reference
│
├── README.md                     # Project documentation
└── .gitignore
```

---

## 🛡 Responsible AI & Security

1. **Evidence-Based Insights**: The AI service never fabricates qualifications, certifications, project experience, or assessment test scores.
2. **Transparent Fallback**: The platform functions seamlessly without requiring an external API key by falling back to its deterministic rule-based engine.
3. **No Employment Guarantees**: Career readiness scores represent alignment with industry expectations, not guaranteed employment.
4. **Data Isolation**: All queries enforce strict user-level access controls so students can never view or modify another student's private data.

---

## 👥 Byte Force Team Credits
Developed by **Byte Force** for the StudentPulse AI initiative.
All components built, verified, and ready for deployment.
