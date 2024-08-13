from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    """
    A custom ObjectId field for use with Pydantic models, to support MongoDB ObjectId serialization.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class FavoritesModel(BaseModel):
    id: int  # Custom numeric ID field
    title: str
    image_file_id: Optional[PyObjectId] = Field(
        default=None, alias="_id"
    )  # Reference to the GridFS file

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
