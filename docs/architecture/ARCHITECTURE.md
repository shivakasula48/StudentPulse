# StudentPulse AI – Architecture Design Document
### Team: Byte Force
### Core Philosophy: EVIDENCE → INSIGHT → ACTION

---

## 1. Executive Summary

**StudentPulse AI** is a modern, full-stack educational technology platform engineered to bridge the critical gap between college academic curriculum and employer expectations. Rather than relying on static roadmaps or unverified self-assessments, StudentPulse AI implements a structured, evidence-driven capability evaluation loop:

1. **Evidence**: Unified collection of academic standing, self-reported skills, verified MCQ assessment results, project deliverables, and certifications.
2. **Insight**: Deterministic role-benchmark gap analysis coupled with Google Gemini explainability to pinpoint exact deficiencies without algorithmic hallucinations.
3. **Action**: Dynamic multi-phase learning curricula, hands-on portfolio project blueprints with 1-click adoption, and AI-assisted technical mock interview simulations.

---

## 2. High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                        STUDENTPULSE AI FRONTEND                        │
│                React.js + Vite + Tailwind CSS + Recharts               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST APIs (JSON + JWT)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND CORE                           │
│  ┌───────────────────────┐  ┌───────────────────────────────────────┐  │
│  │   Auth & Security     │  │          API Route Handlers           │  │
│  │  JWT + bcrypt Hashing │  │ Profile, Skills, Assessments, Roadmap │  │
│  └───────────────────────┘  └───────────────────┬───────────────────┘  │
│                                                 │                      │
│             ┌───────────────────────────────────┴────────────────┐     │
│             ▼                                                    ▼     │
│  ┌───────────────────────┐                    ┌──────────────────────┐ │
│  │ Deterministic Engines │                    │  AI Service Layer    │ │
│  │  - Role Gap Matrix    │                    │  - Google GenAI SDK  │ │
│  │  - Assessment Scorer  │                    │  - Gemini 4 Hydrogen │ │
│  │  - Readiness Index    │                    │  - Safe Fallback     │ │
│  └──────────┬────────────┘                    └──────────┬───────────┘ │
└─────────────┼────────────────────────────────────────────┼─────────────┘
              ▼                                            ▼
┌───────────────────────────────────┐        ┌───────────────────────────┐
│     POSTGRESQL / SQLITE DB        │        │     GOOGLE GEMINI API     │
│  Users, Profiles, Skills, Gaps,   │        │   Role-Gap Explanations,  │
│  Roadmaps, Tasks, Logs, Sessions  │        │   Interview Rubric Eval   │
└───────────────────────────────────┘        └───────────────────────────┘
```

---

## 3. Core Modules & Subsystems

### A. Authentication & Security Layer
- **Stateless JWT Tokens**: Signed with HMAC-SHA256 containing expiration timestamps.
- **Bcrypt Password Encryption**: Salts and hashes credentials up to 72 bytes safely.
- **Tenant Isolation**: Every database query joins through authenticated `current_user.id` to guarantee that no student can inspect or modify another candidate's private records.

### B. Evidence Collection Subsystem
- **Academic & Basic Info**: College, degree, semester, graduation year, target role.
- **Skills Catalog**: Covers Programming, Web, Databases, Frameworks, Tools, AI/ML, and Soft Skills.
- **Self-Reported vs. Verified Indicator**: Self-reported levels (Beginner, Intermediate, Advanced) are separated from objective test scores (0–100%).

### C. Deterministic Gap Engine + AI Explanation Layer
- Compares student competencies against a configurable `RoleSkillRequirement` framework.
- Levels are normalized to integer values (Beginner: 1, Intermediate: 2, Advanced: 3).
- **Rule Categorization**:
  - `Missing`: Prerequisite skill not present in profile.
  - `Needs Improvement`: Student level is lower than required, or verified test score is below 60%.
  - `Strong`: Student level meets or exceeds role requirement and verified score >= 60%.
- **Role Alignment Formula**:
  $$\text{Match \%} = \frac{\text{Strong Count} \times 1.0 + \text{Needs Improvement Count} \times 0.5}{\text{Total Required Skills}} \times 100$$
- **AI Service Integration**:
  - Minimum necessary context (role, match %, strong list, weak list, missing list) is sent to Gemini.
  - If the Gemini API key is unset or network fails, an internal deterministic rule-based generator produces the exact evidence-based analysis transparently.

### D. Career Readiness Score Calculation
No fabricated percentages. Readiness is computed strictly from real records:
$$\text{Readiness Index} = (P \times 0.10) + (A \times 0.35) + (T \times 0.25) + (R \times 0.15) + (E \times 0.15)$$
Where:
- $P$: Profile completeness percentage (0–100)
- $A$: Target role skill alignment ratio (0–100)
- $T$: Average score across completed verified assessment tests (0–100)
- $R$: Personalized learning roadmap tasks completed percentage (0–100)
- $E$: Portfolio project deliverable factor (0–100)

---

## 4. Database Schema Design

- **users**: Master account credentials (`id`, `name`, `email`, `password_hash`, `created_at`).
- **student_profiles**: Academic records (`user_id`, `college`, `degree`, `semester`, `graduation_year`, `career_interest`).
- **skills**: Master taxonomy (`id`, `name`, `category`, `description`).
- **student_skills**: Per-user skill junction (`user_id`, `skill_id`, `self_reported_level`, `assessment_score`).
- **assessment_questions**: Curated test questions (`category`, `skill_name`, `question_text`, `options A-D`, `correct_option`, `explanation`).
- **assessments**: Historical test events (`user_id`, `category`, `total_questions`, `score`, `completed_at`).
- **assessment_answers**: Granular submission records (`assessment_id`, `question_id`, `selected_answer`, `is_correct`).
- **role_skill_requirements**: Role benchmark taxonomy (`role_name`, `skill_id`, `required_level`, `priority`).
- **skill_gap_analyses**: Saved audit logs (`user_id`, `career_goal_id`, `analysis_json`, `created_at`).
- **learning_roadmaps** & **roadmap_tasks**: Phased actionable curricula (`roadmap_id`, `phase`, `title`, `description`, `priority`, `difficulty`, `status`).
- **projects**: Student practical portfolio (`user_id`, `title`, `description`, `technologies`, `github_url`, `live_url`, `status`).
- **certifications**: Verified credentials (`user_id`, `title`, `issuing_organization`, `credential_url`).
- **interview_sessions** & **interview_responses**: Mock interviews with rubric evaluations (`session_id`, `question`, `student_answer`, `feedback`, `strengths`, `missing_concepts`, `model_answer`, `score`).
- **activity_logs**: Audit timeline (`user_id`, `activity_type`, `description`, `created_at`).
- **learning_resources**: Curated official documentation and tutorial repository (`title`, `skill_category`, `resource_type`, `url`).

---

## 5. Security & AI Governance Principles

1. **Explainable AI**: The AI service never invents credentials or calculates scores; scores are computed deterministically by backend rules, and AI acts as an explanatory and coaching advisor.
2. **Transparent Fallback**: When Gemini is unavailable, the system displays an indicator that the rule-based engine is active, remaining 100% operational.
3. **No Employment Guarantees**: Career readiness evaluates alignment with benchmarks; the platform never falsely claims guaranteed placements.
