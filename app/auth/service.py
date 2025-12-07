from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# ---------------------------
# 密碼雜湊（hash password）
# ---------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ---------------------------
# 密碼驗證（verify password）
# ---------------------------
def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# ---------------------------
# JWT access token 生成
# ---------------------------
def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import jwt
# import os

# SECRET_KEY = os.getenv("SECRET_KEY", "secret")
# ALGORITHM = "HS256"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def verify_password(password: str, hashed: str):
#     return pwd_context.verify(password, hashed)

# def create_access_token(data: dict, expires_minutes=60):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
