from sqlalchemy.orm import Session
import models, schemas
import uuid
from password_hashing import Hash
import datetime

# TASK RELATED QUERIES

#need this function to check for duplicate Task IDs when creating a new task
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
        date = datetime.datetime.now(),
        text = task.text,
        user_id = current_user.user_id) # need to assign user id

    db.add(task)
    db.commit()
    db.refresh(task)

#get all tasks of a LOGGED IN user
def get_tasks(db: Session, current_user: models.UserModel):
    return db.query(models.TaskModel).filter(models.TaskModel.user_id == current_user.user_id).all()

#get all tasks of all users
def get_all_tasks(db: Session):
    return db.query(models.TaskModel).all()

#delete all tasks for all users
def delete_all_tasks(db: Session):
    db.query(models.TaskModel).delete()
    db.commit()


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