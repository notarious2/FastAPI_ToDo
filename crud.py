from sqlalchemy.orm import Session
import models, schemas

def get_all_tasks(db: Session):
    return db.query(models.TaskModel).all()

def add_task(db: Session, task: schemas.TaskSchema):
    task = models.TaskModel(task_id=task.task_id, text = task.text, user_id = task.user_id)
    db.add(task)
    db.commit()
    db.refresh(task)

def add_user(db: Session, user: schemas.UserSchema):
    task = models.UserModel(user_id=user.user_id,
    email = user.email,
    name = user.name,
    username = user.username,
    password = user.password)
    db.add(task)
    db.commit()
    db.refresh(task)
