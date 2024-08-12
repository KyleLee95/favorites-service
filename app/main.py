from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.favorites.routes import router as favorites_router
from app.favorites.models import FavoritesModel
from app.database import favorites_collection  # Import the collection
from faker import Faker
from pymongo.errors import BulkWriteError

app = FastAPI()
fake = Faker()

app.include_router(favorites_router, prefix="/favorites")


@app.on_event("startup")
async def startup_event():
    # Clear the collection on startup
    await favorites_collection.delete_many({})
    # Create a unique index on the 'id' field
    await favorites_collection.create_index("id", unique=True)

    # Generate fake data with custom numeric IDs
    favorites = [
        FavoritesModel(id=i, name=fake.name()).dict(by_alias=True)
        for i in range(1, 1001)  # Generate IDs from 1 to 1000
    ]

    try:
        # Insert the generated fake data into the collection
        await favorites_collection.insert_many(favorites)
    except BulkWriteError as bwe:
        print("Bulk Write Error:", bwe.details)  # Log or handle the error as needed


@app.get("/")
def read_root():
    return {"message": "Welcome to the Favorites API!"}


# 404 Handler
@app.exception_handler(StarletteHTTPException)
async def not_found_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "The requested resource was not found."},
        )

    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
