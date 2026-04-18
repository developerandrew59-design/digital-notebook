from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class NoteBase(BaseModel):
    title:str
    content:str
    bookmark: Optional[bool] = False

class NoteCreate(NoteBase):
    pass

class NoteReturn(NoteCreate):
    id:int
    created_at:datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at: datetime   

class Token(BaseModel):
    acess_token:str
    token_type:str

class TokenData(BaseModel):
    id:int | None = None