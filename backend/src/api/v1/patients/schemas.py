from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    """Schema for creating a new patient."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: datetime
    dry_weight_kg: float = Field(..., gt=0)
    gender: Optional[str] = None # e.g., "Male", "Female", "Other"
    contact_number: Optional[str] = None
    address: Optional[str] = None

class PatientResponse(PatientCreate):
    """Schema for a patient returned by the API, including their unique ID."""
    id: str = Field(..., alias="_id") # MongoDB uses _id, Pydantic can map it
    created_at: datetime
    updated_at: datetime

    class Config:
        # Allow population by field name (id) or alias (_id)
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "60d0fe4f5311236168a109ca",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1970-01-01T00:00:00Z",
                "dry_weight_kg": 70.5,
                "gender": "Male",
                "contact_number": "123-456-7890",
                "address": "123 Main St, Anytown",
                "created_at": "2023-10-27T10:00:00Z",
                "updated_at": "2023-10-27T10:00:00Z"
            }
        }