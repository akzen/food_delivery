from fastapi import APIRouter, Depends, HTTPException, status
import models
from schemas import Order
from database import engine, get_db
from sqlalchemy.orm import Session
from .auth import get_current_user, token_exception, get_user_exception


router= APIRouter(
    tags= ["Orders"],
    responses={404: {"description": "Orders Not found"}}
)

models.Base.metadata.create_all(bind=engine)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(order: Order, user: dict= Depends(get_current_user), db: Session = Depends(get_db)):
    
    if not user:
        raise token_exception()
    new_order = models.Order()
    new_order.quantity= order.quantity
    new_order.order_status = order.order_status
    new_order.pizza_size = order.pizza_size
    new_order.user_id = user.get("id")
       
    db.add(new_order)
    db.commit()
    
    return "Order created successfully"

@router.get("/orders")
async def read_all_orders_super_user(user: dict = Depends(get_current_user), db:Session= Depends(get_db)):
    if models.User.is_staff == 1:
        return db.query(models.Order).all()
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a super user to access the orders")

@router.get("/order")
async def read_order(user: dict= Depends(get_current_user), db: Session= Depends(get_db)):
    if user is None:
        raise get_user_exception()
       
    return db.query(models.Order).filter(models.Order.user_id == user.get("id")).all()


# @router.get("/order/by_status")
# async def read_order(order: Order, db: Session= Depends(get_db)):
     
#     order_details = db.query(models.Order).filter(models.Order.user_id == user.get("id")).all()
    
#     if order_details.order_status ==  Order.order_status:
#         return order_details.order_status
    

@router.get("/order/{order_id}")
async def read_order_by_id(order_id: int, user: dict= Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if order_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found")
    
@router.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, 
                       order: Order, user: dict= Depends(get_current_user), db: Session = Depends(get_db)):
    
    if not user:
        raise get_user_exception()
    
    try:    
        if models.User.is_staff == 1 or (models.User.id == user.get("id")):
            order_update = db.query(models.Order).filter(models.Order.id == order_id)\
                .filter(models.Order.user_id == user.get("id")).first()
        
            if order_update is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        
            order_update.quantity= order.quantity
            order_update.order_status = order.order_status
            order_update.pizza_size = order.pizza_size
            order_update.user_id = user.get("id")
            db.add(order_update)
            db.commit()
            
            return " Order updated successfully"
        else:
            return "You dont have any orders to update, please create new Order!"
            
    except: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized to update the order")   

@router.delete("/{order_id}")
async def delete_todo(order_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    try:
        if models.User.is_staff == 1 or (models.User.id == user.get("id")):
            order_data = db.query(models.Order)\
                .filter(models.Order.id == order_id)\
                .filter(models.Order.user_id == user.get("id"))\
                .first()

            if order_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your are not authorized")

            db.query(models.Order)\
                .filter(models.Order.id == order_id)\
                .delete()

            db.commit()
            return "Successfully deleted the Order"
        
        else: 
            return "You dont have any orders to delete or you are not authorized"
        
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not authorized to update the order")  