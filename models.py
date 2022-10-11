from sqlalchemy import Column, DateTime, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=False)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    todos = relationship("TaskModel", back_populates = "owner")
    # class Config:
    #     orm_mode = True

class TaskModel(Base):
    __tablename__ = "task"
    task_id = Column(String, primary_key=True, index=True, unique=True)
    text = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("user.user_id"))
    date = Column(DateTime)
    owner = relationship("UserModel", back_populates = "todos")
    # class Config:
    #     orm_mode = True

