from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo import MongoClient
import gridfs
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://favorites-mongodb:27017/favorites_db")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["favorites_db"]
favorites_collection = db["favorites"]

grid_fs = AsyncIOMotorGridFSBucket(db, "fs")
