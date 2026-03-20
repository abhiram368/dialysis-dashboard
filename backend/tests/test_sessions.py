import pytest
from unittest.mock import MagicMock
from backend.src.core.patients.service import PatientService
from backend.src.api.v1.patients.schemas import PatientCreate
from backend.src.data.models.patient import PatientModel
from datetime import datetime

@pytest.mark.asyncio
async def test_create_patient():
    """
    Tests that a patient is created correctly.
    """
    mock_repo = MagicMock()
    
    # Create a mock of the returned patient model
    mock_patient = PatientModel(
        _id="60d5ec49e9af4a2c8c4a1b2d",
        first_name="Test",
        last_name="Patient",
        date_of_birth=datetime.utcnow(),
        dry_weight_kg=70.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Configure the mock repository to return the mock patient
    mock_repo.create_patient.return_value = mock_patient
    
    # Initialize the service with the mock repository
    service = PatientService(patient_repo=mock_repo)
    
    # Create a patient create schema
    patient_data = PatientCreate(
        first_name="Test",
        last_name="Patient",
        date_of_birth=datetime.utcnow(),
        dry_weight_kg=70.0
    )
    
    # Call the create_patient method
    created_patient = await service.create_patient(patient_data)
    
    # Assert that the repository's create_patient method was called once
    mock_repo.create_patient.assert_called_once()
    
    # Assert that the created patient has the correct data
    assert created_patient.first_name == "Test"
    assert created_patient.last_name == "Patient"
    assert created_patient.dry_weight_kg == 70.0
