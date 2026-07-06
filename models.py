# models.py

from pydantic import BaseModel
from typing import List, Optional


class SkillSuggestion(BaseModel):
    skill_id: str
    skill_name: str
    confidence: float
    rationale: str


class InterviewQuestion(BaseModel):
    conceptual: str
    codebase_specific: str


class SkillEvaluation(BaseModel):
    skill_name: str
    questions: List[InterviewQuestion]


class OutcomeEvaluation(BaseModel):
    outcome: str
    status: str
    evidence: str
    gap: Optional[str] = ""


class Summary(BaseModel):
    overall_alignment: str
    alignment_score: float
    narrative: str
    outcome_evaluation: List[OutcomeEvaluation]
    strengths: List[str]
    gaps: List[str]


class EvaluationReport(BaseModel):
    skills: List[SkillEvaluation]
    summary: Summary


class IntegrityFlag(BaseModel):
    type: str
    timestamp: str
    duration_ms: int
    severity: str


class ProctoringReport(BaseModel):
    session_id: str
    id_check: str
    integrity_score: float
    risk_level: str
    flag_summary: dict
    flags: List[IntegrityFlag]
    narrative: str


class FinalResponse(BaseModel):
    project_title: str
    suggested_skills: List[SkillSuggestion]
    evaluation_report: EvaluationReport
    proctoring_report: ProctoringReport
    metadata: dict