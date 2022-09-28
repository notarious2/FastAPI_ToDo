from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class TaskModel(Base):
    __tablename__ = "task"
    task_id = Column(String, primary_key=True, index=True, unique=True)
    text = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("user.user_id"))
    user = relationship("UserModel", back_populates = "task")
    class Config:
        orm_mode = True

class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    task = relationship("TaskModel", back_populates = "user")
    class Config:
        orm_mode = True