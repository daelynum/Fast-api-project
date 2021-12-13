from typing import Optional

from pydantic import BaseModel


class Menu(BaseModel):
    pizza: str
    price: int

    class Config:
        orm_mode = True


class AdminMenu(BaseModel):
    id: int
    pizza: str
    price: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    pizza_id: int
    count: int

    class Config:
        orm_mode = True


class ShowOrder(BaseModel):
    pizzas: Menu

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    surname: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True


class ShowBasket(BaseModel):
    pizzas: Menu
    count: int
    total_cost: int

    class Config:
        orm_mode = True


class OrderStatus(BaseModel):
    order_number_id: int
    pizzas: Menu
    creator: ShowUser

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    name: Optional[str] = None
