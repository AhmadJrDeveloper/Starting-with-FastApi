from pydantic import BaseModel, validator
from enum import Enum
from datetime import date

class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    HIP_HOP = "hip-hop"

class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hip-Hop"    


class Album(BaseModel):
    title: str
    release_date: date 

class BandBase(BaseModel):
    # id: int
    name: str
    genre: GenreChoices
    albums: list[Album] = []

class BandCreate(BandBase):
    @validator('genre', pre=True)
    def title_case_genre(cls, value):
        return value.title() #rOck -> Rock

class BandWithID(BandBase):
    id: int