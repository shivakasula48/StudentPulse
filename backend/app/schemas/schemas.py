from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# --- Auth Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    college: Optional[str] = None
    degree: Optional[str] = None
    semester: Optional[str] = None
    career_interest: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    user_id: Optional[int] = None

# --- Student Profile Schemas ---
class StudentProfileBase(BaseModel):
    college: Optional[str] = None
    degree: Optional[str] = None
    semester: Optional[str] = None
    graduation_year: Optional[int] = None
    career_interest: Optional[str] = None

class StudentProfileUpdate(StudentProfileBase):
    name: Optional[str] = None

class StudentProfileOut(StudentProfileBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

# --- Skill Schemas ---
class SkillOut(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class StudentSkillCreate(BaseModel):
    skill_name: str
    self_reported_level: str  # Beginner, Intermediate, Advanced

class StudentSkillUpdate(BaseModel):
    self_reported_level: str

class StudentSkillOut(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill: SkillOut
    self_reported_level: str
    assessment_score: Optional[float] = None
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Assessment Schemas ---
class AssessmentQuestionOut(BaseModel):
    id: int
    category: str
    skill_name: str
    difficulty: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    model_config = ConfigDict(from_attributes=True)

class AssessmentSubmissionItem(BaseModel):
    question_id: int
    selected_answer: str  # A, B, C, D

class AssessmentSubmitRequest(BaseModel):
    category: str
    answers: List[AssessmentSubmissionItem]

class AssessmentResultDetail(BaseModel):
    question_id: int
    question_text: str
    selected_answer: str
    correct_option: str
    is_correct: bool
    explanation: Optional[str] = None
    skill_name: str

class AssessmentOut(BaseModel):
    id: int
    category: str
    total_questions: int
    score: float
    completed_at: datetime
    answers: Optional[List[AssessmentResultDetail]] = None
    model_config = ConfigDict(from_attributes=True)

# --- Project Schemas ---
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    status: Optional[str] = "In Progress"

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    status: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    status: str
    model_config = ConfigDict(from_attributes=True)

# --- Certification Schemas ---
class CertificationCreate(BaseModel):
    title: str
    issuing_organization: str
    completion_date: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationUpdate(BaseModel):
    title: Optional[str] = None
    issuing_organization: Optional[str] = None
    completion_date: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    issuing_organization: str
    completion_date: Optional[str] = None
    credential_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# --- Career Goal Schemas ---
class CareerGoalCreate(BaseModel):
    target_role: str
    preferred_domain: Optional[str] = None

class CareerGoalOut(BaseModel):
    id: int
    user_id: int
    target_role: str
    preferred_domain: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RoleInfoOut(BaseModel):
    role_name: str
    description: str
    required_skills: List[Dict[str, Any]]

# --- Skill Gap Schemas ---
class SkillGapItem(BaseModel):
    skill_name: str
    category: str
    required_level: str
    current_level: Optional[str] = None
    assessment_score: Optional[float] = None
    priority: str
    status: str  # Strong, Needs Improvement, Missing
    gap_reason: str

class SkillGapResponse(BaseModel):
    target_role: str
    match_percentage: float
    total_required_skills: int
    strong_skills: List[SkillGapItem]
    needs_improvement_skills: List[SkillGapItem]
    missing_skills: List[SkillGapItem]
    ai_summary: str
    ai_is_fallback: bool
    created_at: datetime

# --- Learning Roadmap Schemas ---
class RoadmapTaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    phase: str
    priority: str
    difficulty: str
    estimated_duration: str
    learning_objective: Optional[str] = None
    recommended_resources: Optional[str] = None
    due_date: Optional[str] = None
    status: str
    model_config = ConfigDict(from_attributes=True)

class RoadmapTaskUpdate(BaseModel):
    status: Optional[str] = None
    due_date: Optional[str] = None

class LearningRoadmapOut(BaseModel):
    id: int
    user_id: int
    title: str
    target_role: str
    created_at: datetime
    tasks: List[RoadmapTaskOut]
    model_config = ConfigDict(from_attributes=True)

# --- Project Recommendation Schemas ---
class RecommendedProjectOut(BaseModel):
    id: str
    title: str
    description: str
    problem_statement: str
    technologies: List[str]
    features: List[str]
    difficulty: str
    skills_developed: List[str]
    implementation_steps: List[str]
    expected_outcome: str

class AdoptProjectRequest(BaseModel):
    title: str
    description: str
    technologies: str

# --- Interview Schemas ---
class InterviewQuestionItem(BaseModel):
    id: str
    question: str
    category: str
    difficulty: str
    hint: Optional[str] = None
    sample_answer_outline: Optional[str] = None

class InterviewGenerateRequest(BaseModel):
    target_role: str
    category: str
    difficulty: Optional[str] = "Intermediate"

class InterviewEvaluateRequest(BaseModel):
    target_role: str
    category: str
    question: str
    student_answer: str

class InterviewEvaluateResponse(BaseModel):
    session_id: int
    question: str
    student_answer: str
    rating: float  # 0 to 100
    strengths: str
    missing_concepts: str
    feedback: str
    model_answer: str
    is_ai_generated: bool

# --- Dashboard & Activity Schemas ---
class ActivityLogOut(BaseModel):
    id: int
    activity_type: str
    description: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DashboardSummaryOut(BaseModel):
    user_name: str
    profile_completion_pct: float
    target_role: Optional[str] = None
    readiness_score: float  # calculated from real data
    total_skills_count: int
    verified_skills_count: int
    skill_gap_summary: Dict[str, int]
    roadmap_progress_pct: float
    active_projects_count: int
    completed_projects_count: int
    completed_assessments_count: int
    average_assessment_score: float
    recommended_next_action: Dict[str, str]
    category_proficiency: List[Dict[str, Any]]
    recent_activities: List[ActivityLogOut]

# --- Resource Schemas ---
class LearningResourceOut(BaseModel):
    id: int
    title: str
    skill_category: str
    resource_type: str
    url: str
    difficulty: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
