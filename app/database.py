from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
class Database:
client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None
db_instance = Database()
async def connect_to_mongo():
db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)
db_instance.db = db_instance.client[settings.DATABASE_NAME]
async def close_mongo_connection():
if db_instance.client:
db_instance.client.close()
def get_collection():
if db_instance.db is None:
  raise RuntimeError("Database not initialized. Please ensure lifespan startup completed.")
return db_instance.db[settings.COLLECTION_NAME]
