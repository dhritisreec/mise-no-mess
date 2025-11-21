from pydantic import BaseModel
from typing import List
from .menu import Station

class Restaurant(BaseModel):
    id: str
    name: str
    location: str
    serviceStyle: str
    stationConfig: List[Station]
