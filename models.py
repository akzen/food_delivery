from database import engine, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR, unique=True)
    email = Column(VARCHAR, unique=True)
    hashed_password = Column(VARCHAR, nullable=False)
    is_staff = Column(Boolean, default= False)
    is_active = Column(Boolean, default= False)
       
    orders = relationship('Order', back_populates='users')
    
    def __repr__(self):
        
        return f"<User {self.id}>"
    

class Order(Base):
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key= True)
    quantity = Column(Integer, nullable =False)
    order_status = Column(VARCHAR, default="Pending")
    pizza_size = Column(VARCHAR, default='Small')
    user_id = Column(Integer, ForeignKey("users.id"))
    
    users = relationship('User', back_populates='orders')
    
    def __repr__(self):
        
        return f"<Order {self.id}>"