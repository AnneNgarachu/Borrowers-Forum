"""
Borrower's Forum Platform - Authentication Service
==================================================

Framework Applied: api_design_integration_framework.md
Principle: Secure API key management with hashed storage

Features:
- Secure key generation (bf_<key_id>_<secret>)
- SHA-256 hashing (secrets never stored in plain text)
- Key verification with timing-safe comparison
- Rate limiting support
- Usage tracking
"""

import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.models.debt_data import APIKey


class AuthService:
    """
    Service for API key authentication and management.
    
    Key Format: bf_<key_id>_<secret>
    - bf_: Prefix identifying Borrower's Forum keys
    - key_id: 16-character public identifier (used for lookups)
    - secret: 32-character random secret (hashed for storage)
    
    Example: bf_abc123def456ghij_aBcDeFgHiJkLmNoPqRsTuVwXyZ012345
    """
    
    # Key configuration
    KEY_PREFIX = "bf_"
    KEY_ID_LENGTH = 16
    SECRET_LENGTH = 32
    
    # Characters for key generation (URL-safe)
    KEY_ID_CHARS = string.ascii_lowercase + string.digits
    SECRET_CHARS = string.ascii_letters + string.digits
    
    def __init__(self, db: Session):
        """Initialize auth service with database session."""
        self.db = db
    
    # ==========================================
    # KEY GENERATION
    # ==========================================
    
    def generate_api_key(
        self,
        name: str,
        owner: str,
        permissions: str = "read",
        rate_limit_per_minute: int = 100,
        expires_in_days: Optional[int] = None
    ) -> Tuple[str, APIKey]:
        """
        Generate a new API key.
        
        Args:
            name: Descriptive name (e.g., "UN DESA Production")
            owner: Key owner (e.g., "UN DESA")
            permissions: "read", "read_write", or "admin"
            rate_limit_per_minute: Max requests per minute (default 100)
            expires_in_days: Days until expiration (None = never expires)
        
        Returns:
            Tuple of (full_api_key, APIKey record)
            
        IMPORTANT: The full API key is only returned ONCE at creation.
        Store it securely - it cannot be retrieved later!
        """
        # Generate key components
        key_id = self._generate_key_id()
        secret = self._generate_secret()
        
        # Create full key (this is what the user receives)
        full_key = f"{self.KEY_PREFIX}{key_id}_{secret}"
        
        # Hash the secret for storage (NEVER store plain text!)
        key_hash = self._hash_secret(secret)
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Validate permissions
        valid_permissions = ["read", "read_write", "admin"]
        if permissions not in valid_permissions:
            raise ValueError(f"Invalid permissions. Must be one of: {valid_permissions}")
        
        # Create database record
        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            owner=owner,
            permissions=permissions,
            rate_limit_per_minute=rate_limit_per_minute,
            expires_at=expires_at,
            is_active=True,
            usage_count=0
        )
        
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        
        return full_key, api_key
    
    def _generate_key_id(self) -> str:
        """Generate a random 16-character key ID."""
        return ''.join(
            secrets.choice(self.KEY_ID_CHARS) 
            for _ in range(self.KEY_ID_LENGTH)
        )
    
    def _generate_secret(self) -> str:
        """Generate a random 32-character secret."""
        return ''.join(
            secrets.choice(self.SECRET_CHARS) 
            for _ in range(self.SECRET_LENGTH)
        )
    
    def _hash_secret(self, secret: str) -> str:
        """
        Hash a secret using SHA-256.
        
        Why SHA-256 instead of bcrypt?
        - API keys are high-entropy random strings (not user passwords)
        - SHA-256 is fast for high-volume API verification
        - bcrypt's slowness is designed for low-entropy passwords
        """
        return hashlib.sha256(secret.encode()).hexdigest()
    
    # ==========================================
    # KEY VERIFICATION
    # ==========================================
    
    def verify_api_key(self, full_key: str) -> Optional[APIKey]:
        """
        Verify an API key and return the key record if valid.
        
        Args:
            full_key: The complete API key (bf_<key_id>_<secret>)
        
        Returns:
            APIKey record if valid, None if invalid
            
        Also updates last_used_at and usage_count on successful verification.
        """
        # Parse the key
        parsed = self._parse_api_key(full_key)
        if not parsed:
            return None
        
        key_id, secret = parsed
        
        # Look up the key by key_id
        api_key = self.db.query(APIKey).filter(
            APIKey.key_id == key_id
        ).first()
        
        if not api_key:
            return None
        
        # Verify the secret
        provided_hash = self._hash_secret(secret)
        if not secrets.compare_digest(provided_hash, api_key.key_hash):
            return None
        
        # Check if key is active
        if not api_key.is_active:
            return None
        
        # Check expiration
        if api_key.expires_at and api_key.expires_at < datetime.utcnow():
            return None
        
        # Update usage statistics
        api_key.last_used_at = datetime.utcnow()
        api_key.usage_count += 1
        self.db.commit()
        
        return api_key
    
    def _parse_api_key(self, full_key: str) -> Optional[Tuple[str, str]]:
        """
        Parse an API key into its components.
        
        Args:
            full_key: The complete API key
        
        Returns:
            Tuple of (key_id, secret) or None if invalid format
        """
        if not full_key or not full_key.startswith(self.KEY_PREFIX):
            return None
        
        # Remove prefix
        key_part = full_key[len(self.KEY_PREFIX):]
        
        # Split into key_id and secret
        parts = key_part.split('_', 1)
        if len(parts) != 2:
            return None
        
        key_id, secret = parts
        
        # Validate lengths
        if len(key_id) != self.KEY_ID_LENGTH or len(secret) != self.SECRET_LENGTH:
            return None
        
        return key_id, secret
    
    # ==========================================
    # KEY MANAGEMENT
    # ==========================================
    
    def list_api_keys(self, include_inactive: bool = False) -> list:
        """
        List all API keys (without exposing secrets).
        
        Args:
            include_inactive: Whether to include deactivated keys
        
        Returns:
            List of APIKey records (key_hash is not exposed in responses)
        """
        query = self.db.query(APIKey)
        
        if not include_inactive:
            query = query.filter(APIKey.is_active == True)
        
        return query.order_by(APIKey.created_at.desc()).all()
    
    def get_api_key_by_id(self, key_id: str) -> Optional[APIKey]:
        """Get an API key by its key_id."""
        return self.db.query(APIKey).filter(APIKey.key_id == key_id).first()
    
    def deactivate_api_key(self, key_id: str) -> bool:
        """
        Deactivate an API key (soft delete).
        
        Returns:
            True if key was deactivated, False if key not found
        """
        api_key = self.get_api_key_by_id(key_id)
        if not api_key:
            return False
        
        api_key.is_active = False
        self.db.commit()
        return True
    
    def reactivate_api_key(self, key_id: str) -> bool:
        """
        Reactivate a deactivated API key.
        
        Returns:
            True if key was reactivated, False if key not found
        """
        api_key = self.get_api_key_by_id(key_id)
        if not api_key:
            return False
        
        api_key.is_active = True
        self.db.commit()
        return True
    
    def delete_api_key(self, key_id: str) -> bool:
        """
        Permanently delete an API key.
        
        Returns:
            True if key was deleted, False if key not found
        """
        api_key = self.get_api_key_by_id(key_id)
        if not api_key:
            return False
        
        self.db.delete(api_key)
        self.db.commit()
        return True
    
    def update_api_key(
        self,
        key_id: str,
        name: Optional[str] = None,
        permissions: Optional[str] = None,
        rate_limit_per_minute: Optional[int] = None
    ) -> Optional[APIKey]:
        """
        Update an API key's metadata.
        
        Returns:
            Updated APIKey record or None if not found
        """
        api_key = self.get_api_key_by_id(key_id)
        if not api_key:
            return None
        
        if name is not None:
            api_key.name = name
        
        if permissions is not None:
            valid_permissions = ["read", "read_write", "admin"]
            if permissions not in valid_permissions:
                raise ValueError(f"Invalid permissions. Must be one of: {valid_permissions}")
            api_key.permissions = permissions
        
        if rate_limit_per_minute is not None:
            api_key.rate_limit_per_minute = rate_limit_per_minute
        
        self.db.commit()
        self.db.refresh(api_key)
        return api_key


