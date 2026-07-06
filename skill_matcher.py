import json


def load_skill_catalog():

    with open("skills.json", "r", encoding="utf-8") as f:
        return json.load(f)


def suggest_skills(project_data, skills_override=None):

    catalog = skills_override or load_skill_catalog()

    detected = []

    file_tree = " ".join(project_data.get("file_tree", [])).lower()

    dependencies = str(project_data.get("dependencies", "")).lower()

    tech_stack = " ".join(project_data.get("tech_stack", [])).lower()

    search_text = file_tree + " " + dependencies + " " + tech_stack


    KEYWORDS = {

        "Python":[
            ".py",
            "python"
        ],

        "FastAPI":[
            "fastapi"
        ],

        "Flask":[
            "flask"
        ],

        "OpenCV":[
            "opencv",
            "cv2"
        ],

        "NumPy":[
            "numpy"
        ],

        "Pandas":[
            "pandas"
        ],

        "TensorFlow":[
            "tensorflow"
        ],

        "Keras":[
            "keras"
        ],

        "Machine Learning":[
            "sklearn",
            "machine learning",
            "scikit"
        ],

        "Deep Learning":[
            "deep learning",
            "tensorflow",
            "keras",
            "torch"
        ],

        "REST API":[
            "api",
            "requests",
            "fastapi",
            "flask"
        ],

        "SQLite":[
            "sqlite"
        ],

        "PostgreSQL":[
            "postgresql",
            "psycopg"
        ],

        "Git":[
            ".git",
            "git"
        ],

        "HTML":[
            ".html"
        ],

        "CSS":[
            ".css"
        ],

        "JavaScript":[
            ".js",
            "javascript"
        ]

    }


    for skill in catalog:

        name = skill["skill_name"]

        words = KEYWORDS.get(name, [])

        for word in words:

            if word in search_text:

                detected.append({

                    "skill_id":skill["skill_id"],

                    "skill_name":name,

                    "confidence":0.95,

                    "rationale":"Detected from project files."

                })

                break


    if len(detected)==0:

        detected.append({

            "skill_id":"uuid-1",

            "skill_name":"Python",

            "confidence":0.60,

            "rationale":"Default skill."

        })


    return detected