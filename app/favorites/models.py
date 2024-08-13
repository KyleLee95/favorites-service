from pydantic import BaseModel
from bson import ObjectId
from pydantic.json import pydantic_encoder
from typing import Optional


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


class FavoritesModel(BaseModel):
    id: int  # Custom numeric ID field
    title: str
    image_file_id: Optional[PyObjectId] = None  # Reference to the GridFS file

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
