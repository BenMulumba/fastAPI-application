from fastapi import FastAPI, Body,Path,Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author =author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# create a new object to validate new request
class BookRequest(BaseModel):
    id:Optional [int] =Field(title= "id is not needed")
    title: str = Field(min_length=3)
    author:str = Field(min_length=1)
    description: str =Field (max_length= 20)
    rating: int  =Field (gt=0, lt=6)
    published_date: int =Field (gt=1999, lt=2031)


    class config:
        json_schema_extra ={
            'example': {
                'title': 'A new book',
                'author': 'Coding with BMB',
                'Description': 'a new desription of the book ',
                'rating': 5,
                'published_date': 2029
            }
        }

    
BOOKS = [
    Book(1,'Computer Science', 'Ben Mulumba', 'Good book ', 7, 2021),
    Book(2,'Fast API', 'Ben Mulumba', 'Great book ', 6, 2031),
    Book(3,'Bootstrap', 'Coding with prince', 'nice book ', 4, 2014),
    Book(4,'Django', 'savanet', 'Awasome book ', 9,2000),
    Book(5,'HTML and CSS', 'Ben Mulumba', 'Good book ', 7,2026),
    Book(6,'Jupyter ', 'Code with prince', 'Good book ', 4, 2032)
]


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_all_books ():
    return BOOKS

@app.get ('/books/{book_id}', status_code=status.HTTP_404_NOT_FOUND)
async def read_book (book_id : int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException (status_code=404, detail='Item not found ')
        

@app.get ('/books/{book_by_rating}', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_a_book (book_request:BookRequest):
    new_book = BOOKS(**book_request.dict())
    BOOKS.append(new_book)

@app.put ('books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in  range (len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book 
            book_changed= True
    if not book_changed:
        raise HTTPException(status_code=404,detail='item not found')
    

@app.delete ('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book (book_id: int =Path(gt=0)):
    book_changed = False
    for i in range (len(BOOKS)):
        if BOOKS[i].id == book_id:  
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='item not found')
    

@app.get('/books/{read_book_by_date}')
async def read_by_published_date(published_date: int = Query (gt=1999, lt=2031)):
    Books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            Books_to_return.append(book)
    return Books_to_return

