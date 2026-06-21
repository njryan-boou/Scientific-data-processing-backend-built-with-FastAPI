from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.services.security import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.db.schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse
)
from app.db.crud import (
    create_note,
    get_note,
    get_notes,
    update_note,
    delete_note
)

router = APIRouter()


@router.post("/", response_model=NoteResponse)
def create_note_route(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_note(db, note, current_user.id)


@router.get("/", response_model=list[NoteResponse])
def get_notes_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_notes(db, current_user.id)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note_route(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = get_note(db, note_id, current_user.id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.put("/{note_id}",
            response_model=NoteResponse)
def update_note_route(
    note_id: int,
    update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = update_note(
        db,
        note_id,
        update,
        current_user.id
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.delete("/{note_id}")
def delete_note_route(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_note(
        db,
        note_id,
        current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {
        "message": "Note deleted"
    }
