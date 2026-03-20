from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from .service import DialysisSessionService
from .session_repo import DialysisSessionRepository
from .schemas import DialysisSessionCreate, DialysisSessionResponse

router = APIRouter()

# Dependency for DialysisSessionService
def get_session_service(session_repo: DialysisSessionRepository = Depends(DialysisSessionRepository)) -> DialysisSessionService:
    return DialysisSessionService(session_repo)

@router.post(
    "/",
    response_model=DialysisSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a new dialysis session",
    description="Records a new dialysis session for a patient, including pre/post weight, vitals, and nurse notes. Automatically detects anomalies."
)
async def record_dialysis_session(
    session_data: DialysisSessionCreate, session_service: DialysisSessionService = Depends(get_session_service)
) -> DialysisSessionResponse:
    """Records a new dialysis session in the system."""
    # Basic validation: end_time must be after start_time
    if session_data.end_time <= session_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="End time must be after start time."
        )
    return await session_service.create_session(session_data)

@router.get(
    "/today",
    response_model=List[DialysisSessionResponse],
    status_code=status.HTTP_200_OK,
    summary="Fetch today's dialysis schedule",
    description="Retrieves all dialysis sessions scheduled for the current day, including any detected anomalies."
)
async def get_today_schedule(
    session_service: DialysisSessionService = Depends(get_session_service)
) -> List[DialysisSessionResponse]:
    """Fetches the dialysis schedule for the current day."""
    return await session_service.get_today_schedule()