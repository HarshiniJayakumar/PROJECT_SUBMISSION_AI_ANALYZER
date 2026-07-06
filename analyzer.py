# analyzer.py

import os
import shutil
import tempfile
from pathlib import Path

from utils import (
    safe_extract_zip,
    get_file_tree,
    read_python_files,
    detect_dependencies,
    get_code_statistics
)

EXTENSION_TECH = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".ipynb": "Jupyter Notebook",
    ".md": "Markdown",
    ".sql": "SQL",
    ".java": "Java",
    ".cs": "C#"
}

FRAMEWORK_KEYWORDS = {
    "flask": "Flask",
    "fastapi": "FastAPI",
    "django": "Django",
    "streamlit": "Streamlit",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "tensorflow": "TensorFlow",
    "torch": "PyTorch",
    "opencv": "OpenCV",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "sqlalchemy": "SQLAlchemy",
    "react": "React",
    "vue": "Vue.js",
    "angular": "Angular",
    "docker": "Docker"
}

PRIORITY_FILES = [
    "app.py",
    "main.py",
    "server.py",
    "run.py",
    "models.py",
    "views.py",
    "requirements.txt",
    "Dockerfile"
]


def detect_tech_stack(file_tree, dependencies):
    tech = set()

    for file_name in file_tree:
        ext = Path(file_name).suffix.lower()
        if ext in EXTENSION_TECH:
            tech.add(EXTENSION_TECH[ext])

    lower_deps = dependencies.lower() if isinstance(dependencies, str) else ""
    lower_tree = " ".join(file_tree).lower()

    for keyword, label in FRAMEWORK_KEYWORDS.items():
        if keyword in lower_deps or keyword in lower_tree:
            tech.add(label)

    if any(path.lower().endswith("requirements.txt") for path in file_tree):
        tech.add("Python")

    return sorted(tech)


def find_important_files(file_tree):
    important = [path for path in PRIORITY_FILES if path in file_tree]

    if not important:
        python_files = [f for f in file_tree if f.endswith(".py")]
        important = python_files[:3]

    if not important:
        important = file_tree[:3]

    return important



def analyze_submission(zip_file):
    """
    Extracts and analyzes a student project ZIP file.
    Returns all extracted project information.
    """

    # Create temporary working directory
    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(temp_dir, zip_file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    extract_path = os.path.join(temp_dir, "project")

    # Safe extraction
    safe_extract_zip(zip_path, extract_path)

    # Collect project information
    file_tree = get_file_tree(extract_path)

    code = read_python_files(extract_path)

    dependencies = detect_dependencies(extract_path)

    statistics = get_code_statistics(extract_path)
    tech_stack = detect_tech_stack(file_tree, dependencies)
    important_files = find_important_files(file_tree)

    return {
        "extract_path": extract_path,
        "file_tree": file_tree,
        "code": code,
        "dependencies": dependencies,
        "statistics": statistics,
        "tech_stack": tech_stack,
        "important_files": important_files
    }