from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Custom type for MongoDB's ObjectId
# Allows Pydantic to validate and serialize ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class DialysisSessionModel(BaseModel):
    """
    Represents a dialysis session document in MongoDB.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patient_id: PyObjectId = Field(...) # Reference to the PatientModel
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
    anomalies: Optional[list[str]] = Field(default_factory=list) # List of detected anomaly types
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True # Required for PyObjectId
        json_schema_extra = {
            "example": {
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
                "anomalies": []
            }
        }