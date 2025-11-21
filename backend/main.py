from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from google.cloud import firestore

app = FastAPI()

db = firestore.Client()

class MenuItem(BaseModel):
    name: str
    ingredients: List[str]

class Menu(BaseModel):
    items: List[MenuItem]

@app.post("/parse_menu")
def parse_menu(menu: Menu):
    # Simple example
    parsed = [{"dish": item.name, "ingredient_count": len(item.ingredients)} for item in menu.items]
    return {"parsed": parsed}

@app.post("/analyze_stations")
def analyze_stations(menu: Menu):
    # VERY simple prototype logic
    stations = {
        "tandoor": [],
        "curry": [],
        "rice": []
    }

    for item in menu.items:
        lower = item.name.lower()
        if "tikka" in lower:
            stations["tandoor"].append(item.name)
        if "biryani" in lower:
            stations["rice"].append(item.name)
        if "butter" in lower or "masala" in lower:
            stations["curry"].append(item.name)

    return {"stations": stations}

@app.post("/store_menu")
def store_menu(menu: Menu):
    doc_ref = db.collection("menus").add(menu.dict())
    return {"stored": True, "id": doc_ref[1].id}
