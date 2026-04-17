from fastapi import Depends, FastAPI,HTTPException,status,Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from routers import notes,users,auth

while True:
    try:
        conn=psycopg2.connect( host="db",
        database="mydb",
        user="postgres",
        password="mysecretpassword",
        port=5432,
        cursor_factory=RealDictCursor)

        cursor=conn.cursor()
        print("Database connection was sucessful")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error",error)
        time.sleep(2)    

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(notes.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")

def new_func():
    return {"message":"hello world"}











    