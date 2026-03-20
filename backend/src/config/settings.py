from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Define your application settings here.
    # Pydantic-settings will automatically load these from environment variables
    # or a .env file.
    app_name: str = "Dialysis Dashboard API"
    debug_mode: bool = False # Controls FastAPI debug mode
    logging_level: str = "INFO" # e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" 

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "dialysis_dashboard_db"

    # Anomaly Detection Thresholds (example values, should be configured)
    # These values should be justified in the README's "Clinical Assumptions & Thresholds" section.
    min_weight_loss_kg: float = 2.0 # Minimum weight loss during a session to avoid "excess interdialytic weight gain" anomaly
    high_post_dialysis_systolic_bp_threshold: int = 140 # mmHg
    min_session_duration_minutes: int = 180 # 3 hours
    max_session_duration_minutes: int = 270 # 4.5 hours


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")