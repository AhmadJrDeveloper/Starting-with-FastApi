from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip-hop"


BANDS = [
    {"id": 1, "name": "The kinks", "genre": "Rock"},
    {"id": 2, "name": "The Beatles", "genre": "Electronic"},
    {"id": 3, "name": "Led Zeppelin", "genre": "Hip-Hop"},
    {"id": 4, "name": "Queen", "genre": "Rock"},
    {"id": 5, "name": "Pink Floyd", "genre": "Rock"},
]

@app.get('/')
async def index() -> dict[str, str]:
    return {"message": "Hello, World!"}
    # return {"message": 5}

@app.get('/about')
async def about() -> str:
    return  "This is a simple FastAPI application"

@app.get("/bands")
async def bands() -> list[dict]:
    return BANDS

@app.get("/bands/{band_id}")
async def band(band_id: int) -> dict:
    band = next((b for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    else:
        return band
    
@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
        # Comparing the genre from the BANDS data with the enum value of the user-specified genre (case-insensitive)
    return [
        b for b in BANDS if b['genre'].lower() == genre.value.lower()
    ]