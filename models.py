from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


from pydantic import BaseModel, Field
from typing import Optional


class BeerModel(BaseModel):
    id: int  # Custom numeric ID field
    name: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
