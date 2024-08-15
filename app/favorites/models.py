from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None, config=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

    def __str__(self):
        return str(self)


class FavoritesModel(BaseModel):
    id: PyObjectId  # Use MongoDB's ObjectId as the ID
    user_session_email: str
    title: str
    artwork: dict  # Storing a complex JSON object as a dictionary

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True


class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_items: Optional[int] = None
    limit: Optional[int] = None


class PaginatedFavoriteResponse(BaseModel):
    pagination: Pagination
    data: List[FavoritesModel]


class ArtworkModel(BaseModel):
    id: int
    title: str
    artist_display: Optional[str]
    place_of_origin: Optional[str]
    medium_display: Optional[str]
    dimensions: Optional[str]
    image_id: Optional[str]


class FavoriteRequest(BaseModel):
    user_session_email: str
    artwork: ArtworkModel

    class Config:
        # Allows handling MongoDB ObjectIds correctly
        arbitrary_types_allowed = True
