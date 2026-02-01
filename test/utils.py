from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base # type: ignore
from ..main import app # type: ignore
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users  # type: ignore
from ..routers.auth import bcrypt_context



SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="session", autouse=True)
# def setup_test_db():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "testuser",
            "id": 1, "user_role": "admin"}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title="Test Todo", priority=1, description="This is a test todo", 
                 complete =False, owner_id=1)
    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()
        conn.close()

@pytest.fixture
def test_user():
    hashed_password = bcrypt_context.hash("testpassword")
    user = Users(username="testuser", email="testuser@example.com", 
    hashed_password=hashed_password)
    db = TestSessionLocal()
    db.add(user)    
    db.commit()
    yield user
    with engine.connect() as conn:  
        conn.execute(text("DELETE FROM users;"))
        conn.commit()
        conn.close() 

