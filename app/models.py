from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class EventIn(BaseModel):
    service: str
    level: str
    message: str
    host: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = datetime.utcnow()
