"""
Borrower's Forum Platform - Admin Router
=========================================

Framework Applied: api_design_integration_framework.md
Principle: Secure admin endpoints for API key management

Endpoints:
- POST /api/v1/admin/keys - Generate new API key (admin only)
- GET /api/v1/admin/keys - List all API keys (admin only)
- GET /api/v1/admin/keys/{key_id} - Get specific key details
- DELETE /api/v1/admin/keys/{key_id} - Deactivate a key
- POST /api/v1/admin/keys/bootstrap - Create first admin key (one-time use)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.auth import require_admin_permission
from src.services.auth_service import AuthService
from src.models.debt_data import APIKey


router = APIRouter(
    prefix="/admin",
    tags=["Admin - API Key Management"]
)


# ==========================================
# PYDANTIC MODELS (Request/Response)
# ==========================================

class APIKeyCreateRequest(BaseModel):
    """Request body for creating a new API key."""
    name: str = Field(..., min_length=3, max_length=100, example="UN DESA Production")
    owner: str = Field(..., min_length=2, max_length=100, example="UN DESA")
    permissions: str = Field(default="read", example="read")
    rate_limit_per_minute: int = Field(default=100, ge=1, le=1000, example=100)
    expires_in_days: Optional[int] = Field(default=None, ge=1, le=365, example=90)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "UN DESA Production Key",
                "owner": "UN DESA",
                "permissions": "read",
                "rate_limit_per_minute": 100,
                "expires_in_days": 90
            }
        }


class APIKeyResponse(BaseModel):
    """Response model for API key (without sensitive data)."""
    key_id: str
    name: str
    owner: str
    permissions: str
    is_active: bool
    rate_limit_per_minute: int
    created_at: datetime
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    usage_count: int
    
    class Config:
        orm_mode = True


class APIKeyCreatedResponse(BaseModel):
    """Response when a new API key is created (includes the full key)."""
    message: str
    api_key: str = Field(..., description="The full API key. Store this securely - it cannot be retrieved again!")
    key_id: str
    name: str
    owner: str
    permissions: str
    rate_limit_per_minute: int
    expires_at: Optional[datetime]
    warning: str = "Store this API key securely. It will not be shown again!"


class BootstrapKeyRequest(BaseModel):
    """Request for bootstrap key creation."""
    admin_secret: str = Field(..., min_length=20, description="The bootstrap secret from environment")
    name: str = Field(default="Initial Admin Key", example="Initial Admin Key")
    owner: str = Field(default="System Administrator", example="System Administrator")


# ==========================================
# BOOTSTRAP ENDPOINT (One-time setup)
# ==========================================

@router.post(
    "/keys/bootstrap",
    response_model=APIKeyCreatedResponse,
    summary="Create initial admin key (one-time)",
    description="""
    **One-time bootstrap endpoint** to create the first admin API key.
    
    This endpoint only works when NO admin keys exist in the database.
    After the first admin key is created, this endpoint is disabled.
    
    Requires a bootstrap secret that should be set as an environment variable.
    """
)
def bootstrap_admin_key(
    request: BootstrapKeyRequest,
    db: Session = Depends(get_db)
):
    """
    Create the first admin API key.
    
    This is a one-time operation that only works when no admin keys exist.
    """
    auth_service = AuthService(db)
    
    # Check if any admin keys already exist
    existing_admin_keys = db.query(APIKey).filter(
        APIKey.permissions == "admin",
        APIKey.is_active == True
    ).count()
    
    if existing_admin_keys > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Bootstrap disabled",
                "message": "Admin keys already exist. Use an existing admin key to create more keys.",
                "hint": "This endpoint only works for initial setup"
            }
        )
    
    # Verify bootstrap secret from environment variable
    from src.config.settings import get_settings
    settings = get_settings()
   
    
    if request.admin_secret != settings.BOOTSTRAP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid bootstrap secret",
                "message": "The provided bootstrap secret is incorrect"
            }
        )
    
    # Create the admin key
    full_key, api_key = auth_service.generate_api_key(
        name=request.name,
        owner=request.owner,
        permissions="admin",
        rate_limit_per_minute=1000  # Admin gets higher rate limit
    )
    
    return APIKeyCreatedResponse(
        message="Admin API key created successfully!",
        api_key=full_key,
        key_id=api_key.key_id,
        name=api_key.name,
        owner=api_key.owner,
        permissions=api_key.permissions,
        rate_limit_per_minute=api_key.rate_limit_per_minute,
        expires_at=api_key.expires_at,
        warning="Store this API key securely. It will not be shown again!"
    )


# ==========================================
# API KEY MANAGEMENT ENDPOINTS
# ==========================================

@router.post(
    "/keys",
    response_model=APIKeyCreatedResponse,
    summary="Generate new API key",
    description="Create a new API key. Requires admin permission."
)
def create_api_key(
    request: APIKeyCreateRequest,
    db: Session = Depends(get_db),
    admin_key: APIKey = Depends(require_admin_permission)
):
    """
    Generate a new API key.
    
    Only admins can create new keys.
    The full API key is only shown once - store it securely!
    """
    auth_service = AuthService(db)
    
    # Validate permissions value
    valid_permissions = ["read", "read_write", "admin"]
    if request.permissions not in valid_permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid permissions",
                "message": f"Permissions must be one of: {valid_permissions}",
                "provided": request.permissions
            }
        )
    
    # Generate the key
    full_key, api_key = auth_service.generate_api_key(
        name=request.name,
        owner=request.owner,
        permissions=request.permissions,
        rate_limit_per_minute=request.rate_limit_per_minute,
        expires_in_days=request.expires_in_days
    )
    
    return APIKeyCreatedResponse(
        message="API key created successfully!",
        api_key=full_key,
        key_id=api_key.key_id,
        name=api_key.name,
        owner=api_key.owner,
        permissions=api_key.permissions,
        rate_limit_per_minute=api_key.rate_limit_per_minute,
        expires_at=api_key.expires_at,
        warning="Store this API key securely. It will not be shown again!"
    )


@router.get(
    "/keys",
    response_model=List[APIKeyResponse],
    summary="List all API keys",
    description="Get a list of all API keys. Requires admin permission."
)
def list_api_keys(
    include_inactive: bool = Query(default=False, description="Include deactivated keys"),
    db: Session = Depends(get_db),
    admin_key: APIKey = Depends(require_admin_permission)
):
    """
    List all API keys (without exposing secrets).
    
    Only admins can view the key list.
    """
    auth_service = AuthService(db)
    keys = auth_service.list_api_keys(include_inactive=include_inactive)
    return keys


@router.get(
    "/keys/{key_id}",
    response_model=APIKeyResponse,
    summary="Get API key details",
    description="Get details for a specific API key. Requires admin permission."
)
def get_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    admin_key: APIKey = Depends(require_admin_permission)
):
    """
    Get details for a specific API key.
    
    The key_id is the public identifier (not the full key).
    """
    auth_service = AuthService(db)
    api_key = auth_service.get_api_key_by_id(key_id)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Key not found",
                "message": f"No API key found with key_id: {key_id}"
            }
        )
    
    return api_key


@router.delete(
    "/keys/{key_id}",
    summary="Deactivate API key",
    description="Deactivate an API key. Requires admin permission."
)
def deactivate_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    admin_key: APIKey = Depends(require_admin_permission)
):
    """
    Deactivate an API key (soft delete).
    
    The key will no longer work, but the record is preserved for audit purposes.
    """
    # Prevent self-deactivation
    if key_id == admin_key.key_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Cannot deactivate own key",
                "message": "You cannot deactivate the key you're currently using"
            }
        )
    
    auth_service = AuthService(db)
    success = auth_service.deactivate_api_key(key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Key not found",
                "message": f"No API key found with key_id: {key_id}"
            }
        )
    
    return {
        "message": "API key deactivated successfully",
        "key_id": key_id
    }


@router.post(
    "/keys/{key_id}/reactivate",
    response_model=APIKeyResponse,
    summary="Reactivate API key",
    description="Reactivate a previously deactivated API key. Requires admin permission."
)
def reactivate_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    admin_key: APIKey = Depends(require_admin_permission)
):
    """
    Reactivate a deactivated API key.
    """
    auth_service = AuthService(db)
    success = auth_service.reactivate_api_key(key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Key not found",
                "message": f"No API key found with key_id: {key_id}"
            }
        )
    
    # Return the updated key
    api_key = auth_service.get_api_key_by_id(key_id)
    return api_key