from sqlalchemy.orm import Session
from sqlalchemy import asc
import models, schemas
import uuid
from password_hashing import Hash
from fastapi import HTTPException, status

# TASK RELATED QUERIES

# need this function:
# - to check for duplicate Task IDs when creating a new task
# - to delete task by its id
def get_task_by_id(db: Session, id: str):
    return db.query(models.TaskModel).filter(models.TaskModel.task_id == id).first()

#add task for logged in user
def add_task(db: Session, task: schemas.TaskCreate, current_user: models.UserModel):
    task_id = str(uuid.uuid4())
    #checking existence of task id
    while get_task_by_id(db=db, id=task_id):
        task_id = uuid.uuid4()
    task = models.TaskModel(
        task_id=task_id,
        date = task.date,
        priority = task.priority,
        text = task.text,
        completed = task.completed,
        user_id = current_user.user_id) # need to assign user id

    db.add(task)
    db.commit()
    db.refresh(task)

# get all tasks of a LOGGED IN user
def get_tasks(db: Session, current_user: models.UserModel):
    return db.query(models.TaskModel).filter(models.TaskModel.user_id == current_user.user_id).all()

# get all tasks of all users
def get_all_tasks(db: Session):
    return db.query(models.TaskModel).all()

# delete task by id - must be logged in
def delete_task_by_id(db: Session, task_id: int, user_id:str):
    # first pull that task
    task = get_task_by_id(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")
    # check current user id matches user id in task 
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Only Task Creator Can Delete Task")
    db.delete(task)
    db.commit()
    return "task deleted"

# delete all tasks for all users
def delete_all_tasks(db: Session):
    db.query(models.TaskModel).delete()
    db.commit()

# update text content of the particular task

def update_task(db: Session, task_id: int, new_task: schemas.TaskOptional, user_id: str):
    # retrieve the task
    task = get_task_by_id(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")
    # task text can be updated by the user who created it
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Only Task Creator Can Delete Task")
    # can change text, priority and completed if passed
    print("NEW TASK ALL!", new_task)
    print("PRIORITY!", new_task.priority)
    if new_task.text!=None: task.text = new_task.text 
    if new_task.priority!=None: task.priority = new_task.priority 
    if new_task.completed!=None: task.completed = new_task.completed 

    # need to reorder tasks
     # retrieve all tasks of the user
    # tasks = db.query(models.TaskModel).filter(models.TaskModel.user_id == user_id).all()
     # order ascendingly
    # tasks.order_by(models.TaskModel.priority.asc())
    db.commit()
    return "task updated!"



# USER RELATED QUERIES

# we need this function to check for duplicate User IDs when creating a new user
def get_user_by_id(db: Session, id: str):
    return db.query(models.UserModel).filter(models.UserModel.user_id == id).first()

# need for user login and registration
def get_user_by_username(db: Session, username: str):
    return db.query(models.UserModel).filter(models.UserModel.username == username).first()

# need for registration - to check if email aready registered
def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def add_user(db: Session, user: schemas.UserCreate):
    user_id =  str(uuid.uuid4())
    
    #checking if such ID already exists:
    while get_user_by_id(db=db, id = user_id):
        user_id =  str(uuid.uuid4())

    #hashing password
    password = Hash.get_hashed_password(user.password)
    
    #adding to Model - SQL table
    new_user = models.UserModel(
    user_id=user_id,
    email = user.email,
    name = user.name,
    username = user.username,
    password = password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#getting all users
def get_users(db: Session):
    return db.query(models.UserModel).all()

#deleting all users
def delete_all_users(db: Session):
    db.query(models.UserModel).delete()
    db.commit()