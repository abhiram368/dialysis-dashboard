import logging
from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ..database import db
from ..models.patient import PatientModel

logger = logging.getLogger(__name__)

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorCollection

class PatientRepository:
    """
    Repository for interacting with the 'patients' collection in MongoDB.
    """
    def __init__(self):
        assert db.database is not None, "MongoDB database not connected. Ensure connect_to_mongo is called on application startup."
        self.collection: "AsyncIOMotorCollection" = db.database.get_collection("patients") # type: ignore

    async def create_patient(self, patient: PatientModel) -> PatientModel:
        """Inserts a new patient document into the database."""
        patient_dict = patient.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(patient_dict)
        patient.id = str(result.inserted_id)
        logger.info(f"Patient created with ID: {patient.id}")
        return patient

    async def get_patient_by_id(self, patient_id: str) -> Optional[PatientModel]:
        data = await self.collection.find_one({"_id": ObjectId(patient_id)})
    
        if not data:
            return None

        data["id"] = str(data["_id"])   # convert ObjectId → str
        return PatientModel(**data)