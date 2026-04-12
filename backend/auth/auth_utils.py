from datetime import datetime, timedelta
from jose import jwt, JWTError
import hashlib
from fastapi import Header, HTTPException

SECRET_KEY = "aadya_secret"
ALGORITHM = "HS256"


# ✅ SAME hashing as CRUD (VERY IMPORTANT)
def hash_password(password: str):
    return pwd_context.hash(password)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    # Try bcrypt first
    try:
        if pwd_context.verify(plain, hashed):
            return True
    except:
        pass

    # Fallback to SHA256
    sha256_hash = hashlib.sha256(plain.encode()).hexdigest()
    return sha256_hash == hashed

# ✅ JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def require_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
