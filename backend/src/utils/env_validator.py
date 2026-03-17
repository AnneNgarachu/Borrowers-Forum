"""
Environment Validation on Startup
==================================

Framework Applied: security_excellence_framework.md + monitoring_observability_generic.md
Principle: Fail fast with clear errors, validate critical configuration
Why: Catch configuration issues before they cause production problems
"""

from pathlib import Path
from typing import List, Tuple
import sys


def validate_environment() -> Tuple[bool, List[str]]:
    """
    Validate environment configuration on startup.
    
    Framework: Security Excellence Framework
    - Fail fast if critical config missing
    - Clear error messages
    - Environment-specific checks
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    warnings = []
    
    try:
        from src.config.settings import get_settings
        settings = get_settings()
        
        print("\n" + "="*60)
        print("🔍 ENVIRONMENT VALIDATION")
        print("="*60)
        
        # ============================================
        # Check 1: Environment
        # ============================================
        print(f"\n✓ Environment: {settings.ENVIRONMENT}")
        
        # ============================================
        # Check 2: Database Configuration
        # ============================================
        if settings.ENVIRONMENT == 'production':
            if 'sqlite' in settings.DATABASE_URL.lower():
                warnings.append("⚠️  WARNING: SQLite not recommended for production")
        
        print(f"✓ Database: {settings.DATABASE_URL.split('://')[0]}://...")
        
        # ============================================
        # Check 3: Secret Key Strength
        # ============================================
        if settings.ENVIRONMENT == 'production':
            if len(settings.SECRET_KEY) < 32:
                issues.append("❌ ERROR: SECRET_KEY too short for production (min 32 chars)")
            if settings.SECRET_KEY == 'your-secret-key-change-in-production':
                issues.append("❌ ERROR: Must set actual SECRET_KEY in production")
        
        print(f"✓ Secret Key: {'*' * min(len(settings.SECRET_KEY), 32)}")
        
        # ============================================
        # Check 4: Required Directories
        # ============================================
        required_dirs = [
            ('Data Directory', settings.DATA_DIR),
            ('Raw Data', settings.RAW_DATA_DIR),
            ('Processed Data', settings.PROCESSED_DATA_DIR),
            ('Database', settings.DATABASE_DIR),
            ('Logs', settings.LOGS_DIR),
            ('Outputs', settings.OUTPUTS_DIR),
        ]
        
        for dir_name, dir_path in required_dirs:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                warnings.append(f"⚠️  Created missing directory: {dir_name}")
            else:
                print(f"✓ {dir_name}: exists")
        
        # ============================================
        # Check 5: API Configuration
        # ============================================
        print(f"✓ API: {settings.API_HOST}:{settings.API_PORT}")
        print(f"✓ CORS Origins: {len(settings.CORS_ORIGINS)} configured")
        
        # ============================================
        # Check 6: External APIs
        # ============================================
        if settings.IMF_API_KEY:
            print(f"✓ IMF API Key: configured")
        else:
            print(f"ℹ️  IMF API Key: not set (optional)")
        
        if settings.WORLD_BANK_API_KEY:
            print(f"✓ World Bank API Key: configured")
        else:
            print(f"ℹ️  World Bank API Key: not set (optional)")
        
        # ============================================
        # Report Results
        # ============================================
        print("\n" + "="*60)
        
        if issues:
            print("❌ VALIDATION FAILED")
            print("="*60)
            for issue in issues:
                print(issue)
            return False, issues
        
        if warnings:
            print("⚠️  VALIDATION PASSED WITH WARNINGS")
            print("="*60)
            for warning in warnings:
                print(warning)
        else:
            print("✅ VALIDATION PASSED")
            print("="*60)
        
        return True, warnings
        
    except Exception as e:
        error_msg = f"❌ Environment validation failed: {e}"
        print("\n" + "="*60)
        print("❌ VALIDATION ERROR")
        print("="*60)
        print(error_msg)
        print("="*60 + "\n")
        return False, [error_msg]


def validate_and_exit_on_failure():
    """
    Run validation and exit if critical issues found.
    
    Use this in application startup to ensure proper configuration.
    
    Example:
        # In src/api/main.py
        from src.utils.env_validator import validate_and_exit_on_failure
        validate_and_exit_on_failure()
    """
    is_valid, issues = validate_environment()
    
    if not is_valid:
        print("\n❌ Cannot start application due to configuration errors.")
        print("Please fix the issues above and try again.\n")
        sys.exit(1)


if __name__ == "__main__":
    """Run validation when executed directly."""
    validate_and_exit_on_failure()
    print("\n✓ Environment validation complete!\n")