import google.genai as genai
from ..config import PROJECT_ID, GEMINI_LOCATION, GEMINI_MODEL_PARSER, GEMINI_MODEL_ANALYSIS, GEMINI_MODEL_REPORT

_client = None

def get_client():
    global _client
    if _client is None:
        # vertexai=True => uses ADC; no API key needed on Cloud Run
        _client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=GEMINI_LOCATION
        )
    return _client

def generate_json(model: str, prompt: str) -> str:
    client = get_client()
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    return resp.text

def generate_text(model: str, prompt: str) -> str:
    client = get_client()
    resp = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return resp.text
