from fastapi import Body, FastAPI 
app = FastAPI()

books = [
    {'title':'title one', 'author' : 'Jean ', 'category': 'science'},
    {'title':'title two', 'author' : 'Seguin', 'category': 'math'},
    {'title':'title three', 'author' : "Mosie", 'category': 'Music'},
    {'title':'title four', 'author' : 'claver', 'category': 'dance'},
    {'title':'title five', 'author' : 'Jean', 'category': 'math'},
    {'title':'title six', 'author' : 'Jeremi', 'category': 'science'}
]

@app.get("/")
async def read_all_books ():
    return books


@app.get ("/books/{book_title}")
async def author_name (author: str):
    for author_name in books:
        if author_name.get('author').casefold() == author.casefold():
            return author_name
        

@app.get ("/books/")
async def read_books_by_query (category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category:str):
    books_to_retourn = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and\
            book.get('category').casefold() == category.casefold():
              books_to_retourn.append(book)
    return books_to_retourn


#  Post method
@app.post("/books/create_book")
async def create_book (new_book=Body()):
    books.append(new_book)


# PUT REQUEST METHOD
@app.put ("books/update_book")
async def update_book (updated_book = Body()):
    for i in range (len(books)):
        if books[i].get('title').casefold() == updated_book.get('title').casefold():
            books[i] = updated_book


# DELETE REQUEST METHOD
@app.delete ("books/delete_book/{book_title}")
async def delete_book (book_title = str):
    for i in range (len(books)):
        if books [i].get ('title').casefold() == book_title.casefold():
            books.pop(i)