import pytest
from backend.src.core.anomalies import detect_anomalies

def test_detect_anomalies_excess_weight_gain():
    """
    Tests that an anomaly is detected for excess interdialytic weight gain.
    """
    session = {
        "pre_weight": 70.0,
        "post_weight": 68.0
    }
    anomalies = detect_anomalies(session)
    assert "Excess interdialytic weight gain" in anomalies

def test_detect_anomalies_no_excess_weight_gain():
    """
    Tests that no anomaly is detected for normal weight gain.
    """
    session = {
        "pre_weight": 70.0,
        "post_weight": 69.0
    }
    anomalies = detect_anomalies(session)
    assert "Excess interdialytic weight gain" not in anomalies
