from bson import ObjectId
from pydantic import BaseModel


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
