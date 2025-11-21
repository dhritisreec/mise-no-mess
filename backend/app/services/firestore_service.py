from google.cloud import firestore
from ..config import PROJECT_ID

_db = None

def get_db():
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db

def restaurant_doc(restaurant_id: str):
    return get_db().collection("restaurants").document(restaurant_id)

def menu_doc(restaurant_id: str, menu_id: str):
    return restaurant_doc(restaurant_id).collection("menus").document(menu_id)

def analysis_run_doc(restaurant_id: str, run_id: str):
    return restaurant_doc(restaurant_id).collection("analysisRuns").document(run_id)

def report_doc(restaurant_id: str, report_id: str):
    return restaurant_doc(restaurant_id).collection("reports").document(report_id)
