"""Main FastAPI application."""
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.config import settings
from app.db import init_db
from app.services import inference, storage
from app.routers import predict, history, feedback
from app.schemas import HealthResponse

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting LeafDoc API...")
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Ensure storage directories exist
    logger.info("Creating storage directories...")
    storage.ensure_storage_dirs()
    
    # Load model
    logger.info("Loading model...")
    model_loaded = inference.load_model()
    if model_loaded:
        logger.info("Model loaded successfully")
    else:
        logger.warning("Model not loaded - using stub predictions")
    
    logger.info("LeafDoc API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LeafDoc API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Plant disease detection API using deep learning",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing and request ID."""
    request_id = str(uuid.uuid4())
    
    # Add request ID to state
    request.state.request_id = request_id
    
    # Log request
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={"request_id": request_id}
    )
    
    # Process request
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.4f}s",
            extra={"request_id": request_id}
        )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} "
            f"Error: {str(e)} Time: {process_time:.4f}s",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={"request_id": request_id},
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        }
    )


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        Health status information
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        model_loaded=inference.is_model_loaded()
    )


# Include routers
app.include_router(predict.router, prefix=settings.API_PREFIX, tags=["Predictions"])
app.include_router(history.router, prefix=settings.API_PREFIX, tags=["History"])
app.include_router(feedback.router, prefix=settings.API_PREFIX, tags=["Feedback"])

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=settings.STORAGE_DIR), name="static")
    logger.info(f"Static files mounted at /static -> {settings.STORAGE_DIR}")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "Plant disease detection API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
