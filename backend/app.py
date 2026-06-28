from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
import logging
import os

from config import settings
from api.routes import router as api_router
from api.middleware import setup_cors, setup_exception_handlers, setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AQI Vision AI API",
    description="Air Quality Index Prediction and Analysis Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Setup CORS
setup_cors(app, [settings.frontend_url, "http://localhost:3000", "http://localhost:5173"])

# Setup exception handlers
setup_exception_handlers(app)

# Include API routes
app.include_router(api_router)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AQI Vision AI API",
        version="1.0.0",
        description="Comprehensive Air Quality Index Prediction, Analysis, and Recommendation System",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Health check endpoint
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "AQI Vision API",
        "environment": settings.environment
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AQI Vision AI API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level="info"
    )
