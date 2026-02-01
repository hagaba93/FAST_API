from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/userme',
    tags=['userme']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # return {"user.id": user.get('id'),
    #         "user.username": user.get('username'),
    #         "user.email": user.get('email'),
    #         "user.first_name": user.get('first_name'),
    #         "user.last_name": user.get('last_name'),
    #         "user.user_role": user.get('user_role')
    #         }
    return db.query(Users).filter(Users.id == user.get('id')).first()

