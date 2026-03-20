from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Custom type for MongoDB's ObjectId
# Allows Pydantic to validate and serialize ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class PatientModel(BaseModel):
    """
    Represents a patient document in MongoDB.
    Uses PyObjectId for the _id field to handle MongoDB's ObjectId type.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: datetime
    dry_weight_kg: float = Field(..., gt=0)
    gender: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True # Required for PyObjectId
        json_schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Doe",
                "date_of_birth": "1985-05-15T00:00:00Z",
                "dry_weight_kg": 65.2,
                "gender": "Female",
                "contact_number": "987-654-3210",
                "address": "456 Oak Ave, Othertown"
            }
        }
