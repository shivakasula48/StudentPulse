from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db
from app.services.ai_service import ai_service
from app.core.config import settings

router = APIRouter(tags=["System"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint checking database connectivity and AI service readiness."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
        "ai_engine": {
            "service": "Google Gemini",
            "model": settings.GEMINI_MODEL,
            "connected": ai_service.is_ai_available(),
            "mode": "Live AI" if ai_service.is_ai_available() else "Rule-based Fallback Engine Active"
        }
    }
