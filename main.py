from fastapi import FastAPI, Depends
import schemas
import models
import crud
from database import Base, engine
from sqlalchemy.orm import Session
from database import get_db


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get('/')
async def root():
    return "Hello World!"


@app.post("/tasks")
def add_task(task: schemas.TaskSchema, db: Session = Depends(get_db)):
    crud.add_task(task=task, db=db)


@app.post("/user")
def add_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    crud.add_user(user=user, db=db)
    return "OK"