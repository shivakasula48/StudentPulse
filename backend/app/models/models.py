import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    Float, Boolean, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skills = relationship("StudentSkill", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="user", cascade="all, delete-orphan")
    career_goals = relationship("CareerGoal", back_populates="user", cascade="all, delete-orphan")
    gap_analyses = relationship("SkillGapAnalysis", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="user", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    college = Column(String(200), nullable=True)
    degree = Column(String(100), nullable=True)
    semester = Column(String(50), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    career_interest = Column(String(150), nullable=True)

    user = relationship("User", back_populates="profile")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False)  # Programming, Web, Database, Framework, Tool, Soft Skill, AI/ML
    description = Column(Text, nullable=True)

    student_skills = relationship("StudentSkill", back_populates="skill")
    role_requirements = relationship("RoleSkillRequirement", back_populates="skill")


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    self_reported_level = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    assessment_score = Column(Float, nullable=True)  # Verified score from tests (0-100)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    question_text = Column(Text, nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_option = Column(String(10), nullable=False)  # A, B, C, or D
    explanation = Column(Text, nullable=True)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)
    total_questions = Column(Integer, default=0)
    score = Column(Float, default=0.0)  # Percentage score 0-100
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    answers = relationship("AssessmentAnswer", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id"), nullable=False)
    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, default=False)

    assessment = relationship("Assessment", back_populates="answers")
    question = relationship("AssessmentQuestion")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(String(255), nullable=True)  # Comma-separated or string
    github_url = Column(String(255), nullable=True)
    live_url = Column(String(255), nullable=True)
    status = Column(String(50), default="In Progress")  # Planned, In Progress, Completed

    user = relationship("User", back_populates="projects")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    issuing_organization = Column(String(200), nullable=False)
    completion_date = Column(String(50), nullable=True)
    credential_url = Column(String(255), nullable=True)

    user = relationship("User", back_populates="certifications")


class CareerGoal(Base):
    __tablename__ = "career_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_role = Column(String(100), nullable=False)
    preferred_domain = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="career_goals")
    analyses = relationship("SkillGapAnalysis", back_populates="career_goal", cascade="all, delete-orphan")


class RoleSkillRequirement(Base):
    __tablename__ = "role_skill_requirements"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), index=True, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    required_level = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    priority = Column(String(50), default="High")  # Critical, High, Medium, Low

    skill = relationship("Skill", back_populates="role_requirements")


class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_goal_id = Column(Integer, ForeignKey("career_goals.id", ondelete="SET NULL"), nullable=True)
    analysis_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="gap_analyses")
    career_goal = relationship("CareerGoal", back_populates="analyses")


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    target_role = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("learning_roadmaps.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    phase = Column(String(100), default="Phase 1: Foundations")
    priority = Column(String(50), default="High")  # Critical, High, Medium, Low
    difficulty = Column(String(50), default="Intermediate")
    estimated_duration = Column(String(50), default="1 week")
    learning_objective = Column(Text, nullable=True)
    recommended_resources = Column(Text, nullable=True)
    due_date = Column(String(50), nullable=True)
    status = Column(String(50), default="Pending")  # Pending, In Progress, Completed

    roadmap = relationship("LearningRoadmap", back_populates="tasks")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)
    target_role = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="interview_sessions")
    responses = relationship("InterviewResponse", back_populates="session", cascade="all, delete-orphan")


class InterviewResponse(Base):
    __tablename__ = "interview_responses"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    missing_concepts = Column(Text, nullable=True)
    model_answer = Column(Text, nullable=True)
    score = Column(Float, nullable=True)  # Indicative rating 0-100
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("InterviewSession", back_populates="responses")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # profile, skill, assessment, roadmap, interview, project
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="activity_logs")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    skill_category = Column(String(100), nullable=False)
    resource_type = Column(String(50), default="Documentation")  # Documentation, Tutorials, Online courses, Coding practice, Video learning, Interview prep
    url = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Beginner")
    description = Column(Text, nullable=True)
