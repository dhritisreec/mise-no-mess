from pydantic import BaseModel
from typing import List, Optional

class Station(BaseModel):
    id: str
    name: str
    capacity: int
    equipment: List[str]
    notes: Optional[str] = None

class MenuItemIngredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

class MenuItem(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    stations: List[str] = []
    ingredients: List[MenuItemIngredient] = []
    prepTimeSeconds: Optional[int] = None
    cookTimeSeconds: Optional[int] = None
    complexityScore: Optional[float] = None

class ParsedMenu(BaseModel):
    restaurantId: str
    name: str
    items: List[MenuItem]
