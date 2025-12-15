from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Distributed Event Logging System")
app.include_router(router)
