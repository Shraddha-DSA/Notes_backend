from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import hash_password
from app.auth import verify_password

def get_user_by_username(db: Session,username: str):
    return (
        db.query(models.User).filter(models.User.username==username).first()
    )
def get_user_by_email(db: Session,email: str):
    return (
        db.query(models.User).filter(models.User.email==email).first()
    )
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd=hash_password(user.password)
    db_user=models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def authenticate_user(
        db: Session,
        username: str,
        password: str
):
    user=get_user_by_username(db,username)
    if not user:
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user