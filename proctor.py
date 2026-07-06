# proctor.py

from viva import get_session


def calculate_integrity_report(session_id):
    """
    Generates the final proctoring report.
    """

    session = get_session(session_id)

    events = session["events"]

    integrity_score = 1.0

    flag_summary = {
        "gaze_off_screen": 0,
        "tab_switched": 0,
        "face_not_detected": 0,
        "multiple_faces_detected": 0,
        "fullscreen_exited": 0,
        "paste_attempted": 0,
        "screenshot_detected": 0
    }

    flags = []

    for event in events:

        event_type = event["event_type"]

        if event_type in flag_summary:
            flag_summary[event_type] += 1

        severity = "low"

        if event_type == "multiple_faces_detected":
            severity = "high"
            integrity_score -= 0.20

        elif event_type == "tab_switched":
            severity = "medium"
            integrity_score -= 0.10

        elif event_type == "gaze_off_screen":
            severity = "low"
            integrity_score -= 0.05

        elif event_type == "face_not_detected":
            severity = "medium"
            integrity_score -= 0.10

        elif event_type == "fullscreen_exited":
            severity = "medium"
            integrity_score -= 0.10

        elif event_type == "paste_attempted":
            severity = "high"
            integrity_score -= 0.15

        elif event_type == "screenshot_detected":
            severity = "high"
            integrity_score -= 0.15

        if event_type in flag_summary:

            flags.append({
                "type": event_type,
                "timestamp": event["timestamp"],
                "duration_ms": event.get("duration_ms", 0),
                "severity": severity
            })

    integrity_score = max(0.0, round(integrity_score, 2))

    if integrity_score >= 0.80:
        risk_level = "low"
    elif integrity_score >= 0.50:
        risk_level = "medium"
    else:
        risk_level = "high"

    narrative = (
        "The viva session was monitored successfully. "
        "Integrity events were analyzed to generate the final report."
    )

    return {
        "session_id": session_id,
        "id_check": session["id_check"],
        "integrity_score": integrity_score,
        "risk_level": risk_level,
        "flag_summary": flag_summary,
        "flags": flags,
        "narrative": narrative
    }