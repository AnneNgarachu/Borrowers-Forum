"""
Borrower's Forum Platform - FastAPI Application
================================================

Framework Applied: api_design_integration_framework.md
Principle: Clean API architecture with proper middleware and error handling
Why: Production-ready API that's easy to extend and maintain
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from src.config.settings import get_settings
from src.services.database import check_database_health
from src.utils.env_validator import validate_environment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()


# ============================================
# LIFESPAN EVENTS
# Framework: Monitoring & Observability Framework
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    
    Framework: Monitoring & Observability
    - Startup validation
    - Health checks
    - Graceful shutdown
    
    Why: Catch configuration issues early, clean shutdown
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 60)
    
    # Validate environment
    is_valid, issues = validate_environment()
    if not is_valid:
        logger.error("❌ Environment validation failed!")
        for issue in issues:
            logger.error(f"  {issue}")
        raise RuntimeError("Cannot start application with invalid configuration")
    
    # Check database health
    db_health = check_database_health()
    if db_health["status"] == "healthy":
        logger.info(f"✓ Database: {db_health['database_type']}")
    else:
        logger.warning(f"⚠️  Database: {db_health['details']}")
    
    logger.info(f"✓ Environment: {settings.ENVIRONMENT}")
    logger.info(f"✓ API: {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"✓ Debug Mode: {settings.DEBUG}")
    logger.info("=" * 60)
    logger.info("✅ Application started successfully!")
    logger.info("=" * 60)
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("🛑 Shutting down application...")
    logger.info("=" * 60)


# ============================================
# CREATE FASTAPI APPLICATION
# Framework: API Design & Integration Framework
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Debt intelligence platform for the UN-backed Borrower's Forum",
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc",  # ReDoc
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


# ============================================
# MIDDLEWARE
# Framework: API Design & Integration Framework
# ============================================

# CORS Middleware
# Framework: Security Excellence Framework
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Timing Middleware
# Framework: Monitoring & Observability Framework
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Add response time header to all requests.
    
    Framework: Monitoring & Observability
    Why: Track API performance, identify slow endpoints
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    
    # Log slow requests
    if process_time > 1.0:
        logger.warning(
            f"Slow request: {request.method} {request.url.path} "
            f"took {process_time:.2f}s"
        )
    
    return response


# Request Logging Middleware
# Framework: Monitoring & Observability Framework
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests.
    
    Framework: Monitoring & Observability
    Why: Audit trail, debugging, monitoring
    """
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"← {request.method} {request.url.path} - {response.status_code}")
    return response


# ============================================
# ERROR HANDLERS
# Framework: API Design & Integration Framework
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with clear messages.
    
    Framework: API Design & Integration
    Why: User-friendly error messages, help developers debug
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "status_code": 422,
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors gracefully.
    
    Framework: Security Excellence + Monitoring
    Why: Don't leak internal details, but log for debugging
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # In development, show full error
    if settings.DEBUG:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "status_code": 500,
                "details": str(exc),
                "type": type(exc).__name__
            }
        )
    
    # In production, hide details
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "status_code": 500,
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# ============================================
# ROOT ENDPOINTS
# Framework: API Design & Integration Framework
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns basic information about the API.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "operational",
        "docs": "/api/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Framework: Monitoring & Observability Framework
    Used by load balancers and monitoring systems to verify service health.
    
    Returns:
        dict: Health status including database connectivity
    """
    db_health = check_database_health()
    
    # Determine overall health
    is_healthy = db_health["status"] == "healthy"
    
    return {
        "status": "healthy" if is_healthy else "degraded",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_health,
        "timestamp": time.time()
    }


# ============================================
# API ROUTER REGISTRATION
# Framework: Clean Architecture
# ============================================

# Import routers
from src.api.routers.countries import router as countries_router
from src.api.routers.debt import router as debt_router
from src.api.routers.precedents import router as precedents_router



# Register routers
app.include_router(countries_router, prefix=settings.API_V1_PREFIX, tags=["Countries"])
app.include_router(debt_router, prefix=settings.API_V1_PREFIX, tags=["Debt Calculator"])
app.include_router(precedents_router, prefix=settings.API_V1_PREFIX, tags=["Precedents Search"])




# ============================================
# DEVELOPER NOTES
# ============================================
"""
FASTAPI APPLICATION STRUCTURE:

1. **Lifespan Events**:
   - Startup: Validate environment, check database
   - Shutdown: Graceful cleanup
   
2. **Middleware** (order matters!):
   - CORS: Enable cross-origin requests
   - Timing: Track request duration
   - Logging: Audit trail

3. **Error Handlers**:
   - Validation errors: 422 with clear messages
   - Server errors: 500 (hide details in production)

4. **Root Endpoints**:
   - /: API information
   - /health: Health check for monitoring

5. **API Routers**:
   - /api/v1/countries: Country operations
   - /api/v1/debt: Debt calculator (coming next)
   - /api/v1/precedents: Precedent search (coming next)

HOW TO RUN:

Development (with auto-reload):
```bash
python -m uvicorn src.api.main:app --reload
```

Production:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

HOW TO TEST:

1. Start server: `uvicorn src.api.main:app --reload`
2. Open browser: http://localhost:8000
3. View docs: http://localhost:8000/api/docs
4. Health check: http://localhost:8000/health

HOW TO ADD NEW ENDPOINTS:

1. Create router file: `src/api/routers/my_feature.py`
2. Define endpoints with FastAPI decorators
3. Import in main.py: `from src.api.routers import my_feature`
4. Register: `app.include_router(my_feature.router, prefix="/api/v1")`
"""