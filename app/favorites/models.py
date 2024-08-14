from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
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
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    userSessionEmail: EmailStr
    image_file_id: Optional[PyObjectId] = None  # Reference to the GridFS file

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
