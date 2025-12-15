from fastapi import APIRouter
from .db import events
from .models import EventIn

router = APIRouter()

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
