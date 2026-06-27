from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import schemas
from app.crud import user as user_crud
from app.auth import create_access_token

router=APIRouter(prefix="/users",tags=["Users"])
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",
             response_model=schemas.UserResponse,
             status_code=201)
def register(
    user: schemas.UserCreate,
    db: Session=Depends(get_db)
):
    if user_crud.get_user_by_username(db,user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    if user_crud.get_user_by_email(db,user.email):
        raise HTTPException(status_code=400,
                            detail="Email already exists")
    return user_crud.create_user(db,user)

@router.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session=Depends(get_db)
):
    db_user=user_crud.authenticate_user(db,user.username,user.password)
    if not db_user:
        raise HTTPException(status_code=401,
                            detail="Invalid username or password")
    access_token=create_access_token({
        "sub": db_user.username,
        "role":db_user.role
    })
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }