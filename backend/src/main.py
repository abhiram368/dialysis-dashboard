import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from .config.settings import Settings
from .core.exceptions import DialysisDashboardException
from .data.database import connect_to_mongo, close_mongo_connection
from .data.repositories import routes as sessions_routes
from .api.v1.patients import routes as patients_routes
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
def configure_logging(log_level: str):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Optionally, set uvicorn's loggers to the same level
    logging.getLogger("uvicorn.access").setLevel(numeric_level)
    logging.getLogger("uvicorn.error").setLevel(numeric_level)


# Initialize settings
settings = Settings()
configure_logging(settings.logging_level)

# Get a logger instance for this module
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="API for tracking dialysis sessions and detecting anomalies."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# --- Custom Exception Handlers ---
@app.exception_handler(DialysisDashboardException)
async def dialysis_dashboard_exception_handler(request: Request, exc: DialysisDashboardException):
    """Handles custom DialysisDashboardException, returning a structured JSON response."""
    logger.error(f"DialysisDashboardException caught: {exc.message} (Status: {exc.status_code}) for path: {request.url.path}", exc_info=True, extra={"details": exc.details})
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "details": exc.details,
            "code": exc.__class__.__name__
        },
    )

@app.get("/", include_in_schema=False)
async def root():
    """Redirects to the API documentation."""
    return RedirectResponse(url="/docs")

@app.get("/test-http-error")
async def test_http_error():
    """An endpoint to demonstrate raising a standard HTTPException."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This is a standard HTTP 404 error.")

@app.get("/test-custom-error")
async def test_custom_error():
    """An endpoint to demonstrate raising a custom DialysisDashboardException."""
    raise DialysisDashboardException(
        message="A specific application error occurred.", status_code=status.HTTP_400_BAD_REQUEST, details={"field": "value_invalid"})

# --- Global Exception Handler for unexpected errors ---
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles all unhandled exceptions, returning a generic 500 error."""
    logger.exception(f"Unhandled exception: {exc} for path: {request.url.path}", extra={"path": request.url.path})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An unexpected server error occurred.",
            "details": None,
            "code": "InternalServerError"
        },
    )

# --- API Routers ---
app.include_router(patients_routes.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(sessions_routes.router, prefix="/api/v1/sessions", tags=["Dialysis Sessions"])
