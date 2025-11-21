from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from ..services.storage_service import upload_menu_file
from ..services.firestore_service import menu_doc, restaurant_doc

router = APIRouter(prefix="/restaurants", tags=["menus"])

@router.post("/{restaurant_id}/menus/upload")
async def upload_menu(
    restaurant_id: str,
    menu_name: str = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Only PDF/PNG/JPEG supported")

    content = await file.read()
    menu_id = menu_name.lower().replace(" ", "_")

    gs_uri = upload_menu_file(restaurant_id, menu_id, file.filename, content, file.content_type)

    # Ensure restaurant exists (create basic doc if not)
    restaurant_ref = restaurant_doc(restaurant_id)
    if not restaurant_ref.get().exists:
        restaurant_ref.set({
            "name": restaurant_id,
            "location": "India",
            "serviceStyle": "full_service",
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }, merge=True)

    menu_ref = menu_doc(restaurant_id, menu_id)
    menu_ref.set({
        "name": menu_name,
        "rawSourceType": "pdf" if file.content_type == "application/pdf" else "image",
        "rawSourceLocation": gs_uri,
        "parsed": False,
        "parsedAt": None,
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }, merge=True)

    return {
        "restaurantId": restaurant_id,
        "menuId": menu_id,
        "gsUri": gs_uri
    }
