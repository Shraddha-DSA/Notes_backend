from sqlalchemy.orm import Session
from app import models
from app import schemas
from sqlalchemy import or_


def create_note(db: Session,note: schemas.NoteCreate):
    db_note=models.Note(
        title=note.title,
        content=note.content,
        tags=note.tags,
        category=note.category
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session,
              skip: int=0,
              limit: int=10):
    return(

     db.query(models.Note)
     .offset(skip)
     .limit(limit)
     .all()
     )


def get_note(db: Session,note_id: int):
    return (db.query(models.Note).filter(models.Note.id==note_id).first())


def update_note(db: Session,note_id:int,note: schemas.NoteCreate):
    db_note=get_note(db,note_id)
    if db_note:
        db_note.title=note.title
        db_note.content=note.content
        db_note.tags=note.tags
        db_note.category=note.category
        db.commit()
        db.refresh(db_note)
    return db_note


def search_notes(db,query: str):
    return (
        db.query(models.Note).filter(
            or_(
                models.Note.title.ilike(f"%{query}%"),
                models.Note.content.ilike(f"%{query}%")
            )
        ).all()
    )

def get_notes_by_category(
        db,
        category: str
):
    return (
        db.query(models.Note).filter(
            models.Note.category==category
        ).all()
    )
def get_notes_by_tag(
        db,
        tag: str
):
    return (
        db.query(models.Note).filter(
            models.Note.tags.contains(tag)
        ).all()
    )