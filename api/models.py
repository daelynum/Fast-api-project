from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship

from database import Base


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, index=True)
    pizza = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    basket = relationship("Basket", lazy='joined', back_populates="pizzas")
    status = relationship("Status", lazy='joined', back_populates="pizzas")


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)

    basket = relationship("Basket", lazy='joined', back_populates="creator")
    status = relationship("Status", lazy='joined', back_populates="creator")


class Basket(Base):
    __tablename__ = 'shopping_basket'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    count = Column(Integer, nullable=False)
    total_cost = Column(Integer, nullable=False)

    pizzas = relationship('Menu', lazy='joined', back_populates='basket')
    creator = relationship("Users", lazy='joined', back_populates="basket")


class Status(Base):
    __tablename__ = 'order_status'

    order_number_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    created_at = Column(DATETIME, nullable=False)

    pizzas = relationship('Menu', lazy='joined', back_populates='status')
    creator = relationship("Users", lazy='joined', back_populates="status")