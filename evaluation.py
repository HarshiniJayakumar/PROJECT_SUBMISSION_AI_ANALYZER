# evaluation.py

import json
from config import model


def clean_json_response(text):
    """
    Removes markdown formatting from Gemini responses.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")

    if text.startswith("```"):
        text = text.replace("```", "")

    text = text.replace("```", "").strip()

    return text


def generate_evaluation(project_title,
                        project_outcomes,
                        project_data,
                        suggested_skills,
                        questions):
    """
    Generates the evaluation report using Gemini.
    """

    prompt = f"""
You are an expert software project evaluator.

Project Title:
{project_title}

Project Outcomes:
{project_outcomes}

Suggested Skills:
{json.dumps(suggested_skills, indent=4)}

Interview Questions:
{json.dumps(questions, indent=4)}

Tech Stack:
{json.dumps(project_data.get('tech_stack', []), indent=4)}

Important Files:
{json.dumps(project_data.get('important_files', []), indent=4)}

Project File Tree:
{project_data['file_tree']}

Dependencies:
{project_data['dependencies']}

Project Statistics:
{project_data['statistics']}

Project Code:
{project_data['code'][:12000]}

Create a detailed evaluation report suitable for a hackathon-style project review.
Include:
- a summary explaining what the student built,
- whether stated outcomes are correct and met,
- the key technologies and important files,
- what is strong and what is missing,
- a final verdict and recommended next steps.

Also identify the most important files for the reviewer to inspect, especially when a skill is mentioned that may not be fully supported by the code.

Return ONLY valid JSON.

Format:

{{
  "skills": {json.dumps(questions, indent=4)},
  "summary":
  {{
      "overall_alignment":"strong",
      "alignment_score":0.90,
      "narrative":"",
      "outcome_evaluation":[
          {{
              "outcome":"",
              "status":"",
              "evidence":"",
              "gap":""
          }}
      ],
      "strengths":[
          ""
      ],
      "gaps":[
          ""
      ],
      "verdict":"",
      "next_steps":""
  }}
}}

Do not use markdown.

Return JSON only.
"""

    try:
        response = model.generate_content(prompt)
        cleaned = clean_json_response(response.text)
        evaluation = json.loads(cleaned)

        if not isinstance(evaluation, dict):
            raise ValueError("Invalid evaluation format")

        return evaluation
    except Exception as e:
        return {
            "skills": questions,
            "summary": {
                "overall_alignment": "unknown",
                "alignment_score": 0.0,
                "narrative": (
                    "Automated evaluation is temporarily unavailable due to AI service quota or an internal error. "
                    "Please retry after some time."
                ),
                "outcome_evaluation": [],
                "strengths": [
                    "Detected skills: " + ", ".join([
                        skill.get("skill_name", str(skill)) if isinstance(skill, dict) else str(skill)
                        for skill in suggested_skills
                    ])
                ],
                "gaps": [
                    "Evaluation service temporarily unavailable."
                ],
                "verdict": "Evaluation not available",
                "next_steps": "Retry analysis later or upgrade your Gemini quota."
            }
        }