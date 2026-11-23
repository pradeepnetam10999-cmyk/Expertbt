from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base,engine
from app.api import router

Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version="1.0.0",
    description="All-Learning binary-options research and demo platform. No real-money execution.")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,
    allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api")

@app.get("/")
def root():
    return {"name":settings.app_name,"version":"1.0.0","status":"development",
            "mode":"research_demo","real_money_execution":False}
