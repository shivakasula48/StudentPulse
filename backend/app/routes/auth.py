from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.database.session import get_db
from app.models.models import User, StudentProfile, CareerGoal, ActivityLog
from app.schemas.schemas import UserCreate, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Create user
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.flush()

    # Create profile
    profile = StudentProfile(
        user_id=user.id,
        college=user_in.college,
        degree=user_in.degree,
        semester=user_in.semester,
        career_interest=user_in.career_interest
    )
    db.add(profile)

    # Set default career goal if provided
    if user_in.career_interest:
        goal = CareerGoal(
            user_id=user.id,
            target_role=user_in.career_interest,
            created_at=datetime.utcnow()
        )
        db.add(goal)

    # Log activity
    log = ActivityLog(
        user_id=user.id,
        activity_type="profile",
        description="Created StudentPulse AI account and profile",
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    goal = db.query(CareerGoal).filter(CareerGoal.user_id == current_user.id).order_by(CareerGoal.created_at.desc()).first()

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "college": profile.college if profile else None,
        "degree": profile.degree if profile else None,
        "semester": profile.semester if profile else None,
        "graduation_year": profile.graduation_year if profile else None,
        "career_interest": profile.career_interest if profile else None,
        "target_role": goal.target_role if goal else (profile.career_interest if profile else None),
        "created_at": current_user.created_at
    }
