from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from .menu import ParsedMenu, Station

class AnalysisParams(BaseModel):
    serviceWindowMinutes: int = 120
    targetCovers: int = 80

class AnalysisRequest(BaseModel):
    restaurantId: str
    menuId: str
    menu: ParsedMenu
    stationConfig: List[Station]
    params: AnalysisParams

class ConflictAnalysisResponse(BaseModel):
    inefficiencies: List[Dict[str, Any]]
    score: float

class GenerateReportRequest(BaseModel):
    restaurantId: str
    menuId: str
    analysisRunId: Optional[str] = None
    menu: ParsedMenu
    inefficiencies: List[Dict[str, Any]]

class GenerateReportResponse(BaseModel):
    jsonReport: Dict[str, Any]
    narrative: str
