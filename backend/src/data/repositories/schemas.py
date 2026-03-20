from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DialysisSessionCreate(BaseModel):
    """Schema for creating a new dialysis session."""
    patient_id: str = Field(..., description="The ID of the patient for this session.")
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    pre_weight_kg: float = Field(..., gt=0)
    post_weight_kg: float = Field(..., gt=0)
    systolic_bp_pre: Optional[int] = Field(None, gt=0)
    diastolic_bp_pre: Optional[int] = Field(None, gt=0)
    systolic_bp_post: Optional[int] = Field(None, gt=0)
    diastolic_bp_post: Optional[int] = Field(None, gt=0)
    machine_id: Optional[str] = None
    nurse_notes: Optional[str] = None

class DialysisSessionResponse(DialysisSessionCreate):
    """Schema for a dialysis session returned by the API, including its unique ID and detected anomalies."""
    id: str = Field(..., alias="_id") # MongoDB uses _id, Pydantic can map it
    anomalies: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f5311236168a109cb",
                "patient_id": "60d0fe4f5311236168a109ca",
                "start_time": "2023-10-27T08:00:00Z",
                "end_time": "2023-10-27T12:00:00Z",
                "pre_weight_kg": 70.0,
                "post_weight_kg": 67.5,
                "systolic_bp_pre": 130,
                "diastolic_bp_pre": 85,
                "systolic_bp_post": 120,
                "diastolic_bp_post": 80,
                "machine_id": "M-001",
                "nurse_notes": "Patient tolerated session well.",
                "anomalies": ["Excess interdialytic weight gain"]
            }
        }