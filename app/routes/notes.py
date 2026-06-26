from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from .. import crud
from .. import schemas
from fastapi import HTTPException
from app.dependencies import get_current_user
from app import models
router=APIRouter()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/notes")
def create_note(
    note: schemas.NoteCreate,
    db: Session=Depends(get_db)
):
    return crud.create_note(db,note)



@router.get("/notes",
            response_model=list[schemas.NoteResponse])
def get_notes(
    skip: int=0,
    limit: int=10,
    db: Session=Depends(get_db),
    current_user: models.User=Depends(get_current_user)
):
    return crud.get_notes(db,skip,limit)



@router.get("/notes/search",
            response_model=list[schemas.NoteResponse])
def search_notes(
    q:str,
    db: Session=Depends(get_db)
    ):
    return crud.search_notes(db,q)

@router.get("/notes/{note_id}",
            response_model=schemas.NoteResponse)
def get_note(
    note_id: int,
    db: Session=Depends(get_db)
):
    note = crud.get_note(db,note_id)
    if note is None:
        raise HTTPException(status_code=404,
                            detail="Note not found")
    return note


@router.get(
        "/notes/category/{category}",
        response_model=list[schemas.NoteResponse]
)
def get_notes_by_category(
    category: str,
    db: Session=Depends(get_db)
):
    return crud.get_notes_by_category(
        db,
        category
    )

@router.get(
        "/notes/tag/{tag}",
        response_model=list[schemas.NoteResponse]
)
def get_notes_by_tag(
    tag: str,
    db: Session=Depends(get_db)
):
    return crud.get_notes_by_tag(
        db,
        tag
    )



@router.put("/notes/{note_id}",
            response_model=schemas.NoteResponse)
def update_note(
    note_id: int,
    note: schemas.NoteCreate,
    db: Session=Depends(get_db)
):
    updated_note=crud.update_note(
        db,note_id,note
    )
    if updated_note is None:
        raise HTTPException(status_code=404,
                            detail="Note not found")
    return updated_note



@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session=Depends(get_db)
):
    note = crud.delete_note(db,note_id)
    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    return {
        "message":"Note deleted successfully"
    }



