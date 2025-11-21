from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from ..models.menu import ParsedMenu, MenuItem
from ..services.firestore_service import menu_doc, restaurant_doc
from ..services.gemini_service import generate_json
from ..config import GEMINI_MODEL_PARSER

router = APIRouter(prefix="/tools", tags=["tools"])

class ParseMenuRequest(BaseModel):
    restaurantId: str
    menuId: str
    menuName: str
    rawMenuText: Optional[str] = None

class ParseMenuResponse(BaseModel):
    menu: ParsedMenu

@router.post("/parse_menu", response_model=ParseMenuResponse)
async def parse_menu(req: ParseMenuRequest):
    if not req.rawMenuText:
        raise HTTPException(status_code=400, detail="rawMenuText is required for now")

    # you can fetch stationConfig from restaurant doc to bias station assignments
    restaurant = restaurant_doc(req.restaurantId).get()
    station_ids = ["tandoor", "curry", "tawa", "rice_biryani", "garde_manger", "desserts", "beverages"]
    if restaurant.exists:
        cfg = restaurant.to_dict().get("stationConfig")
        if cfg:
            station_ids = [s.get("id") for s in cfg]

    prompt = f"""
You are an expert in Indian restaurant menus and kitchen operations.

Convert the following Indian menu into JSON with this schema:

{{
  "name": string,
  "items": [
    {{
      "id": string,                  // slug: lowercase, underscores
      "name": string,
      "category": string,
      "price": number | null,
      "stations": [string],          // choose from: {station_ids}
      "ingredients": [
        {{"name": string, "quantity": number | null, "unit": string | null}}
      ],
      "prepTimeSeconds": number | null,
      "cookTimeSeconds": number | null,
      "complexityScore": number | null  // 0-1, higher = more complex
    }}
  ]
}}

Menu will contain Indian dishes like: Butter Chicken, Paneer Butter Masala, Veg Biryani,
Paneer Tikka, Chicken Tikka, Dal Makhani, Masala Dosa, Idli, Medu Vada, Sambar, etc.

Be consistent: similar gravies (e.g. makhani) should reference the same ingredient name.

MENU TEXT:
{req.rawMenuText}
"""

    json_str = generate_json(GEMINI_MODEL_PARSER, prompt)
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Gemini JSON: {e}")

    items = [MenuItem(**item) for item in parsed.get("items", [])]

    menu = ParsedMenu(
        restaurantId=req.restaurantId,
        name=req.menuName,
        items=items
    )

    # save back to Firestore
    menu_ref = menu_doc(req.restaurantId, req.menuId)
    menu_ref.set({
        "name": req.menuName,
        "parsed": True,
        "parsedAt": firestore.SERVER_TIMESTAMP,  # type: ignore[name-defined]
        "items": [i.model_dump() for i in items]
    }, merge=True)

    return ParseMenuResponse(menu=menu)
