from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import SECRET_KEY,ALGORITHM
from app import models
oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/users/login"
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(
        token: str=Depends(oauth2_scheme),
        db: Session=Depends(get_db)
):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,details="Invalid")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    user=(db.query(models.User).filter(models.User.username==username).first())
    if user is None:
        raise HTTPException(status_code=401,detail="User not found")
    return user

def get_current_admin(current_user: models.User=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user