import logging
from datetime import datetime
from typing import List, Optional

from .schemas import DialysisSessionCreate, DialysisSessionResponse
from ...data.models.session import DialysisSessionModel
from ...data.repositories.session_repo import DialysisSessionRepository
from ...core.anomalies import detect_anomalies

logger = logging.getLogger(__name__)

class DialysisSessionService:
    """
    Handles business logic for dialysis session operations.
    Interacts with DialysisSessionRepository for data persistence and Anomaly Detection.
    """
    def __init__(self, session_repo: DialysisSessionRepository):
        self.session_repo = session_repo

    async def create_session(self, session_data: DialysisSessionCreate) -> DialysisSessionResponse:
        """Records a new dialysis session and detects anomalies."""
        # Convert Pydantic input schema to internal data model
        session_model = DialysisSessionModel(**session_data.model_dump())
        now = datetime.utcnow()
        session_model.created_at = now
        session_model.updated_at = now

        # Detect anomalies
        session_model.anomalies = detect_anomalies(session_model)
        if session_model.anomalies:
            logger.warning(f"Anomalies detected for new session for patient {session_model.patient_id}: {session_model.anomalies}")

        # Persist to database via repository
        created_session = await self.session_repo.create_session(session_model)

        # Convert internal data model back to Pydantic response schema
        session_response = DialysisSessionResponse(
            _id=str(created_session.id),
            **created_session.model_dump(exclude={"id"}) # Exclude 'id' as it's mapped to '_id'
        )
        return session_response

    async def get_today_schedule(self) -> List[DialysisSessionResponse]:
        """
        Fetches all dialysis sessions scheduled for the current day.
        """
        today = datetime.utcnow()
        sessions = await self.session_repo.get_sessions_for_day(today)

        # Convert internal data models to Pydantic response schemas
        session_responses = [
            DialysisSessionResponse(
                _id=str(session.id),
                **session.model_dump(exclude={"id"})
            )
            for session in sessions
        ]
        return session_responses