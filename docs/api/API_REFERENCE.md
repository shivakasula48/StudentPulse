# StudentPulse AI – REST API Reference Manual
### Base URL: `/api`
### Interactive Swagger Documentation: `http://localhost:8000/docs`

---

## 1. Authentication Endpoints

### Register Student Account
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "name": "Alex Mercer",
    "email": "alex.mercer@byteforce.edu",
    "password": "Password123!",
    "college": "National Institute of Technology",
    "degree": "B.Tech Computer Science",
    "semester": "6th Semester",
    "career_interest": "Java Developer"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "Alex Mercer",
      "email": "alex.mercer@byteforce.edu",
      "created_at": "2026-11-20T11:00:00Z"
    }
  }
  ```

### Student Login
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "alex.mercer@byteforce.edu",
    "password": "Password123!"
  }
  ```
- **Response** (`200 OK`): Token and user object.

### Current User Profile
- **Endpoint**: `GET /api/auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response** (`200 OK`): Authenticated user and profile summary.

---

## 2. Student Profile Endpoints

### Get Unified Profile
- **Endpoint**: `GET /api/profile`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Full student capability profile (basic info, skills, projects, certifications, assessments).

### Update Profile Info
- **Endpoint**: `PUT /api/profile`
- **Request Body**:
  ```json
  {
    "name": "Alex Mercer Updated",
    "college": "National Institute of Technology",
    "semester": "7th Semester",
    "graduation_year": 2026
  }
  ```

### Manage Certifications
- `POST /api/profile/certifications` (Create credential)
- `DELETE /api/profile/certifications/{id}` (Delete credential)

### Career Goals
- `POST /api/profile/career-goals` (Set target career role)

---

## 3. Skills Endpoints

- `GET /api/skills`: Full master taxonomy of skills.
- `GET /api/skills/my-skills`: Student's attached skills with self-reported level and verified test score.
- `POST /api/skills/my-skills`: Add or update a skill in student inventory.
- `PUT /api/skills/my-skills/{id}`: Update proficiency level (Beginner, Intermediate, Advanced).
- `DELETE /api/skills/my-skills/{id}`: Remove skill from student inventory.

---

## 4. Assessment Endpoints

- `GET /api/assessments/categories`: List of 8 assessment categories with metadata.
- `GET /api/assessments/questions?category=...`: MCQs for active category (answers hidden).
- `POST /api/assessments/submit`:
  - **Payload**:
    ```json
    {
      "category": "Programming Skills",
      "answers": [
        { "question_id": 1, "selected_answer": "A" },
        { "question_id": 2, "selected_answer": "B" }
      ]
    }
    ```
  - **Response**: Total calculated score, verified skill score update, and question explanations.
- `GET /api/assessments/results`: Past assessment history.

---

## 5. Skill Gap Analysis Endpoints

- `GET /api/analysis/roles`: Available target roles and requirements.
- `POST /api/analysis/skill-gap`:
  - **Payload**: `{"target_role": "Java Developer"}`
  - **Response**: Match %, categorized gap lists (Strong, Needs Improvement, Missing), and AI explanatory summary.
- `GET /api/analysis/skill-gap/history`: Previous analysis audit logs.

---

## 6. Learning Roadmap Endpoints

- `POST /api/roadmap/generate`: Generates personalized multi-phase curriculum based on current gaps.
- `GET /api/roadmap`: Returns active roadmap with tasks.
- `PUT /api/roadmap/tasks/{id}`: Update task status (`Pending`, `In Progress`, `Completed`).

---

## 7. Project Recommendations & Portfolio

- `GET /api/projects/recommendations?target_role=...`: Gap-targeting project recommendations.
- `POST /api/projects/adopt`: 1-click adopt project into personal portfolio.
- `GET /api/projects`: List active and completed projects.
- `POST /api/projects`: Add manual project.
- `PUT /api/projects/{id}`: Update status and links.
- `DELETE /api/projects/{id}`: Delete project.

---

## 8. AI Mock Interview Preparation

- `GET /api/interview/categories`: Supported categories.
- `POST /api/interview/generate`: Get role and category questions with hints.
- `POST /api/interview/evaluate`:
  - **Payload**:
    ```json
    {
      "target_role": "Java Developer",
      "category": "OOP",
      "question": "What is polymorphism?",
      "student_answer": "Polymorphism allows objects to take multiple forms..."
    }
    ```
  - **Response**: Rubric score (0–100), strengths, missing concepts, feedback, and model answer.
- `GET /api/interview/history`: Past practice sessions.

---

## 9. Career Readiness Dashboard

- `GET /api/dashboard/summary`:
  - Returns calculated Readiness Score, Profile Completeness, Radar chart proficiency array, Gap breakdown, and Context-Aware Recommended Next Action.

---

## 10. System Health

- `GET /api/health`: Health status, DB latency check, and Gemini AI connection status.
