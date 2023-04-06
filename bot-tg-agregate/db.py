from motor.motor_asyncio import AsyncIOMotorClient
from config import Config


def get_db() -> AsyncIOMotorClient:
    """Mongodb `Motor` client getter"""
    _uri = Config.MONGO_URI.format(
        user=Config.MONGO_USER,
        password=Config.MONGO_PASSWORD,
        address=Config.MONGO_ADDRESS,
        port=Config.MONGO_PORT
    )
    return AsyncIOMotorClient(_uri)
