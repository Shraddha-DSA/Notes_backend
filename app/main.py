from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes.notes import router
from app.routes.users import router as user_router
Base.metadata.create_all(bind=engine)
app=FastAPI(
    title="Notes Management API"
)
app.include_router(router)
app.include_router(user_router)