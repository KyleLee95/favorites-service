from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.favorites.routes import router as favorites_router
from app.favorites.models import FavoritesModel
from app.database import favorites_collection, seed_database  # Import the collection
from pymongo.errors import BulkWriteError

app = FastAPI()

app.include_router(favorites_router, prefix="/favorites")


@app.on_event("startup")
async def startup_event():
    print("Starting up the favorites service...")
    await seed_database(10)


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
