from pydantic import BaseModel
from enum import Enum
from datetime import date

class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip-hop"


class Album(BaseModel):
    title: str
    release_date: date 

class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album] = []