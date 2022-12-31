from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    hashed_password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra ={
            'example':{
                "username": "Abinaya001",
                "email": "abinaya@gmail.com",
                "hashed_password": "Password@1",
                "is_staff": False,
                "is_active": True
            }
        }

class LoginModel(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class Order(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str]
    pizza_size: Optional[str]
    user_id: Optional[int]
    
    class Config:
        orm_mode = True
        schema_extra={
            "example": {
                "quantity": 2,
                "order_status": 'Pending',
                "pizza_size": 'Small'               
            }
        }
    
