from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
import models
from oath import get_current_user_id
import schemas

router = APIRouter()


@router.post('/choose_pizza', status_code=status.HTTP_201_CREATED, tags=['Order'])
def choose_pizza(request: schemas.Order, db: Session = Depends(get_db),
          current_user_id: schemas.User = Depends(get_current_user_id)):
    pizza = db.query(models.Menu).filter(models.Menu.id == request.pizza_id).first()

    order = models.Basket(user_id=current_user_id,
                          pizza_id=pizza.id,
                          count=request.count,
                          total_cost=pizza.price * request.count)
    db.add(order)
    db.commit()
    db.refresh(order)
    return f'{pizza.pizza} добавлена в заказ'


@router.post('/order', status_code=200, response_model=list[schemas.OrderStatus], tags=['Order'])
def make_an_order(db: Session = Depends(get_db),
                  current_user_id: schemas.User = Depends(get_current_user_id)):
    basket = db.query(models.Basket).filter(models.Basket.user_id == current_user_id)
    for row in basket.all():
        new_order = models.Status(user_id=current_user_id,
                                  pizza_id=row.pizza_id,
                                  created_at=func.now())
        db.add(new_order)
    db.commit()
    while len(basket.all()) > 0:
        basket.delete(synchronize_session=False)
    db.commit()
    return db.query(models.Status).filter(models.Status.user_id == current_user_id).all()