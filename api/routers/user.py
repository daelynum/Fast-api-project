from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from starlette import status

import schemas
from database import get_db
import models
from hashing import Hash

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.Users(name=request.name,
                            surname=request.surname,
                            email=request.email,
                            password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
