from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from typing import Optional
from fastapi import HTTPException

app = FastAPI()

class BookPatchDTO(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    ibsn: Optional[str] = None
    year: Optional[int] = None

class BookDTO(BaseModel):
    name: str
    author: str
    ibsn: str
    year: int

class Book(BaseModel):
    id: int
    name: str
    author: str
    ibsn: str
    year: int

books_db: List[Book] = [
    Book(id=1, name="1984", author="George Orwell", ibsn="9780451524935", year=1949),
    Book(id=2, name="To Kill a Mockingbird", author="Harper Lee", ibsn="9780060935467", year=1960),
    Book(id=3, name="The Great Gatsby", author="F. Scott Fitzgerald", ibsn="9780743273565", year=1925),
]

next_id = 4

@app.get("/books", response_model=List[Book])
def get_books():
    return books_db

@app.get("/books/{id}", response_model=Book)
def get_one_book(id: int):
    for book in books_db:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}")
def delete_one_book(id: int):
    global books_db
    original_length = len(books_db)
    books_db = [book for book in books_db if book.id != id]

    if len(books_db) == original_length:
        raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookDTO):
    global next_id
    book = Book(id=next_id, **book_data.dict())
    books_db.append(book)
    next_id += 1
    return book

@app.put("/books/{id}", response_model=Book, status_code=200)
def update_book(id: int, book_data: BookDTO):
    for index, book in enumerate(books_db):
        if book.id == id:
            updated_book = Book(id=id, **book_data.dict())
            books_db[index] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")

@app.patch("/books/{id}", response_model=Book)
def patch_book(id: int, book_data: BookPatchDTO):
    for index, book in enumerate(books_db):
        if book.id == id:
            updated_fields = book_data.dict(exclude_unset=True)
            updated_book_data = book.dict()
            updated_book_data.update(updated_fields)
            updated_book = Book(**updated_book_data)
            books_db[index] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")
