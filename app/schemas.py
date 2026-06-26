from pydantic import BaseModel, EmailStr
from datetime import datetime
class NoteCreate(BaseModel):
    title: str
    content: str
    tags: str | None=None
    category: str | None=None
class NotesResponse(NoteCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        from_attributes=True