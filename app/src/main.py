from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .routers.products import router as products_router


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="DevOps Performance & Scalability Platform",
)


@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "environment": settings.app_env,
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/ready")
def readiness():
    return {
        "status": "ready",
    }


app.include_router(products_router)


Instrumentator().instrument(app).expose(app)
