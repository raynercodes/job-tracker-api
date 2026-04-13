from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
import secrets
import jwt
from datetime import datetime, UTC, timedelta
from flask import request, g
from functools import wraps

def create_access_token(user_id):
    expiration = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "user_id": user_id,
        "exp": expiration
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

def create_refresh_token():
    return secrets.token_hex(32)

def require_access_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise ValueError("Missing authorization header")
        
        if not auth_header.startswith("Bearer "):
            raise ValueError("Invalid authorization format")
        
        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            raise ValueError("Missing access token")
        
        try: 
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Access token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid access token")
        
        g.user_id = payload["user_id"]

        return f(*args, **kwargs)
    
    return wrapper
