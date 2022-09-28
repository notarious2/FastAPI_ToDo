from fastapi import FastAPI, Depends, Request
import schemas
import models
import crud
from database import Base, engine
from sqlalchemy.orm import Session
from database import get_db
from typing import List

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get('/')
async def root():
    return "Hello World!"


@app.post("/tasks")
async def add_task(task: schemas.TaskSchema, db: Session = Depends(get_db)):
    crud.add_task(task=task, db=db)
    return "OK"

@app.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db=db)

@app.get("/tasks/delete")
async def delete_all_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_tasks(db=db)

@app.post("/user")
async def add_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    crud.add_user(user=user, db=db)
    return "User Added" 

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@app.get("/users/delete")
async def delete_all_users(db: Session = Depends(get_db)):
    return crud.delete_all_users(db=db)