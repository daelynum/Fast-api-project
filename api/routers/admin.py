from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
import models
from oath import get_current_user_id
import schemas

router = APIRouter()


@router.get('/pizza', status_code=200, response_model=List[schemas.AdminMenu], tags=['Admin'])
def all_pizzas(db: Session = Depends(get_db),
               current_user_id: schemas.User = Depends(get_current_user_id)):
    """Show all pizzas with id"""
    menu = db.query(models.Menu).all()
    if current_user_id == 1:
        return menu
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This rout for admin only')


@router.post('/pizza', status_code=status.HTTP_201_CREATED, tags=["Admin"])
def new_pizza(request: schemas.Menu, db: Session = Depends(get_db),
              current_user_id: schemas.User = Depends(get_current_user_id)):
    """Create pizza"""
    new_pizza = models.Menu(pizza=request.pizza,
                            price=request.price)
    if current_user_id == 1:
        db.add(new_pizza)
        db.commit()
        db.refresh(new_pizza)
        return new_pizza
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This rout for admin only')


@router.delete('/pizza/{pizza_id}', tags=["Admin"])
def delete_pizza(pizza_id, db: Session = Depends(get_db),
                 current_user_id: schemas.User = Depends(get_current_user_id)):
    """Delete pizza"""
    pizza = db.query(models.Menu).filter(models.Menu.id == pizza_id).first()
    if current_user_id == 1:
        if not pizza:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'pizza with id {pizza_id} not found')
        else:
            db.query(models.Menu).filter(models.Menu.id == pizza_id).delete(synchronize_session=False)
        db.commit()
        return {'information': f'pizza with id {pizza_id} deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This rout for admin only')


@router.put('/pizza/{pizza_id}', tags=["Admin"])
def update_pizza(pizza_id, request: schemas.Menu, db: Session = Depends(get_db),
                 current_user_id: schemas.User = Depends(get_current_user_id)):
    """Update pizza"""
    pizza = db.query(models.Menu).filter(models.Menu.id == pizza_id).first()
    if current_user_id == 1:
        if not pizza:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'pizza with id {pizza_id} not found')
        else:
            db.query(models.Menu).filter(models.Menu.id == pizza_id).update({
                "pizza": request.pizza,
                "price": request.price
            }, synchronize_session='evaluate')
        db.commit()
        return {'information': f'pizza with id {pizza_id} updated successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This rout for admin only')


@router.get('/users/{user_id}', status_code=200, response_model=schemas.ShowUser, tags=['Admin'])
def show_user(user_id: int, db: Session = Depends(get_db),
              current_user_id: schemas.User = Depends(get_current_user_id)):
    one_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if current_user_id == 1:
        if not one_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} is not available')
        return one_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This rout for admin only')


@router.delete('/order/{user_id}', status_code=200, tags=['Admin'])
def complete_an_order(user_id: int, db: Session = Depends(get_db),
                   current_user_id: schemas.User = Depends(get_current_user_id)):
    order = db.query(models.Status).filter(models.Status.user_id == user_id).all()
    if current_user_id == 1:
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'order for user {user_id} not found')
        else:
            db.query(models.Status).filter(models.Status.user_id == user_id).delete(synchronize_session=False)
        db.commit()
        return {'information': f'order for user {user_id} finished'}