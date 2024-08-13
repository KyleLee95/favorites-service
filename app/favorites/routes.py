from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from bson import ObjectId
from app.favorites.models import FavoritesModel
from app.database import favorites_collection

router = APIRouter()


# GET all records
@router.get("/", response_model=list[FavoritesModel])
async def get_favorites():
    favorites = await favorites_collection.find().to_list(1000)
    return favorites


@router.get("/{id}", response_model=FavoritesModel)
async def get_favorite(id: int):
    favorite = await favorites_collection.find_one({"id": id})
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


# DELETE a record by id
@router.delete("/{id}")
async def delete_favorite(id: str):
    result = await favorites_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"status": "Favorite deleted"}
    raise HTTPException(status_code=404, detail="Favorite not found")


# PUT (update) a record by id
@router.put("/{id}", response_model=FavoritesModel)
async def update_favorite(id: str, favorite: FavoritesModel):
    result = await favorites_collection.replace_one(
        {"_id": ObjectId(id)}, favorite.dict(by_alias=True)
    )
    if result.modified_count == 1:
        return favorite
    raise HTTPException(status_code=404, detail="Favorite not found")


# POST (add) a new record
@router.post("/", response_model=FavoritesModel)
async def add_favorite(favorite: FavoritesModel):
    new_favorite = await favorites_collection.insert_one(favorite.dict(by_alias=True))
    created_favorite = await favorites_collection.find_one(
        {"_id": new_favorite.inserted_id}
    )
    return created_favorite
