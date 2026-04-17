from fastapi import Depends,HTTPException,status,Response,APIRouter
import schemas
import models,Oauth2
from database import get_db
from sqlalchemy.orm import Session
from utils import hash

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=hash(user.password)
    user.password=hashed_password
    user_dict=models.User(**user.model_dump())
    db.add(user_dict)
    db.commit()
    db.refresh(user_dict)

    return user_dict

@router.get("/",response_model=list[schemas.UserOut])
def get_all_users(db:Session=Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    users=db.query(models.User).all()

    return users

@router.get("/{id}",response_model=schemas.UserOut)
def get_one_user(id:int,db:Session=Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user