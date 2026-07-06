# app.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import json
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import Request
from fastapi.responses import HTMLResponse

from analyzer import analyze_submission
from skill_matcher import suggest_skills
from question_generator import generate_questions
from evaluation import generate_evaluation
from viva import start_session, add_event
from proctor import calculate_integrity_report

app = FastAPI(
    title="Project Submission AI Analyzer",
    description="AI-powered project analyzer and viva assistant",
    version="1.0"
)
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/student", response_class=HTMLResponse)
async def student(request: Request):
    html = (TEMPLATE_DIR / "student.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/mentor", response_class=HTMLResponse)
async def mentor(request: Request):
    html = (TEMPLATE_DIR / "mentor.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    html = (TEMPLATE_DIR / "report.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)





@app.post("/analyze-submission")
async def analyze_submission_api(
    project_title: str = Form(...),
    project_outcomes: str = Form(None),
    outcomes: str = Form(None),
    zip_file: UploadFile = File(...),
    student_name: str = Form(None),
    project_description: str = Form(None),
    skill_catalog: str = Form(None)
):
    """
    Analyze the uploaded student project.
    """

    try:

        # Normalize incoming outcome field names
        if not project_outcomes and outcomes:
            project_outcomes = outcomes

        # Analyze uploaded ZIP
        project_data = analyze_submission(zip_file)

        # Detect skills (allow catalog override from UI)
        skills_override = None
        if skill_catalog:
            try:
                import json as _json

                skills_override = _json.loads(skill_catalog)
            except Exception:
                skills_override = None

        suggested_skills = suggest_skills(project_data, skills_override=skills_override)

        # Generate interview questions
        questions = generate_questions(
            project_data,
            suggested_skills
        )

        # Generate evaluation report
        evaluation = generate_evaluation(
            project_title,
            project_outcomes,
            project_data,
            suggested_skills,
            questions
        )

        # Map response keys to those expected by the frontend UI
        response = {
            "project_title": project_title,
            "student_name": student_name,
            "project_description": project_description,
            "detected_skills": suggested_skills,
            "project_summary": evaluation.get("summary", evaluation),
            "outcome_evaluation": evaluation.get("summary", {}).get("outcome_evaluation", []),
            "questions": questions,
            "interview_questions": questions,
            "integrity_report": {},
            "tech_stack": project_data.get("tech_stack", []),
            "important_files": project_data.get("important_files", []),
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "ai_model": "Gemini"
            }
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/viva-session/start")
def start_viva_session():
    """
    Starts a new viva session.
    """

    try:
        return start_session()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/viva-session/event")
async def record_event(
    session_id: str = Form(...),
    event_type: str = Form(...),
    timestamp: str = Form(...),
    duration_ms: int = Form(0),
    confidence: float = Form(1.0)
):
    """
    Records a proctoring event.
    """

    try:

        event = {
            "event_type": event_type,
            "timestamp": timestamp,
            "duration_ms": duration_ms,
            "confidence": confidence
        }

        return add_event(
            session_id=session_id,
            event=event
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/viva-session/end")
async def end_viva_session(
    session_id: str = Form(...)
):
    """
    Ends the viva session and generates the final proctoring report.
    """

    try:

        report = calculate_integrity_report(session_id)

        return JSONResponse(
            content=report
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )