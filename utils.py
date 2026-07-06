# utils.py

import os
import zipfile
import shutil


def safe_extract_zip(zip_path: str, extract_to: str):
    """
    Safely extracts a ZIP file while preventing path traversal attacks.
    """

    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)

    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        for member in zip_ref.namelist():

            member_path = os.path.abspath(
                os.path.join(extract_to, member)
            )

            if not member_path.startswith(os.path.abspath(extract_to)):
                raise Exception("Unsafe ZIP detected!")

        zip_ref.extractall(extract_to)


def get_file_tree(folder_path: str):
    """
    Returns all file paths inside the extracted project.
    """

    file_tree = []

    for root, dirs, files in os.walk(folder_path):

        for file in files:
            relative_path = os.path.relpath(
                os.path.join(root, file),
                folder_path
            )
            file_tree.append(relative_path)

    return file_tree


def read_python_files(folder_path: str):
    """
    Reads all Python files and combines them into one string.
    """

    combined_code = ""

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.endswith(".py"):

                file_path = os.path.join(root, file)

                try:

                    with open(file_path, "r", encoding="utf-8") as f:

                        combined_code += (
                            f"\n\n# FILE: {file}\n"
                        )

                        combined_code += f.read()

                except Exception:
                    pass

    return combined_code


def detect_dependencies(folder_path: str):
    """
    Reads requirements.txt if present.
    """

    requirements = os.path.join(
        folder_path,
        "requirements.txt"
    )

    if os.path.exists(requirements):

        with open(requirements, "r", encoding="utf-8") as f:
            return f.read()

    return ""


def get_code_statistics(folder_path: str):
    """
    Returns basic statistics about the project.
    """

    total_files = 0
    python_files = 0

    for root, dirs, files in os.walk(folder_path):

        total_files += len(files)

        for file in files:

            if file.endswith(".py"):
                python_files += 1

    return {
        "total_files": total_files,
        "python_files": python_files
    }