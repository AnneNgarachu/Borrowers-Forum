"""
Borrower's Forum Platform - Authentication Dependencies
========================================================

Framework Applied: api_design_integration_framework.md
Principle: Dependency injection for clean, reusable authentication

Usage in routers:
    from src.api.auth import require_api_key, require_admin
    
    @router.get("/protected")
    def protected_endpoint(api_key: APIKey = Depends(require_api_key)):
        return {"owner": api_key.owner}
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from collections import defaultdict
import time

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.services.auth_service import AuthService
from src.models.debt_data import APIKey


# ==========================================
# API KEY HEADER CONFIGURATION
# ==========================================

# Define the header where API key should be provided
api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,  # We'll handle missing key ourselves for better error messages
    description="API key for authentication. Format: bf_<key_id>_<secret>"
)


# ==========================================
# RATE LIMITER (In-Memory)
# ==========================================

class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    Tracks requests per API key and enforces limits.
    
    Note: This resets when the server restarts.
    For production at scale, use Redis instead.
    """
    
    def __init__(self):
        # Structure: {key_id: [(timestamp1), (timestamp2), ...]}
        self._requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key_id: str, limit_per_minute: int) -> tuple:
        """
        Check if a request is allowed under the rate limit.
        
        Args:
            key_id: The API key identifier
            limit_per_minute: Maximum requests allowed per minute
        
        Returns:
            Tuple of (is_allowed: bool, requests_remaining: int, reset_time: int)
        """
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests (older than 1 minute)
        self._requests[key_id] = [
            ts for ts in self._requests[key_id] 
            if ts > minute_ago
        ]
        
        current_count = len(self._requests[key_id])
        remaining = max(0, limit_per_minute - current_count)
        
        if current_count >= limit_per_minute:
            # Calculate when the oldest request will expire
            oldest = min(self._requests[key_id]) if self._requests[key_id] else now
            reset_time = int(oldest + 60 - now)
            return False, 0, reset_time
        
        # Record this request
        self._requests[key_id].append(now)
        
        return True, remaining - 1, 60


# Global rate limiter instance
rate_limiter = RateLimiter()


# ==========================================
# AUTHENTICATION DEPENDENCIES
# ==========================================

async def get_api_key_optional(
    api_key: Optional[str] = Security(api_key_header),
    db: Session = Depends(get_db)
) -> Optional[APIKey]:
    """
    Get API key if provided, but don't require it.
    
    Use this for endpoints that work with or without authentication,
    but provide more data when authenticated.
    """
    if not api_key:
        return None
    
    auth_service = AuthService(db)
    return auth_service.verify_api_key(api_key)


async def require_api_key(
    api_key: Optional[str] = Security(api_key_header),
    db: Session = Depends(get_db)
) -> APIKey:
    """
    Require a valid API key for the endpoint.
    
    Use this for protected endpoints:
    
        @router.get("/data")
        def get_data(api_key: APIKey = Depends(require_api_key)):
            return {"owner": api_key.owner}
    
    Raises:
        HTTPException 401: If no API key provided
        HTTPException 401: If API key is invalid
        HTTPException 403: If API key is expired or inactive
        HTTPException 429: If rate limit exceeded
    """
    # Check if key was provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "API key required",
                "message": "Please provide an API key in the X-API-Key header",
                "docs": "Contact the platform administrator to obtain an API key"
            },
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Validate key format
    if not api_key.startswith("bf_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid API key format",
                "message": "API key must start with 'bf_'",
                "example": "bf_xxxxxxxxxxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            }
        )
    
    # Verify the key
    auth_service = AuthService(db)
    verified_key = auth_service.verify_api_key(api_key)
    
    if not verified_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid API key",
                "message": "The provided API key is invalid, expired, or has been deactivated"
            }
        )
    
    # Check rate limit
    is_allowed, remaining, reset_time = rate_limiter.is_allowed(
        verified_key.key_id, 
        verified_key.rate_limit_per_minute
    )
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Limit: {verified_key.rate_limit_per_minute}/minute",
                "retry_after_seconds": reset_time
            },
            headers={
                "Retry-After": str(reset_time),
                "X-RateLimit-Limit": str(verified_key.rate_limit_per_minute),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_time)
            }
        )
    
    return verified_key


async def require_read_permission(
    api_key: APIKey = Depends(require_api_key)
) -> APIKey:
    """
    Require at least read permission.
    
    Allowed permissions: read, read_write, admin
    """
    # All valid keys have at least read permission
    return api_key


async def require_write_permission(
    api_key: APIKey = Depends(require_api_key)
) -> APIKey:
    """
    Require write permission.
    
    Allowed permissions: read_write, admin
    """
    if api_key.permissions not in ["read_write", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Insufficient permissions",
                "message": "This endpoint requires write permission",
                "your_permission": api_key.permissions,
                "required": "read_write or admin"
            }
        )
    return api_key


async def require_admin_permission(
    api_key: APIKey = Depends(require_api_key)
) -> APIKey:
    """
    Require admin permission.
    
    Allowed permissions: admin only
    """
    if api_key.permissions != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Insufficient permissions",
                "message": "This endpoint requires admin permission",
                "your_permission": api_key.permissions,
                "required": "admin"
            }
        )
    return api_key


# ==========================================
# DEVELOPER NOTES
# ==========================================
"""
USAGE EXAMPLES:

1. Protect an endpoint (require any valid key):
   
   from src.api.auth import require_api_key
   
   @router.get("/countries")
   def list_countries(api_key: APIKey = Depends(require_api_key)):
       # api_key contains the verified key record
       return {"message": f"Hello, {api_key.owner}!"}

2. Require specific permissions:
   
   from src.api.auth import require_admin_permission
   
   @router.delete("/keys/{key_id}")
   def delete_key(key_id: str, api_key: APIKey = Depends(require_admin_permission)):
       # Only admin keys can access this
       pass

3. Optional authentication:
   
   from src.api.auth import get_api_key_optional
   
   @router.get("/public")
   def public_endpoint(api_key: Optional[APIKey] = Depends(get_api_key_optional)):
       if api_key:
           return {"message": f"Hello, {api_key.owner}!"}
       else:
           return {"message": "Hello, anonymous user!"}

HTTP ERROR CODES:
- 401 Unauthorized: No key provided or invalid key
- 403 Forbidden: Valid key but insufficient permissions
- 429 Too Many Requests: Rate limit exceeded
"""