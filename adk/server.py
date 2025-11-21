# server.py (in your ADK agent folder, e.g. misenomess/adk/)
import os
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
app: FastAPI = get_fast_api_app(agents_dir=AGENT_DIR, web=True)

@app.get("/health")
def health():
    return {"status": "ok", "service": "mise-no-mess-adk"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
