from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import UserCreate
from app.auth.service import hash_password, verify_password, create_access_token
from app.schemas import TokenResponse,LoginRequest

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(400, "User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    # username or email のどちらでログインしても OK
    if data.username:
        user = db.query(User).filter(User.username == data.username).first()
    else:
        user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": user.username, "user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


# @router.post("/login", response_model=Token)
# def login(data: UserCreate, db: Session = Depends(get_db)):

#     user = db.query(User).filter(User.email == data.email).first()
#     if not user or not verify_password(data.password, user.password_hash):
#         raise HTTPException(401, "Invalid credentials")

#     token = create_access_token({"user_id": user.id, "role": user.role})
#     return Token(access_token=token, token_type="bearer")
