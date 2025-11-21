from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import menu_upload, tools_parse_menu, tools_analyze, tools_report

app = FastAPI(title="Indian Menu Optimizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu_upload.router)
app.include_router(tools_parse_menu.router)
app.include_router(tools_analyze.router)
app.include_router(tools_report.router)

@app.get("/")
def health():
    return {"status": "ok"}
