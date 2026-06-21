from sqlalchemy.orm import Session

from .models import Note
from .schemas import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate):

    db_note = Note(
        title=note.title,
        content=note.content
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def get_note(db: Session, note_id: int):

    return (
        db.query(Note)
        .filter(Note.id == note_id)
        .first()
    )


def get_notes(db: Session):

    return db.query(Note).all()


def update_note(
    db: Session,
    note_id: int,
    update: NoteUpdate
):

    note = get_note(db, note_id)

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
    note_id: int
):

    note = get_note(db, note_id)

    if not note:
        return False

    db.delete(note)
    db.commit()

    return True