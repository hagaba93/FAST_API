

# from http.client import UNAUTHORIZED
# from pydoc import text

from ..routers.todos import get_db, get_current_user  # type: ignore
# from ..routers.auth import get_current_user  # type: ignore

from fastapi import status

from ..models import Todos  # type: ignore
from .utils import * 



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

 

def test_read_all_authenticated(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == [{'id': 1, 'title': 'Test Todo', 'priority': 1, 'description': 'This is a test todo', 
                 'complete': False, 'owner_id': 1}] 

# def test_read_one_authenticated(test_todo):
#     response = client.get("todos/todo/1")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {'complete': False, 'title': 'Test Todo',
#                                 'description': 'This is a test todo', 'id': 1,
#                                 'priority': 1, 'owner_id': 1}

    

def test_read_one_authenticated(test_todo: Todos):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    # assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'id': 1, 'title': 'Test Todo', 'priority': 1, 'description': 'This is a test todo', 
                 'complete': False, 'owner_id': 1}
    
def test_read_one_unauthenticated(test_todo: Todos):
    response = client.get("/todos/todo/999")
    # assert response.status_code == status.HTTP_200_OK
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not meant."}
    # assert response.json() == {'Authentication Failed'}
 

def test_create_todo(test_todo: Todos):
    # todo_data = {
    #     "title": "New Todo",
    #     "description": "This is a new todo",
    #     "complete": False,
    # }

    request_data = {
         'title': 'kytr',
            'description' : ' our Column(String) kytr',
            'priority': 3,
                'complete': False}
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

# # FAILED TodoApp3/test/test_todos.py::test_create_todo - assert 422 == 201
    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description') 
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
#     # 


def test_update_todo(test_todo: Todos):
    update_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo",
        "priority": 2,
        "complete": True,
    }
    response = client.put("/todos/todo/1", json=update_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == update_data.get("title")
    assert model.description == update_data.get("description")
    assert model.priority == update_data.get("priority")
    assert model.complete == update_data.get("complete")


def test_update_todo_not_found(test_todo: Todos):
    update_data = {
        "title": "Updated Todo",
        "description": "This is an updated todo",
        "priority": 2,
        "complete": True,
    }
    response = client.put("/todos/todo/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}


def test_delete_todo(test_todo: Todos):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo: Todos):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}

