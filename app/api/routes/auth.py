from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.services.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password
)
from app.db import models, schemas
from app.db.database import get_db

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # Check if username or email already exists
    existing = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists")
        
    is_first_user = db.query(models.User).count() == 0

    # Create new user
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        is_admin=is_first_user
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login")
def login(
    data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_admin": user.is_admin
    }


@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user
