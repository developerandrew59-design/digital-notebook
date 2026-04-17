from config import settings
from jose import JWTError, jwt
from schemas import TokenData
import models
from database import get_db
from datetime import datetime, timezone,timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

SECRET_KEY= settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_acess_token(data:dict):
    encode=data.copy()
    expiry_time=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expiry_time})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_acess_token(token:str,creds_execcptions):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if id is None:
            raise creds_execcptions
        token_data=TokenData(id=id)
    except JWTError:
        raise creds_execcptions 

    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    creds_execcptions=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credintinals",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token=verify_acess_token(token,creds_execcptions)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user

   
        
