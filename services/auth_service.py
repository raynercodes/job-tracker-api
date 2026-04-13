from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC
from utils.auth import create_access_token, create_refresh_token
from repos.auth_repo import store_refresh_token, create_user, get_user_by_username, get_refresh_token_repo, revoke_refresh_token
from utils.logger import logger

def register_user(username, password):
    username = (username or "").strip().lower()
    password = password or ""

    created_at = datetime.now(UTC).isoformat()

    if not username:
        raise ValueError("Username required")
    
    if len(username) <= 3:
        raise ValueError("Username must be at least 4 characters")

    if not password:
        raise ValueError("Password required")
    
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    
    existing = get_user_by_username(username)
     
    if existing:
        raise ValueError("User already exists")
    
    password_hash = generate_password_hash(password)

    create_user(username, password_hash, created_at)

    logger.info(f"User registered username={username}")
    return {"username": username}

def login_user(username, password):
    username = (username or "").strip().lower()
    password = password or ""

    if not username:
        raise ValueError("Username required")

    if not password:
        raise ValueError("Password required")
    
    logger.info(f"User login attempt username={username}")

    row = get_user_by_username(username)

    if row is None:
        logger.warning(f"Invalid credentials username={username}")
        raise ValueError("Invalid credentials")
    
    user_id, password_hash = row

    is_password = check_password_hash(password_hash, password)

    if not is_password:
        logger.warning(f"Invalid credentials")
        raise ValueError("Invalid credentials")
    
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token()
    created_at = datetime.now(UTC).isoformat()

    store_refresh_token(user_id, refresh_token, created_at)

    logger.info(f"Login successful user_id={user_id}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def refresh_access_token_service(refresh_token):
    refresh_token = (refresh_token or "").strip()

    if not refresh_token:
        raise ValueError("Refresh token is required")
    
    row = get_refresh_token_repo(refresh_token)

    if row is None:
        logger.warning(f"Refresh token invalid")
        raise ValueError("Invalid refresh token")
    
    token_id, user_id, token, created_at, revoked_at = row

    if revoked_at is not None:
        logger.warning(f"Refresh token invalid")
        raise ValueError("Invalid refresh token")
    
    revoked_time = datetime.now(UTC).isoformat()

    revoke_refresh_token(refresh_token, revoked_time)
    
    access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token()
    new_created_at = datetime.now(UTC).isoformat()

    store_refresh_token(user_id, new_refresh_token, new_created_at)
    
    logger.info(f"Refresh successful user_id={user_id}")
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }