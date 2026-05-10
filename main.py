from fastapi import Depends, FastAPI,HTTPException,status,Response

import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from routers import notes,users,auth

app = FastAPI()

app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")

def new_func():
    return {"message":"hello world"}











    