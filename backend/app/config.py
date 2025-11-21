import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0092808289")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "west-europe1")

# Firestore & Storage
FIRESTORE_USE_EMULATOR = os.getenv("FIRESTORE_EMULATOR_HOST") is not None
MENUS_BUCKET = os.getenv("MENUS_BUCKET", "restaurant-menus-" + PROJECT_ID)

# Gemini / Vertex AI
GEMINI_LOCATION = os.getenv("GEMINI_LOCATION", "west-europe1")
GEMINI_MODEL_PARSER = os.getenv("GEMINI_MODEL_PARSER", "gemini-2.5-flash")
GEMINI_MODEL_ANALYSIS = os.getenv("GEMINI_MODEL_ANALYSIS", "gemini-2.5-flash")
GEMINI_MODEL_REPORT = os.getenv("GEMINI_MODEL_REPORT", "gemini-2.5-flash")

