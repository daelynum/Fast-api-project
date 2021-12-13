import uvicorn
from fastapi import FastAPI

from database import engine
from routers import order, basket, status, admin, authentification, user
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(order.router)
app.include_router(basket.router)
app.include_router(status.router)
app.include_router(admin.router)
app.include_router(authentification.router)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host='127.0.0.1', port=8000)