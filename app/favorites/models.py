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
    def validate(
        cls, v, field=None, config=None
    ):  # Update the signature to accept additional arguments
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
        populate_by_name = True  # Updated to Pydantic V2
        from_attributes = True


class PaginatedFavoriteResponse(BaseModel):
    pagination: Pagination
    data: List[FavoritesModel]


class FavoriteRequest(BaseModel):
    user_session_email: str
    artwork: ArtworkModel

    class Config:
        arbitrary_types_allowed = True
