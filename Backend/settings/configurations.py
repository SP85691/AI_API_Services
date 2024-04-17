from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import secrets

# Generate secret key
SECRET_KEY = secrets.token_urlsafe(32)

# Hashing algorithm SHA256
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Expiration time for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Secret key for JWT
JWT_SECRET_KEY = secrets.token_urlsafe(32)

# Algorithm for JWT
ALGORITHM = "HS256"

# Create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify access token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return False
    
# Hash password
def hash_password(password):
    return pwd_context.hash(password)

# Verify password
def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)

# Generate random password
def generate_password():
    return secrets.token_urlsafe(8)

# Generate random username
def generate_username():
    return secrets.token_urlsafe(6)

