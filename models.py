from tkinter import CASCADE

from sqlalchemy.sql.expression import text
from database import Base
from sqlalchemy import TIMESTAMP, Column,Integer,String,ForeignKey

class Note(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=True)
    content=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    account_id=Column(Integer,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__="accounts"
    id=Column(Integer,nullable=False,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

