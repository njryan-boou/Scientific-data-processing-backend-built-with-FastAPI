from sqlalchemy.orm import Session

from .models import Note
from .schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate, user_id: int):

    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=user_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def get_note(db: Session, note_id: int, user_id: int):

    return (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == user_id
        )
        .first()
    )


def get_notes(db: Session, user_id: int):

    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .all()
    )


def update_note(
    db: Session,
    note_id: int,
    update: NoteUpdate,
    user_id: int
):

    note = get_note(db, note_id, user_id)

    if not note:
        return None

    if update.title is not None:
        note.title = update.title

    if update.content is not None:
        note.content = update.content

    db.commit()
    db.refresh(note)

    return note


def delete_note(
    db: Session,
    note_id: int,
    user_id: int
):

    note = get_note(db, note_id, user_id)

    if not note:
        return False

    db.delete(note)
    db.commit()

    return True
