from .utils import *
from ..routers.admin import get_db, get_current_user  # type: ignore
from fastapi import status
from ..models import Todos  # type: ignore


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_admin_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'title': 'Test Todo', 'priority': 1, 'description': 'This is a test todo', 
                 'complete': False, 'owner_id': 1}]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the todo has been deleted
    db = TestSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model is None

def test_admin_delete_nonexistent_todo(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}