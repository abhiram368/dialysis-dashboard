from fastapi import APIRouter, status, Depends

from ....data.database import db

from .schemas import PatientCreate, PatientResponse
from ....core.patients.service import PatientService
from ....data.repositories.patient_repo import PatientRepository

router = APIRouter()

# Dependency for PatientService (can be injected for testing)
def get_patient_service(patient_repo: PatientRepository = Depends(PatientRepository)) -> PatientService:
    return PatientService(patient_repo)

@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new patient",
    description="Registers a new patient with their dry weight and basic demographics."
)
async def register_patient(
    patient_data: PatientCreate, patient_service: PatientService = Depends(get_patient_service)
) -> PatientResponse:
    """Registers a new patient in the system."""
    return await patient_service.create_patient(patient_data)