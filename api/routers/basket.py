from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from oath import get_current_user_id
import schemas

router = APIRouter()


@router.get('/basket', status_code=200, response_model=List[schemas.ShowBasket], tags=['Basket'])
def show_basket(db: Session = Depends(get_db),
                current_user_id: schemas.User = Depends(get_current_user_id)):
    basket = db.query(models.Basket).join(models.Menu, models.Basket.user_id == current_user_id).all()

    return basket


@router.get('/order_price', status_code=200, tags=['Basket'])
def order_price(db: Session = Depends(get_db),
                current_user_id: schemas.User = Depends(get_current_user_id)):
    price_in_db = db.query(models.Basket.total_cost).filter(models.Basket.user_id == current_user_id).all()
    total = []
    for el in price_in_db:
        total.append(el[0])
    return f'Общая стоимость заказа в корзине составляет {sum(total)} рублей'