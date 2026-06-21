from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
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
    db: Session = Depends(get_db)
):
    return create_note(db, note)


@router.get("/", response_model=list[NoteResponse])
def get_notes_route(
    db: Session = Depends(get_db)
):
    return get_notes(db)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note_route(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = get_note(db, note_id)

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
    db: Session = Depends(get_db)
):
    note = update_note(
        db,
        note_id,
        update
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
    db: Session = Depends(get_db)
):
    success = delete_note(
        db,
        note_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return {
        "message": "Note deleted"
    }
