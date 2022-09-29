from sys import prefix
from fastapi import FastAPI, Depends, Request, HTTPException, status
from auth import get_current_user
import schemas
import models
import crud
import auth
from database import Base, engine
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from hashed import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


Base.metadata.create_all(bind=engine)


app = FastAPI()

#Authenticate user based on username and password
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    # find user with such username
    if not user:
        return False
    # check if passwords match
    if not Hash.verify_hashed_password(plain_password=password, hashed_password=user.password):
        return False
    return user        



@app.get('/')
async def root():
    return "Hello World!"

@app.post('/login', tags = ["Authentication"])
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
   user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
   if not user:
    raise HTTPException(
       	status_code=status.HTTP_401_UNAUTHORIZED,
       	detail="Incorrect email or password",
       	headers={"WWW-Authenticate": "Bearer"},
   	)
   access_token = auth.create_access_token(data={"username": user.username}) 
   return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username
    }




#CREATE A TASK
@app.post("/tasks")
async def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    crud.add_task(task=task, db=db, current_user=current_user)
    return "OK"
#GET ALL TASKS OF A USER
@app.get("/tasks", response_model=List[schemas.TaskDisplay])
async def get_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.get_tasks(db=db, current_user=current_user)

@app.get("/tasks/delete")
async def delete_all_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_tasks(db=db)

@app.post("/user", response_model=schemas.UserDisplay)
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.add_user(user=user, db=db)
    

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.get("/users/delete")
async def delete_all_users(db: Session = Depends(get_db)):
    return crud.delete_all_users(db=db)