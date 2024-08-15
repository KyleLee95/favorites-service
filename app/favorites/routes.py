from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from bson import ObjectId
from typing import Optional
from app.favorites.models import FavoritesModel, PaginatedFavoriteResponse, Pagination
from app.database import favorites_collection
import math

router = APIRouter()


@router.get("/", response_model=PaginatedFavoriteResponse)
async def get_favorites(
    user_session_email: str,  # Required parameter for exact email match
    query: Optional[str] = None,  # Fuzzy search query parameter
    page: int = 1,
    limit: int = 10,
):
    # Exact match filter for user session email
    base_query = {"userSessionEmail": user_session_email}

    # If a fuzzy search query is provided, add regex filtering for title and artist
    if query is not None:
        base_query["$or"] = [
            {
                "title": {"$regex": query, "$options": "i"}
            },  # Case-insensitive search on title
            {
                "artist": {"$regex": query, "$options": "i"}
            },  # Case-insensitive search on artist
        ]

    # Count total items for pagination based on the constructed query
    total_items = await favorites_collection.count_documents(base_query)

    # Fetch the paginated results
    favorites = (
        await favorites_collection.find(base_query)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(length=limit)
    )

    total_pages = math.ceil(total_items / limit)
    pagination = Pagination(
        current_page=page, total_pages=total_pages, total_items=total_items, limit=limit
    )

    return PaginatedFavoriteResponse(pagination=pagination, data=favorites)


@router.get("/{id}", response_model=FavoritesModel)
async def get_favorite_by_id(id: str):
    favorite = await favorites_collection.find_one({"_id": ObjectId(id)})
    if favorite:
        return favorite
    raise HTTPException(status_code=404, detail="Favorite not found")


@router.post("/", response_model=FavoritesModel)
async def add_favorite(favorite: FavoritesModel):
    # Check if a similar favorite already exists (optional check)
    existing_favorite = await favorites_collection.find_one(
        {"user_session_email": favorite.user_session_email, "artwork": favorite.artwork}
    )
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Favorite already exists")

    # Insert the new favorite
    new_favorite = await favorites_collection.insert_one(favorite.dict(by_alias=True))
    created_favorite = await favorites_collection.find_one(
        {"_id": new_favorite.inserted_id}
    )
    return created_favorite


@router.delete("/{id}")
async def delete_favorite(id: str):
    result = await favorites_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"status": "Favorite deleted"}
    raise HTTPException(status_code=404, detail="Favorite not found")
