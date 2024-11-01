from fastapi import FastAPI, HTTPException, Path, Query
from enum import Enum
from schemas import BandBase, BandCreate, BandWithID, GenreURLChoices
from typing import Annotated

app = FastAPI()


BANDS = [
    {"id": 1, "name": "The kinks", "genre": "Rock"},
    {"id": 2, "name": "The Beatles", "genre": "Electronic"},
    {"id": 3, "name": "Led Zeppelin", "genre": "Hip-Hop"},
    {"id": 4, "name": "Queen", "genre": "Rock"},
    {
        "id": 5,
        "name": "Pink Floyd",
        "genre": "Rock",
        "albums": [{"title": "Master of Realm", "release_date": "2015-07-11"}],
    },
]


@app.get("/")
async def index() -> dict[str, str]:
    return {"message": "Hello, World!"}
    # return {"message": 5}


@app.get("/about")
async def about() -> str:
    return "This is a simple FastAPI application"


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    #  has_albums: bool = False
    q: Annotated[str | None, Query(max_length = 10)] = None
) -> list[BandWithID]:
    band_list = [BandWithID(**band) for band in BANDS]
    if genre:
        # Filtering the BANDS based on the user-specified genre (case-insensitive)
        band_list = [
            band for band in band_list if band.genre.lower() == genre.value.lower()
        ]
    # if has_albums:
    #     # Filtering the BANDS based on the presence of albums
    #     band_list = [
    #         band for band in band_list if band.albums
    #     ]

    if q:
        band_list = [
            band for band in band_list if q.lower() in band.name.lower()
        ]
    return band_list


@app.get("/bands/{band_id}")
async def band(band_id: Annotated[int, Path(title="The Band ID")]) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    else:
        return band


@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
    # Comparing the genre from the BANDS data with the enum value of the user-specified genre (case-insensitive)
    return [b for b in BANDS if b["genre"].lower() == genre.value.lower()]


@app.post("/bands")
async def band_create(bandData: BandCreate) -> BandWithID:
    id = BANDS[-1]["id"] + 1
    band = BandWithID(id=id, **bandData.model_dump()).model_dump()
    BANDS.append(band)
    return band
