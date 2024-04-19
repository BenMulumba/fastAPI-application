from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel,Field
import models
from models import todos
from database import engine, SessionLocal
from typing import Annotated 
from sqlalchemy.orm import Session
from starlette import status


router = APIRouter() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# create and add data on the database
class TodoRequest(BaseModel):
    title:str =Field (min_length=3)
    description: str = Field (min_length=4)
    priority:int =Field(gt=0, lt=8)
    complete: bool



@router.get("/",status_code=status.HTTP_200_OK)
async def read_all (db:db_dependency):
    return db.query(todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_id (db: db_dependency, todo_id: int = Path (gt=0) ):
    todo_model = db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException (status_code=404, detail='Todo not found')


# create a post method to serve as record into our database
@router.post("/todo",status_code= status.HTTP_201_CREATED)

async def create_to_do (db: db_dependency, todo_request:TodoRequest):
    todo_model = todos(**todo_request.dict ())

    db.add(todo_model)
    db.commit()


# create a put request method to save as record into our database
@router.put("/todo/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def update_todo (db: db_dependency,todo_id:int, todo_request:TodoRequest):
    todo_model =db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException (status_code=404, detail='todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

# adding a delete request method
@router.delete ("todo/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(todos).filter(todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException (status_code=404, detail='todo not found')
    db.query(todos).filter(todos.id == todo_id).delete()

    db.commit()




