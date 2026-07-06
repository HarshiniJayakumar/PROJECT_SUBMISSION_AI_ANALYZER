# viva.py

import uuid
from datetime import datetime

# In-memory storage for active viva sessions
viva_sessions = {}


def start_session():
    """
    Creates a new viva session.
    """

    session_id = str(uuid.uuid4())

    viva_sessions[session_id] = {
        "session_id": session_id,
        "start_time": datetime.utcnow().isoformat(),
        "events": [],
        "id_check": "pending"
    }

    return {
        "session_id": session_id,
        "message": "Viva session started successfully."
    }


def add_event(session_id, event):
    """
    Adds a proctoring event to an existing session.
    """

    if session_id not in viva_sessions:
        raise Exception("Invalid session ID")

    viva_sessions[session_id]["events"].append(event)

    if event["event_type"] == "id_verified":
        viva_sessions[session_id]["id_check"] = "id_verified"

    elif event["event_type"] == "id_failed":
        viva_sessions[session_id]["id_check"] = "id_failed"

    return {
        "message": "Event recorded successfully."
    }


def get_session(session_id):
    """
    Returns the stored session.
    """

    if session_id not in viva_sessions:
        raise Exception("Invalid session ID")

    return viva_sessions[session_id]