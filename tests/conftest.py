from fastapi.testclient import TestClient
from main import app
from config import settings
import models,schemas
from database import  get_db,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from Oauth2 import create_acess_token
import pytest

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingsessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingsessionLocal()
    try:
        yield db
    finally:
        db.close()   

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) 

@pytest.fixture()
def test_users(client):
    user_data={"email":"laptop@gmail.com",
               "password":"api"}
    response=client.post("/users",json=user_data) 
    user=response.json()
    user['password']=user_data['password']
    assert response.status_code==201
    return user           

@pytest.fixture()
def test_token(test_users):
    return create_acess_token({"user_id":test_users['id']})

@pytest.fixture()
def authorized_client(client,test_token,test_users):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }

    return client

@pytest.fixture()
def test_all_notes(test_users,session):
    notes_data = [
        {"title": "first title", "content": "first content", "account_id": test_users['id']},
        {"title": "second title", "content": "second content", "account_id": test_users['id']},
        {"title": "third title", "content": "third content", "account_id": test_users['id']},
        {"title": "fouth title", "content": "fourth content", "account_id": test_users['id']}]
    
    def create_test_note_model(note):
            return models.Note(**note)
    
    notemap=map(create_test_note_model,notes_data)
    notes=list(notemap)  


    session.add_all(notes)

    session.commit()

    notes=session.query(models.Note).all()
    return notes