# ==========================================
# DEVELOPER NOTES
# ==========================================
"""
SECURITY DESIGN DECISIONS:

1. **SHA-256 for API Keys** (not bcrypt):
   - API keys are 32 random characters = ~190 bits of entropy
   - Bcrypt is designed for low-entropy passwords (12-20 characters)
   - SHA-256 is sufficient and much faster for high-entropy secrets
   - Google, AWS, Stripe all use SHA-256 for API key hashing

2. **Key Format (bf_<key_id>_<secret>)**:
   - bf_: Prefix identifies our keys (helps with key rotation, debugging)
   - key_id: Public identifier for lookups (safe to log)
   - secret: Private part that proves ownership (never log!)

3. **Timing-Safe Comparison**:
   - secrets.compare_digest() prevents timing attacks
   - Regular == comparison leaks info about how many characters match

4. **Soft Delete**:
   - Deactivate instead of delete preserves audit trail
   - Can reactivate if needed
   - Hard delete available for GDPR compliance

USAGE EXAMPLE:

    from src.services.auth_service import AuthService
    from src.services.database import SessionLocal
    
    db = SessionLocal()
    auth = AuthService(db)
    
    # Generate a new key
    full_key, key_record = auth.generate_api_key(
        name="UN DESA Production",
        owner="UN DESA",
        permissions="read",
        rate_limit_per_minute=100
    )
    print(f"Store this key securely: {full_key}")
    
    # Verify a key
    api_key = auth.verify_api_key("bf_abc123..._xyz789...")
    if api_key:
        print(f"Valid key owned by: {api_key.owner}")
    else:
        print("Invalid key")
"""