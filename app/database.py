from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo import MongoClient
import gridfs
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["favorites_db"]
favorites_collection = db["favorites"]

grid_fs = AsyncIOMotorGridFSBucket(db, "fs")
