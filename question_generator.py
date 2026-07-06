# question_generator.py

import json
import re
from config import model


# -----------------------------------------
# Clean Gemini Response
# -----------------------------------------

def clean_json_response(text):

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")

    if text.startswith("```"):
        text = text.replace("```", "")

    return text.replace("```", "").strip()


def extract_json(text):

    cleaned = clean_json_response(text)

    match = re.search(r"(\[[\s\S]*\])", cleaned)

    if match:
        return match.group(1)

    return cleaned


# -----------------------------------------
# Fallback Questions
# -----------------------------------------

def fallback_questions(skills):

    questions = []

    for skill in skills:

        if isinstance(skill, dict):
            skill = skill.get("skill_name", "General")

        # Technical Question
        questions.append(
            f"[{skill}] Technical: Explain the core concepts of {skill}."
        )

        # Contextual Question
        questions.append(
            f"[{skill}] Contextual: How did you use {skill} in your project?"
        )

    return questions


# -----------------------------------------
# Generate Questions
# -----------------------------------------

def generate_questions(project_data, suggested_skills):

    # Convert skills into plain list

    skills = []

    for skill in suggested_skills:

        if isinstance(skill, dict):

            skills.append(skill.get("skill_name", "General"))

        else:

            skills.append(str(skill))

    prompt = f"""
You are an expert software engineering interviewer.

Detected Skills:

{skills}

Generate EXACTLY TWO questions for EACH skill.

Question 1:
Technical

Question 2:
Contextual (based on the student's project)

Return ONLY JSON.

Example

[
"Python Technical: Explain decorators.",

"Python Contextual: Where did you use Python in this project?",

"Flask Technical: Explain Flask routing.",

"Flask Contextual: Why did you choose Flask for this project?"
]
"""

    try:

        response = model.generate_content(prompt)

        extracted = extract_json(response.text)

        questions = json.loads(extracted)

        if not isinstance(questions, list):

            raise Exception()

        return questions

    except Exception:

        return fallback_questions(skills)