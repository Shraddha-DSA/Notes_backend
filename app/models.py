from email.policy import default
from operator import index
from turtle import back

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Note(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    
    content=Column(String,nullable=False)

    tags=Column(String)

    category=Column(String)

    created_at=Column(DateTime,
                      default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,
                      onupdate=datetime.utcnow)


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False,index=True)
    email=Column(String,unique=True,nullable=False,index=True)
    hashed_password=Column(String,nullable=False)
    role=Column(String,default="user",nullable=False)
    notes=relationship("Note",back_populates="owner")
    