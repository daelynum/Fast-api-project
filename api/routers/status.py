from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from oath import get_current_user_id
import schemas

router = APIRouter()


@router.get('/status', status_code=200, response_model=list[schemas.OrderStatus], tags=['Status'])
def get_status(db: Session = Depends(get_db),
               current_user_id: schemas.User = Depends(get_current_user_id)):
    status = db.query(models.Status).filter(models.Status.user_id == current_user_id).all()
    return status
