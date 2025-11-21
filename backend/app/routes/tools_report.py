from fastapi import APIRouter
from datetime import datetime

from ..models.analysis import GenerateReportRequest, GenerateReportResponse
from ..services.firestore_service import report_doc
from ..services.gemini_service import generate_text
from ..config import GEMINI_MODEL_REPORT

router = APIRouter(prefix="/tools", tags=["tools"])

@router.post("/generate_report", response_model=GenerateReportResponse)
async def generate_report(req: GenerateReportRequest):
    json_report = {
        "inefficiencies": req.inefficiencies,
        "menuSummary": {
            "itemCount": len(req.menu.items),
            "categories": sorted({i.category for i in req.menu.items if i.category}),
        }
    }

    prompt = f"""
You are an expert consultant for Indian restaurant kitchens.

Write a concise, actionable report for the restaurant owner.

Context:
- The restaurant serves Indian dishes like Butter Chicken, Veg Biryani, Paneer Tikka, Dal Makhani, Masala Dosa, etc.
- They care about overloaded stations (especially curry station), ingredient reuse (gravies, chutneys), and food waste.

Use the JSON below as the source of truth:

JSON_REPORT:
{json_report}

Report structure:
- Title
- Summary (3-4 bullet points)
- Section: Station Load & Bottlenecks
- Section: Ingredient & Prep Inefficiencies
- Section: Concrete Recommendations (short bullets)

Keep it under 700 words.
"""

    narrative = generate_text(GEMINI_MODEL_REPORT, prompt)

    report_id = f"report_{int(datetime.utcnow().timestamp())}"
    doc = report_doc(req.restaurantId, report_id)
    doc.set({
        "menuId": req.menuId,
        "analysisRunId": req.analysisRunId,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "jsonReport": json_report,
        "narrative": narrative
    })

    return GenerateReportResponse(
        jsonReport=json_report,
        narrative=narrative
    )
