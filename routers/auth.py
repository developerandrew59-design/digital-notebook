from fastapi import Depends,HTTPException,status,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import schemas,models,utils
from database import  get_db
from sqlalchemy.orm import Session
from Oauth2 import create_acess_token

router=APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/",response_model=schemas.Token,status_code=status.HTTP_201_CREATED)
def login_route(user_cred:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
    if not utils.verify(user_cred.password,user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid creditinals")
    token=create_acess_token(data={"user_id":user.id})

    return {"acess_token":token, "token_type": "bearer"}


