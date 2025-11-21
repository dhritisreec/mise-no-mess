from fastapi import APIRouter
from datetime import datetime
import json

from ..models.analysis import AnalysisRequest, ConflictAnalysisResponse
from ..services.firestore_service import analysis_run_doc
from ..services.gemini_service import generate_json
from ..config import GEMINI_MODEL_ANALYSIS

router = APIRouter(prefix="/tools", tags=["tools"])

@router.post("/analyze_conflicts", response_model=ConflictAnalysisResponse)
async def analyze_conflicts(req: AnalysisRequest):
    # simple feature extraction
    station_usage = {}
    ingredient_usage = {}

    for item in req.menu.items:
        for s in item.stations:
            station_usage.setdefault(s, 0)
            station_usage[s] += (item.prepTimeSeconds or 300) + (item.cookTimeSeconds or 300)

        for ing in item.ingredients:
            key = ing.name.lower()
            ingredient_usage.setdefault(key, 0)
            ingredient_usage[key] += 1

    features = {
        "stationUsage": station_usage,
        "ingredientUsage": ingredient_usage,
        "stationConfig": [s.model_dump() for s in req.stationConfig],
        "params": req.params.model_dump()
    }

    prompt = f"""
You are a kitchen operations consultant for Indian restaurants.

Given the features JSON below, identify:
- Overloaded stations (e.g. curry station with too many gravies like Butter Chicken, Dal Makhani, Paneer Butter Masala).
- Underutilized stations (e.g. tandoor with very few dishes).
- Ingredient bottlenecks (e.g. makhani gravy used across many dishes).
- Inconsistent ingredient usage (same chutney/gravy prepared differently in multiple stations).
- Specific recommendations to reduce waste and balance workflow.

Return this JSON:

{{
  "inefficiencies": [
    {{
      "id": string,
      "type": "station_overload" | "station_underutilized" | "ingredient_bottleneck" | "inconsistent_usage" | "other",
      "severity": "low" | "medium" | "high",
      "stationId": string | null,
      "ingredient": string | null,
      "details": object,
      "recommendations": [string]
    }}
  ],
  "score": number  // 0-1 where higher is a better-designed menu
}}

FEATURES:
{json.dumps(features, indent=2)}
"""

    json_str = generate_json(GEMINI_MODEL_ANALYSIS, prompt)
    res = json.loads(json_str)

    run_id = f"run_{int(datetime.utcnow().timestamp())}"
    doc = analysis_run_doc(req.restaurantId, run_id)
    doc.set({
        "menuId": req.menuId,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "status": "completed",
        "parameters": req.params.model_dump(),
        "summary": {
            "score": res.get("score"),
            "keyFindings": [
                i.get("type") + ": " + (i.get("recommendations") or [""])[0]
                for i in res.get("inefficiencies", [])[:5]
            ]
        }
    })

    return ConflictAnalysisResponse(
        inefficiencies=res.get("inefficiencies", []),
        score=res.get("score", 0.0)
    )
