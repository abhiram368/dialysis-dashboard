import logging
from datetime import datetime, timedelta
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database import db
from ..models.session import DialysisSessionModel

logger = logging.getLogger(__name__)

class DialysisSessionRepository:
    """
    Repository for interacting with the 'dialysis_sessions' collection in MongoDB.
    """
    def __init__(self):
        assert db.database is not None, "MongoDB database not connected. Ensure connect_to_mongo is called on application startup."
        self.collection: AsyncIOMotorCollection = db.database.get_collection("dialysis_sessions") # type: ignore

    async def create_session(self, session: DialysisSessionModel) -> DialysisSessionModel:
        """Inserts a new dialysis session document into the database."""
        session_dict = session.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(session_dict)
        session.id = str(result.inserted_id)
        logger.info(f"Dialysis session created with ID: {session.id} for patient {session.patient_id}")
        return session

    async def get_session_by_id(self, session_id: str) -> Optional[DialysisSessionModel]:
        """Retrieves a single dialysis session by its ID."""
        data = await self.collection.find_one({"_id": ObjectId(session_id)})
        if not data:
            return None
        data["id"] = str(data["_id"])
        return DialysisSessionModel(**data)

    async def get_sessions_by_patient_id(self, patient_id: str) -> List[DialysisSessionModel]:
        """Retrieves all dialysis sessions for a given patient ID."""
        sessions = await self.collection.find({"patient_id": ObjectId(patient_id)}).to_list(length=None)
        return [DialysisSessionModel(**{**s, "id": str(s["_id"])}) for s in sessions]

    async def get_sessions_for_day(self, target_date: datetime) -> List[DialysisSessionModel]:
        """
        Retrieves all dialysis sessions scheduled for a specific day.
        The target_date should represent the start of the day (e.g., 2023-10-27 00:00:00).
        """
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        sessions = await self.collection.find({
            "start_time": {"$gte": start_of_day, "$lt": end_of_day}
        }).sort("start_time", 1).to_list(length=None)

        return [DialysisSessionModel(**{**s, "id": str(s["_id"])}) for s in sessions]