from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import get_db
import schemas, crud
from typing import List

#CREATING A ROUTER FOR USER
router = APIRouter(
    prefix = '/user',
    tags = ['user']
)


#CREATE A USER
@router.post("", response_model=schemas.UserDisplay)
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.add_user(user=user, db=db)
    
#GET ALL USERS
@router.get("", response_model=List[schemas.UserDisplay])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

#DELETED ALL USERS
@router.get("/delete")
async def delete_all_users(db: Session = Depends(get_db)):
    return crud.delete_all_users(db=db)