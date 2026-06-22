from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.services.security import require_admin_user
from app.db import models, schemas
from app.db.database import get_db


router = APIRouter()


def _admin_user_response(user: models.User, note_count: int) -> schemas.AdminUserResponse:
    return schemas.AdminUserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        created_at=user.created_at,
        note_count=note_count,
    )


def _get_user_or_404(db: Session, user_id: int) -> models.User:
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.get("/users", response_model=list[schemas.AdminUserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(require_admin_user)
):
    del current_admin

    rows = (
        db.query(
            models.User,
            func.count(models.Note.id).label("note_count")
        )
        .outerjoin(models.Note, models.Note.user_id == models.User.id)
        .group_by(models.User.id)
        .order_by(models.User.id)
        .all()
    )

    return [
        _admin_user_response(user, note_count)
        for user, note_count in rows
    ]


@router.put("/users/{user_id}", response_model=schemas.AdminUserResponse)
def update_user(
    user_id: int,
    update: schemas.AdminUserUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(require_admin_user)
):
    user = _get_user_or_404(db, user_id)

    if update.username is not None:
        existing = (
            db.query(models.User)
            .filter(
                models.User.username == update.username,
                models.User.id != user_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        user.username = update.username

    if update.email is not None:
        existing = (
            db.query(models.User)
            .filter(
                models.User.email == update.email,
                models.User.id != user_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.email = update.email

    if update.is_admin is not None:
        if user.id == current_admin.id and not update.is_admin:
            raise HTTPException(
                status_code=400,
                detail="You cannot remove your own admin access"
            )

        user.is_admin = update.is_admin

    db.commit()
    db.refresh(user)

    note_count = (
        db.query(models.Note)
        .filter(models.Note.user_id == user.id)
        .count()
    )

    return _admin_user_response(user, note_count)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(require_admin_user)
):
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own admin account"
        )

    user = _get_user_or_404(db, user_id)

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted"
    }
