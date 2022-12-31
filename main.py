from fastapi import FastAPI
from routers import auth, register,orders

# from .routers import auth, orders, users
app = FastAPI()


app.include_router(register.router)
app.include_router(auth.router)
app.include_router(orders.router)   