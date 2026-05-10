import pytest
import schemas


def test_get_all_notes(authorized_client,test_all_notes):
    response=authorized_client.get("/notes/")
    def validate(note):
        return schemas.NoteReturn(**note)
    notes_map=map(validate,response.json())
    notes_list=list(notes_map)
    assert len(response.json())==len(test_all_notes)
    assert response.status_code==200


def test_unauthorized_user_acess_all_notes(client,test_all_notes):
    response=client.get("/notes")
    assert response.status_code==401

def test_unauthorized_user_acess_single_notes(client,test_all_notes):
    response=client.get(f"/notes/{test_all_notes[0].id}")
    assert response.status_code==401 

def test_get_one_note_not_exists(authorized_client):
    response=authorized_client.get("/notes/8943")
    assert response.status_code==404

def test_get_one_note(authorized_client,test_all_notes):
    response=authorized_client.get(f"/notes/{test_all_notes[0].id}")
    note=schemas.NoteReturn(**response.json())
    
    assert note.id==test_all_notes[0].id
    assert note.content==test_all_notes[0].content
    assert response.status_code==200



@pytest.mark.parametrize("title,content,bookmark",
                        [("fighter jets","F-16,F-22,F-25",True),
                        ("API frameworks","django,fastapi,flask",False),
                        ("junk food","pizza,chips,burger",True)])
def test_create_one_note(authorized_client,test_all_notes,title,content,bookmark,test_users):
    response=authorized_client.post("/notes/",json={"title":title,"content":content,"bookmark":bookmark})
    
    new_note=schemas.NoteReturn(**response.json())
    assert new_note.title==title
    assert new_note.content==content
    assert new_note.bookmark==bookmark
    assert response.status_code==201

def test_create_note_default_bookmark_False(authorized_client,test_users):
    response=authorized_client.post("/notes",json={"title":"fake title","content":"fake content"})
    new_post=schemas.NoteCreate(**response.json())
    assert new_post.bookmark==False
    assert response.status_code==201

def test_unauthorized_user_create_note(client):
    response=client.post("/notes",json={"title":"fake title","content":"fake content"})
    assert response.status_code==401

def test_unauthorized_user_deleting_note(client,test_all_notes):
    response=client.delete(f"/notes/{test_all_notes[0].id}")
    assert response.status_code==401 

def test_authorized_user_deleting_note(authorized_client,test_all_notes):
    response=authorized_client.delete(f"/notes/{test_all_notes[0].id}")
    assert response.status_code==204    

def test_authorized_user_deleting_note_non_exitent(authorized_client):
    response=authorized_client.delete("/notes/8229348")
    assert response.status_code==404    


def test_update_note_authorized_user(authorized_client,test_users,test_all_notes):

    data={"title":"updated note",
    "content":"updated contents"}

    response=authorized_client.put(f"/notes/{test_all_notes[0].id}",json=data)
    updated_post=schemas.NoteReturn(**response.json())
    assert updated_post.title==data['title']
    assert updated_post.content==data["content"]
    assert response.status_code==200

def test_unauthorized_user_updating_note(client,test_users,test_all_notes):
    response=client.put(f"/notes/{test_all_notes[0].id}") 
    assert response.status_code==401   


def test_authorized_user_updating_note_non_exitent(authorized_client):
    data={"title":"updated post",
    "content":"updated contents"}
    response=authorized_client.put(f"/notes/7323939",json=data)
    assert response.status_code==404    