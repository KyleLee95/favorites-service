from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from bson import ObjectId

router = APIRouter()


# GET all records
@router.get("/")
async def get_favorites():
    pass


@router.get("/{id}")
async def get_favorite(id: int):
    pass
    # raise HTTPException(status_code=404, detail="Favorite not found")


# GET records by page
@router.get("/paged/{pageNum}")
async def get_favorites_paged(pageNum: int = 0):
    pass
