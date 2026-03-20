from datetime import datetime
import logging

from ...api.v1.patients.schemas import PatientCreate, PatientResponse # Keep API schemas for input/output
from ...data.models.patient import PatientModel # Use the new PatientModel for internal representation
from ...data.repositories.patient_repo import PatientRepository

logger = logging.getLogger(__name__)

class PatientService:
    """
    Handles business logic for patient operations.
    Interacts with PatientRepository for data persistence.
    """
    def __init__(self, patient_repo: PatientRepository):
        self.patient_repo = patient_repo

    async def create_patient(self, patient_data: PatientCreate) -> PatientResponse:
        """Registers a new patient."""
        # Convert Pydantic input schema to internal data model
        patient_model = PatientModel(**patient_data.model_dump())
        now = datetime.utcnow()
        patient_model.created_at = now
        patient_model.updated_at = now

        # Persist to database via repository
        created_patient = await self.patient_repo.create_patient(patient_model)

        # Convert internal data model back to Pydantic response schema
        patient_response = PatientResponse(
            _id=str(created_patient.id), # Ensure ID is string for API response
            created_at=created_patient.created_at,
            updated_at=created_patient.updated_at,
            **created_patient.model_dump(exclude={"id", "created_at", "updated_at"})
        )
        return patient_response