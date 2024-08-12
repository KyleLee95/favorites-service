from fastapi import FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from models import BeerModel
from bson import ObjectId
from faker import Faker
import os

app = FastAPI()
fake = Faker()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["beer_db"]
collection = db["beers"]


@app.on_event("startup")
async def startup_event():
    await collection.delete_many({})  # Clear the collection on startup
    await collection.create_index("id", unique=True)

    beers = [
        BeerModel(id=i, name=fake.name()).dict(by_alias=True)
        for i in range(1, 1001)  # Generate IDs from 1 to 1000
    ]

    try:
        await collection.insert_many(beers)
    except BulkWriteError as bwe:
        print("Bulk Write Error:", bwe.details)  # Log or handle the error as needed


@app.get("/")
def read_root():
    return {"message": "Welcome to the Beer API!"}


# GET all records
@app.get("/beers/", response_model=list[BeerModel])
async def get_beers():
    beers = await collection.find().to_list(1000)
    return beers


@app.get("/beers/{id}", response_model=BeerModel)
async def get_beer(id: int):
    beer = await collection.find_one({"id": id})
    if beer:
        return beer
    raise HTTPException(status_code=404, detail="Beer not found")


# GET records by page
@app.get("/beers/paged/{pageNum}", response_model=list[BeerModel])
async def get_beers_paged(pageNum: int = 0):
    beers = await collection.find().skip(pageNum * 20).limit(20).to_list(20)
    return beers


# DELETE a record by id
@app.delete("/beers/{id}")
async def delete_beer(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"status": "Beer deleted"}
    raise HTTPException(status_code=404, detail="Beer not found")


# PUT (update) a record by id
@app.put("/beers/{id}", response_model=BeerModel)
async def update_beer(id: str, beer: BeerModel):
    result = await collection.replace_one(
        {"_id": ObjectId(id)}, beer.dict(by_alias=True)
    )
    if result.modified_count == 1:
        return beer
    raise HTTPException(status_code=404, detail="Beer not found")


# POST (add) a new record
@app.post("/beers/", response_model=BeerModel)
async def add_beer(beer: BeerModel):
    new_beer = await collection.insert_one(beer.dict(by_alias=True))
    created_beer = await collection.find_one({"_id": new_beer.inserted_id})
    return created_beer
