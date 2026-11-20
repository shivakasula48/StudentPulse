import json
import logging
from typing import Dict, Any, List, Tuple
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-4-hydrogen"
        self.client = None
        
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Gemini client initialized with model {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}. Falling back to rule-based engine.")
                self.client = None

    def is_ai_available(self) -> bool:
        return self.client is not None

    def explain_skill_gap(
        self,
        target_role: str,
        student_name: str,
        match_percentage: float,
        strong_skills: List[str],
        needs_improvement: List[str],
        missing_skills: List[str]
    ) -> Tuple[str, bool]:
        """
        Generates an evidence-based explanation of the student's skill gap.
        Returns: (explanation_text, is_fallback)
        """
        if not self.is_ai_available():
            return self._fallback_skill_gap_explanation(
                target_role, student_name, match_percentage,
                strong_skills, needs_improvement, missing_skills
            ), True

        prompt = f"""
You are a Senior Technical Career Architect evaluating a student for the role of {target_role}.
Candidate Name: {student_name}
Role Alignment Match: {match_percentage:.1f}%

Evidence Breakdown:
- Strong Skills: {', '.join(strong_skills) if strong_skills else 'None verified yet'}
- Skills Needing Improvement / Verification: {', '.join(needs_improvement) if needs_improvement else 'None'}
- Missing Critical Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Instructions:
- Provide a concise, professional 3-paragraph career readiness assessment following the EVIDENCE → INSIGHT → ACTION methodology.
- Do NOT fabricate qualifications or make unrealistic placement guarantees.
- Explain clearly WHY missing skills matter for industry-standard {target_role} roles.
- Emphasize high-priority action items.
Keep it strictly under 250 words.
"""
        try:
            response = self.client.interactions.create(
                model=self.model_name,
                input=prompt
            )
            return response.output_text.strip(), False
        except Exception as e:
            logger.error(f"Gemini API error during skill gap explanation: {e}")
            return self._fallback_skill_gap_explanation(
                target_role, student_name, match_percentage,
                strong_skills, needs_improvement, missing_skills
            ), True

    def _fallback_skill_gap_explanation(
        self,
        target_role: str,
        student_name: str,
        match_percentage: float,
        strong_skills: List[str],
        needs_improvement: List[str],
        missing_skills: List[str]
    ) -> str:
        """Deterministic rule-based explanation based on verified evidence."""
        strong_text = f"You have established demonstrable competency in {', '.join(strong_skills)}." if strong_skills else "You have not yet validated core skills for this role."
        improve_text = f"However, skills such as {', '.join(needs_improvement)} require either deeper proficiency or formal assessment verification." if needs_improvement else ""
        missing_text = f"To meet industry benchmarks for {target_role}, the primary blockers are missing prerequisites: {', '.join(missing_skills)}." if missing_skills else "You currently have baseline coverage across all required role competencies."
        
        return (
            f"Career Readiness Assessment for {target_role} ({match_percentage:.1f}% Match):\n\n"
            f"{strong_text} {improve_text}\n\n"
            f"{missing_text}\n\n"
            f"Recommended Immediate Action: Focus on high-priority missing skills by following your customized learning roadmap and implementing hands-on project deliverables."
        )

    def evaluate_interview_response(
        self,
        target_role: str,
        category: str,
        question: str,
        student_answer: str,
        expected_keywords: List[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a student's answer to an interview question.
        Returns rubric scores, strengths, missing concepts, feedback, and model answer.
        """
        if not self.is_ai_available():
            return self._fallback_interview_evaluation(
                target_role, category, question, student_answer, expected_keywords
            )

        prompt = f"""
You are an expert technical interviewer evaluating an entry-to-mid level candidate for the role of {target_role}.
Category: {category}
Question: {question}
Candidate's Answer: {student_answer}

Evaluate the response objectively using this JSON format:
{{
  "rating": <integer between 0 and 100>,
  "strengths": "<What the student articulated well>",
  "missing_concepts": "<Key technical nuances, edge cases, or standard terminology missed>",
  "feedback": "<Constructive 2-3 sentence coaching feedback>",
  "model_answer": "<Clean, professional standard industry answer under 150 words>"
}}
Return ONLY valid JSON.
"""
        try:
            response = self.client.interactions.create(
                model=self.model_name,
                input=prompt
            )
            # Parse JSON
            raw_text = response.output_text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            data = json.loads(raw_text.strip())
            data["is_ai_generated"] = True
            return data
        except Exception as e:
            logger.error(f"Gemini API error during interview evaluation: {e}")
            return self._fallback_interview_evaluation(
                target_role, category, question, student_answer, expected_keywords
            )

    def _fallback_interview_evaluation(
        self,
        target_role: str,
        category: str,
        question: str,
        student_answer: str,
        expected_keywords: List[str] = None
    ) -> Dict[str, Any]:
        """Transparent, rule-based rubric evaluation."""
        ans = student_answer.strip().lower()
        word_count = len(ans.split())
        
        # Heuristic scoring based on length, depth, structure
        base_score = 40.0
        if word_count > 15:
            base_score += 20.0
        if word_count > 35:
            base_score += 15.0
        if word_count > 60:
            base_score += 10.0

        # Check for technical clarity
        strengths = []
        if word_count > 25:
            strengths.append("Provided a structured response with clear progression of thought.")
        if any(term in ans for term in ["because", "due to", "trade-off", "example", "complexity", "interface", "performance"]):
            strengths.append("Demonstrated analytical reasoning and recognized technical causality.")
            base_score += 10.0
        if not strengths:
            strengths.append("Attempted the question directly.")

        missing = []
        if word_count < 30:
            missing.append("Explanation is brief; industry interviews expect concrete examples, architecture context, and boundary cases.")
        if "trade-off" not in ans and "performance" not in ans:
            missing.append("Discussion of performance implications, time/space complexity, or memory overhead.")

        score = min(92.0, max(30.0, base_score))

        return {
            "rating": score,
            "strengths": " ".join(strengths),
            "missing_concepts": " ".join(missing) if missing else "Include real-world production trade-offs and edge case handling.",
            "feedback": f"Good effort. For {target_role} interviews, articulate the architectural reason behind each concept and cite practical production trade-offs.",
            "model_answer": f"In a professional interview for {target_role}, begin with a precise definition, explain the internal mechanism, compare trade-offs against alternatives, and conclude with a production use-case.",
            "is_ai_generated": False
        }

ai_service = AIService()
