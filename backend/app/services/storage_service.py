from google.cloud import storage
from ..config import MENUS_BUCKET, PROJECT_ID

_storage_client = None

def get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client

def upload_menu_file(restaurant_id: str, menu_id: str, filename: str, content: bytes, content_type: str) -> str:
    client = get_storage_client()
    bucket = client.bucket(MENUS_BUCKET)
    blob_path = f"{restaurant_id}/{menu_id}/{filename}"
    blob = bucket.blob(blob_path)
    blob.upload_from_string(content, content_type=content_type)
    return f"gs://{MENUS_BUCKET}/{blob_path}"
