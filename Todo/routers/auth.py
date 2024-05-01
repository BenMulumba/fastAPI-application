from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException   
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext# (installing bcrypt and passlib to implement hashed password)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer #  to use it as a dependency injection for APIs
from jose import jwt, JWTError




router = APIRouter()

#for each JWT we will need a secret key and an algorithm
SECRET_KEY = 'a207e60c0dd9c2a8d765d84d394e070d' 
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


class CreateUserRequest (BaseModel):
    username : str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class TOKEN (BaseModel):
    access_token : str
    token_type : str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# creating a new function for user authentication
def authenticate_user (username: str,password:str, db):
    user = db.query(Users).filter(Users.username == username).first() #here we're gonna take only the first reponse 
    if not user: #means if the user is empty or none
        return False
    if not bcrypt_context.verify(password, user.hashed_password):  #check if the password is correct 
        return False
    return user


def create_access_token (username:str, user_id:int, expires_delta:timedelta):
    #create information to include inside our JWT
    encode = { 'sub': username, 'id': user_id} # to use it as json token
    expires = datetime.utcnow() + expires_delta #when this token is no longer authprised
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_curent_user (token:Annotated[str, Depends(oauth2_bearer)]):#this function is to be used for security when verifying the token that is beeing pasted in 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = str = payload.get('sub')
        user_id = int = payload.get ('id')
        
        if username is None or user_id is None:
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate')    
        return {'username': username, 'id':user_id}
    
    except JWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate')    
      




@router.post('/auth/')
async def create_user (db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users (
        email= create_user_request.email,
        username =create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password), #the hash method uses algorithm that hides the user password
        is_active = True,
        role = create_user_request.role,
    )
    db.add(create_user_model)
    db.commit()



# creating a Json token for authentication
@router.post ("/token", response_model =TOKEN)
async def log_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency): #this is what generate the authomated request body for user auth.
    user = authenticate_user (form_data.username,form_data.password, db)
    if not user:
        return 'Failed Authentication'
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type':'bearer' }
    
    
