
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import get_db
import schemas, crud, models
from typing import List
from auth import get_current_user #to get authorized user

#CREATING A ROUTER FOR USER
router = APIRouter(
    prefix = '/task',
    tags = ['task']
)



# CREATE A TASK
@router.post("")
async def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    crud.add_task(task=task, db=db, current_user=current_user)
    return "OK"
# GET ALL TASKS OF A USER - BASED ON AUTHORIZATION
@router.get("", response_model=List[schemas.TaskDisplay])
async def get_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.get_tasks(db=db, current_user=current_user)

# GET ALL TASKS OF ALL USERS
@router.get("/all", response_model=List[schemas.TaskDisplay])
async def get__all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db=db)

# DELETE TASK BY ID
@router.get("/delete/{id}")
async def delete_task_by_id(id:str, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.delete_task_by_id(task_id=id, db=db, user_id=current_user.user_id)

# DELETE ALL TASKS IRRESPECTIVE FOR ALL USERS
@router.get("/delete")
async def delete_all_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_tasks(db=db)

