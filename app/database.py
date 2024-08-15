from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from app.favorites.models import FavoritesModel, PyObjectId
from bson import ObjectId
from faker import Faker
import asyncio
import os

MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://favorites-mongodb.hfu5mq8dph6eg.us-east-1.cs.amazonlightsail.com:27017/favorites_db",
)
client = AsyncIOMotorClient(MONGODB_URL)
db = client["favorites_db"]
favorites_collection = db["favorites"]


fake = Faker()


def create_fake_artwork():
    return {
        "_score": fake.random_number(digits=5, fix_len=True),
        "dimensions_detail": [
            {
                "depth": fake.random_number(digits=2) if fake.boolean() else None,
                "diameter": fake.random_number(digits=2) if fake.boolean() else None,
                "width": fake.random_number(digits=2),
                "clarification": fake.word() if fake.boolean() else None,
                "height": fake.random_number(digits=2),
            }
        ],
        "medium_display": fake.text(max_nb_chars=20),
        "artist_display": f"{fake.name()}\n{fake.country()}",
        "alt_titles": None,
        "style_title": fake.word(),
        "exhibition_history": None,
        "title": fake.sentence(nb_words=3),
        "gallery_title": f"Gallery {fake.random_number(digits=3)}",
        "place_of_origin": fake.country(),
        "api_model": "artworks",
        "api_link": f"https://api.artic.edu/api/v1/artworks/{fake.random_number(digits=6)}",
        "id": fake.random_number(digits=6),
        "image_id": str(ObjectId()),
        "dimensions": f"{fake.random_number(digits=2)} × {fake.random_number(digits=2)} cm ({fake.random_number(digits=2)} × {fake.random_number(digits=2)} in.)",
    }


def create_fake_favorite() -> FavoritesModel:
    return FavoritesModel(
        id=PyObjectId(),  # Generate a new ObjectId for the ID
        user_session_email=fake.email(),  # Generate a fake email
        title=fake.sentence(nb_words=6),  # Generate a fake title
        artwork={  # Generate a fake artwork object
            "_score": fake.random_number(digits=5),
            "dimensions_detail": [
                {
                    "depth": None,
                    "diameter": None,
                    "width": fake.random_number(digits=3),
                    "clarification": None,
                    "height": fake.random_number(digits=3),
                }
            ],
            "medium_display": fake.word() + " on canvas",
            "artist_display": fake.name(),
            "alt_titles": None,
            "style_title": fake.word(),
            "exhibition_history": None,
            "title": fake.sentence(nb_words=3),
            "gallery_title": fake.word(),
            "place_of_origin": fake.country(),
            "api_model": "artworks",
            "api_link": fake.url(),
            "image_id": str(ObjectId()),
            "dimensions": f"{fake.random_number(digits=2)} × {fake.random_number(digits=2)} cm",
        },
    )


async def seed_database(n: int):
    fake_favorites = [create_fake_favorite() for _ in range(n)]
    # Convert each FavoritesModel instance to a dictionary
    favorite_dicts = [favorite.dict(by_alias=True) for favorite in fake_favorites]
    await favorites_collection.insert_many(favorite_dicts)
    print(f"Inserted {n} fake favorites into the database.")
