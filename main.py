from fastapi import FastAPI
from database import Base, engine
from routers import user, task, authorization

Base.metadata.create_all(bind=engine)


app = FastAPI()

#INCLUDING USER ROUTER
app.include_router(user.router)
#INCLUDING TASK ROUTER
app.include_router(task.router)
#INCLUDING AUTHORIZATION ROUTER
app.include_router(authorization.router)



@app.get('/', tags=["root"])
async def root():
    return "Hello World!"




