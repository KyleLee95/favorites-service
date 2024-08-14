from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from bson import ObjectId
from app.favorites.models import FavoritesModel, PaginatedFavoriteResponse, Pagination
from app.database import favorites_collection
import math

router = APIRouter()


@router.get("/", response_model=PaginatedFavoriteResponse)
async def get_favorites(page: int = 1, limit: int = 10):
    total_items = await favorites_collection.count_documents({})
    favorites = (
        await favorites_collection.find()
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


# GET records by page
@router.get("/paged/{pageNum}", response_model=list[FavoritesModel])
async def get_favorites_paged(pageNum: int = 0):
    favorites = (
        await favorites_collection.find().skip(pageNum * 20).limit(20).to_list(20)
    )
    return favorites


@router.post("/", response_model=FavoritesModel)
async def add_favorite(favorite: FavoritesModel):
    new_favorite = await favorites_collection.insert_one(favorite.dict(by_alias=True))
    created_favorite = await favorites_collection.find_one(
        {"_id": new_favorite.inserted_id}
    )
    return created_favorite


@router.put("/{id}", response_model=FavoritesModel)
async def update_favorite(id: str, favorite: FavoritesModel):
    result = await favorites_collection.replace_one(
        {"_id": ObjectId(id)}, favorite.dict(by_alias=True)
    )
    if result.modified_count == 1:
        updated_favorite = await favorites_collection.find_one({"_id": ObjectId(id)})
        return updated_favorite
    raise HTTPException(status_code=404, detail="Favorite not found")


@router.delete("/{id}")
async def delete_favorite(id: str):
    result = await favorites_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"status": "Favorite deleted"}
    raise HTTPException(status_code=404, detail="Favorite not found")
