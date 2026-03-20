import logging
from typing import Optional, TYPE_CHECKING
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..config.settings import Settings

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoDB:
    client: Optional["AsyncIOMotorClient"] = None # type: ignore
    database: Optional["AsyncIOMotorDatabase"] = None # type: ignore

db = MongoDB()

async def connect_to_mongo():
    """Connects to MongoDB at application startup."""
    settings = Settings()
    client_instance = AsyncIOMotorClient(settings.mongodb_url) # Assign to local variable
    db.client = client_instance
    db.database = client_instance[settings.mongodb_db_name] # Use local variable
    logger.info(f"Connected to MongoDB: {settings.mongodb_url}, Database: {settings.mongodb_db_name}")

async def close_mongo_connection():
    """Closes the MongoDB connection at application shutdown."""
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed.")