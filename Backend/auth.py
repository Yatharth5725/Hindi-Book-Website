from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import bcrypt
import os
import secrets
import re
from dotenv import load_dotenv

load_dotenv()

# Generate a secure secret key if not provided
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Generate a secure random key for development
    SECRET_KEY = secrets.token_urlsafe(32)
    print("WARNING: Using generated SECRET_KEY. Set SECRET_KEY in .env for production!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

# Password validation regex
PASSWORD_PATTERN = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

security = HTTPBearer()

def create_access_token(data: dict):
    """Create a secure JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),  # Issued at
        "type": "access"  # Token type
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode JWT token with enhanced security"""
    if not token or not isinstance(token, str):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    # Basic token format validation
    if not token.count('.') == 2:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Additional security checks
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token verification failed")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    # Ensure required fields exist
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return payload

def get_current_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated admin user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    # Ensure required fields exist
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # Check admin privileges
    if not payload.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return payload

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength and return (is_valid, error_message)"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not PASSWORD_PATTERN.match(password):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@$!%*?&)"
    
    return True, ""

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Validate password strength
    is_valid, error_msg = validate_password_strength(password)
    if not is_valid:
        raise ValueError(error_msg)
    
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    if not password or not hashed_password:
        return False
    
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False
