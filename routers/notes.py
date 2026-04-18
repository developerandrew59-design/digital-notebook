
from typing import Optional
from sqlalchemy import or_
from fastapi import Depends,HTTPException,status,Response,APIRouter
import Oauth2
import schemas
import models
from database import engine, get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/notes",
    tags=['Notes']
)

@router.get("/",response_model=list[schemas.NoteReturn])
def get_all_notes(db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user),
                 lim:int=4,skip:int=0,search:Optional[str]="",bookmark: Optional[bool] = None):
    #cursor.execute("""SELECT * FROM notes""")
    #notes=cursor.fetchall()

    query=db.query(models.Note).filter(
        models.Note.account_id==current_user.id,
        or_(
            models.Note.title.contains(search),
            models.Note.content.contains(search)        
            ))

    if bookmark is not None:
        query=query.filter(models.Note.bookmark==bookmark)    

    notes=query.limit(lim).offset(skip).all()    
    return notes

@router.post("/",response_model=schemas.NoteReturn,status_code=status.HTTP_201_CREATED)
def create_note(note:schemas.NoteCreate,db: Session = Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    #cur.execute("""INSERT INTO notes (title,content) VALUES
                 #(%s,%s) RETURNING * """,
                 #(note.title,note.content) 
    #post_dict=cur.fetchone() 
    #conn.commit()
    print(current_user.id)
    note_dict=models.Note(account_id=current_user.id,**note.model_dump())
    db.add(note_dict)
    db.commit()
    db.refresh(note_dict)

    return note_dict



@router.get("/{id}",response_model=schemas.NoteReturn)
def get_one_note(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):

    #cur.execute("""SELECT * FROM notes WHERE id=%s""",str(id))
    #note=cur.fetchone()

    note=db.query(models.Note).filter(models.Note.id==id).first()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id {id} note found")
    
    if not note.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    
    return note



@router.delete("/{id}")
def delete_note(id:int,db:Session=Depends(get_db),current_user:int=Depends(Oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM notes WHERE id=%s RETURNING * """,(str(id)))    
    #deleted_note=cursor.fetchone()
    #conn.commit()

    deleted_note_query=db.query(models.Note).filter(models.Note.id==id)
    deleted_note=deleted_note_query.first()

    if deleted_note==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id {id} note found")
    
    if not deleted_note.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")
    
    deleted_note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.NoteReturn)
def update_note(id:int,note:schemas.NoteCreate,db:Session=Depends
                (get_db),current_user:int=Depends(Oauth2.get_current_user)):
    #cursor.execute(""" UPDATE notes SET title=%s,content=%s WHERE id=%s RETURNING *""",
     #              (note.title,note.content,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()

    updated_query=db.query(models.Note).filter(models.Note.id==id)
    updated_note=updated_query.first()

    if updated_note==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id {id} not found")
    
    if not updated_note.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")

    updated_query.update(note.model_dump(), synchronize_session=False)
    db.commit()
    

    return updated_query.first()