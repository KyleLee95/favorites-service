from fastapi import APIRouter, Query
from app.aic_api import aic_api

router = APIRouter()


# GET all records
@router.get("/")
async def search(query: str = Query(..., description="The search query")):

    response = aic_api.search_artworks(query)

    return response


@router.get("/{id}")
async def get_favorite(id: int):
    return {"message": "Not implemented"}
    # raise HTTPException(status_code=404, detail="Favorite not found")


# GET records by page
@router.get("/paged/{pageNum}")
async def get_favorites_paged(pageNum: int = 0):
    response = aic_api.get_artworks_paged(pageNum)
    return response
