from ast import List
from urllib import response
from config import settings
import schemas
import pytest
from config import settings
from jose import jwt
from models import User

def test_root(client):
    response=client.get("/")
    print(response.json().get("message"))

    assert response.json().get("message")=="hello world"
    assert response.status_code==200

def test_create_user(client):
    response=client.post("/users",json={"email":"hello523@email.com","password":"password123"}) 
    print(response.json())
    new_user=schemas.UserOut(**response.json())

    assert new_user.email=="hello523@email.com"
    assert response.status_code==201

def test_login_user(client,test_users):
    response=client.post("/login",data={"username":test_users['email'],"password":test_users['password']})
    page=schemas.Token(**response.json())
    payload=jwt.decode(page.acess_token,settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert id==test_users['id']
    assert response.status_code==201
    assert page.token_type=="bearer"

@pytest.mark.parametrize("email,password,status_code",
                         [("wrong@gmail.com","some",403),
                          ("laptop@gmail.com","wrong",403),
                          ("wrong@gmail.com","wrong",403),
                          (None,"wrong",422),
                          ("laptop@gmail.com",None,422)])
def test_failed_login(client,email,password,status_code):
    response=client.post("/login",data={"username":email,"password":password})
    
    assert response.status_code==status_code

def test_get_one_user(authorized_client,test_users):
    response=authorized_client.get(f"/users/{test_users['id']}") 
    note=schemas.UserOut(**response.json())

    assert response.status_code==200
    assert note.email==test_users['email']

def test_get_all_users(authorized_client,test_users):
    response=authorized_client.get("/users")
    def validate(user):
        return schemas.UserOut(**user)
    users_map=map(validate,response.json())
    users_list=List(users_map)

    assert response.status_code==200
    assert users_list   

    
    









   
