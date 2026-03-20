from typing import Any, Dict, Optional

class DialysisDashboardException(Exception):
    """Base exception for the Dialysis Dashboard application."""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)