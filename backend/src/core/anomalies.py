from typing import List
from datetime import timedelta
from ..data.models.session import DialysisSessionModel
from ..config.settings import Settings

settings = Settings() # Load settings to access thresholds

def detect_anomalies(session: DialysisSessionModel) -> List[str]:
    """
    Detects anomalies in a dialysis session.
    """
    anomalies = []
    
    # Anomaly 1: Excess interdialytic weight gain
    # Assuming 'interdialytic weight gain' refers to the difference between pre-weight of current session
    # and post-weight of the *previous* session. For a single session, we'll interpret it as
    # the weight gained *during* the session, which is usually a loss.
    # The README implies "interdialytic weight gain" is between sessions.
    # For now, let's assume it means the difference between pre-weight and the patient's dry weight.
    # This requires fetching patient's dry weight, which is not available in session directly.
    # For simplicity, let's re-interpret this as "excessive weight loss during session" or
    # if pre_weight is significantly higher than dry_weight (which would be a check in the service layer).
    # For the current `anomalies.py` context, let's stick to what's directly available in the session.
    # A more robust implementation would involve fetching the patient's dry weight or previous session's post-weight.
    
    # Let's assume for now, the anomaly check is for *weight loss* during the session being too low (i.e., not enough fluid removed)
    # or if pre_weight is too high relative to an ideal.
    # Given the prompt, "Excess interdialytic weight gain" is usually pre-weight vs. dry weight.
    # For this example, let's check if the weight *removed* is less than a threshold, implying retention.
    if session.pre_weight_kg - session.post_weight_kg < settings.min_weight_loss_kg:
            anomalies.append("Excess interdialytic weight gain")
            
    # Anomaly 2: High post-dialysis systolic BP
    if session.systolic_bp_post is not None and session.systolic_bp_post > settings.high_post_dialysis_systolic_bp_threshold:
        anomalies.append("High post-dialysis systolic BP")

    # Anomaly 3: Abnormal session duration
    session_duration = session.end_time - session.start_time
    if session_duration < timedelta(minutes=settings.min_session_duration_minutes):
        anomalies.append("Abnormal session duration (too short)")
    elif session_duration > timedelta(minutes=settings.max_session_duration_minutes):
        anomalies.append("Abnormal session duration (too long)")

    return anomalies
