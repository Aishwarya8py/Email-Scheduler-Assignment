import motor.motor_asyncio

from .config import MONGO_DB_NAME, MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

schedules_col = db["schedules"]
logs_col = db["send_logs"]
