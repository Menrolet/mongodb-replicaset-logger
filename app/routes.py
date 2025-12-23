from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .db import events
from .models import EventIn

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/events")
def add_event(event: EventIn):
    events.insert_one(event.model_dump())
    return {"status": "ok"}

@router.get("/events")
def get_events(service: str | None = None, level: str | None = None):
    query = {}
    if service: query["service"] = service
    if level: query["level"] = level
    return list(events.find(query, {"_id": 0}).limit(100))

@router.get("/events/stats")
def stats_by_level():
    pipeline = [
        {"$group": {"_id": "$level", "count": {"$sum": 1}}}
    ]
    return list(events.aggregate(pipeline))

@router.get("/health")
def health():
    return {"status": "up"}
