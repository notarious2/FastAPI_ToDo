from pydantic import BaseModel
from typing import Optional



class TaskSchema(BaseModel):
    task_id: str
    text: str
    user_id: str
    
    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    user_id: str
    email: str
    name: str
    username: str
    password: str
    # class Config:
    #     orm_mode = True

class UserDisplaySchema(BaseModel):
    name: str

    # makes links between User and UserDisplay schemas
    # class Config:
    #     orm_mode = True