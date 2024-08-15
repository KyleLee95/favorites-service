from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List


class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_items: Optional[int] = None
    limit: Optional[int] = None


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

    def __str__(self):
        return str(self)


class ArtworkModel(BaseModel):
    id: int
    title: str
    artist_display: Optional[str]
    place_of_origin: Optional[str]
    medium_display: Optional[str]
    dimensions: Optional[str]
    image_id: Optional[str]


class FavoritesModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_session_email: str = Field(alias="userSessionEmail")
    artwork: ArtworkModel

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        from_attributes = True  # If you're using Pydantic V2


class PaginatedFavoriteResponse(BaseModel):
    pagination: Pagination
    data: List[FavoritesModel]


class FavoriteRequest(BaseModel):
    user_session_email: str
    artwork: ArtworkModel

    class Config:
        # Allows handling MongoDB ObjectIds correctly
        arbitrary_types_allowed = True
