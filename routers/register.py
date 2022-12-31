from fastapi import APIRouter, Depends, HTTPException, status
from database import engine, get_db
from schemas import SignUpModel
from sqlalchemy.orm import Session
import models
from passlib.context import CryptContext
from .auth import generate_password


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

router= APIRouter(
    prefix="/register",
    tags= ["Register"],
    responses={401: {"description": "User already exists"}}
)

models.Base.metadata.create_all(bind=engine)

      
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(create_user: SignUpModel, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == create_user.username).first()
    
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists ")
    
          
    create_user_model = models.User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.is_active = create_user.is_active
    create_user_model.is_staff = create_user.is_staff
   

    hash_password = generate_password(create_user.hashed_password)

    create_user_model.hashed_password = hash_password
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
        
    return {"message": "You are registered Successfully"}
    