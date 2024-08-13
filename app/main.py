from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.favorites.routes import router as favorites_router
from app.favorites.models import FavoritesModel
from app.search.routes import router as search_router
from app.database import favorites_collection  # Import the collection
from faker import Faker
from pymongo.errors import BulkWriteError

app = FastAPI()
fake = Faker()

app.include_router(favorites_router, prefix="/favorites")
app.include_router(search_router, prefix="/search")


@app.on_event("startup")
async def startup_event():
    print("FastAPI server startup event")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Favorites API!"}


# 404 Handler
@app.exception_handler(StarletteHTTPException)
async def not_found_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Sorry, we couldn't find that. We might not support that functionality."
            },
        )

    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
