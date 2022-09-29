from fastapi import FastAPI, Depends, Request, HTTPException, status
import crud
import auth
from database import Base, engine
from sqlalchemy.orm import Session
from database import get_db
from hashed import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from routers import user, task

Base.metadata.create_all(bind=engine)


app = FastAPI()

#INCLUDING USER ROUTER
app.include_router(user.router)
#INCLUDING TASK ROUTER
app.include_router(task.router)
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



@app.get('/', tags=["root"])
async def root():
    return "Hello World!"

@app.post('/login', tags = ["authentication"])
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



