"""
LAYERED ARCHITECTURE
"Stack your code in layers. Each layer only talks to the layer below it."

Analogy: a restaurant.
  Customer -> Waiter (presentation) -> Chef (service) -> Storeroom (data)
The waiter never cooks, and the chef never takes orders from customers.

In a real project each layer would be its own module or folder:
    app/
      api/           <- presentation layer (routes, request/response)
      services/      <- business logic
      repositories/  <- data access
Here they live in one file so you can read the whole flow at once.
"""
from dataclasses import dataclass


# ===========================================================================
# LAYER 3: DATA ACCESS - "the storeroom"
# Knows HOW data is stored. Knows nothing about business rules or HTTP.
# ===========================================================================
@dataclass
class Book:
    id: int
    title: str
    copies_available: int


class BookRepository:
    def __init__(self):
        self._books = {
            1: Book(1, "Clean Code", 2),
            2: Book(2, "Python Tricks", 0),
        }

    def get(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def save(self, book: Book) -> None:
        self._books[book.id] = book


# ===========================================================================
# LAYER 2: SERVICE / BUSINESS LOGIC - "the chef"
# Knows the RULES of a library. Knows nothing about HTTP or JSON.
# ===========================================================================
class BookNotAvailable(Exception):
    pass


class BookNotFound(Exception):
    pass


class LibraryService:
    def __init__(self, books: BookRepository):
        self.books = books

    def borrow(self, book_id: int) -> Book:
        book = self.books.get(book_id)
        if book is None:
            raise BookNotFound(f"No book with id {book_id}")
        if book.copies_available == 0:  # business rule
            raise BookNotAvailable(f"'{book.title}' is out of stock")
        book.copies_available -= 1
        self.books.save(book)
        return book


# ===========================================================================
# LAYER 1: PRESENTATION / API - "the waiter"
# Turns requests into service calls and results into responses.
# No business rules here.
# ===========================================================================
class LibraryApi:
    def __init__(self, service: LibraryService):
        self.service = service

    def post_borrow(self, request: dict) -> dict:
        try:
            book = self.service.borrow(int(request["book_id"]))
            return {"status": 200, "body": {"title": book.title, "left": book.copies_available}}
        except BookNotFound as error:
            return {"status": 404, "body": {"error": str(error)}}
        except BookNotAvailable as error:
            return {"status": 409, "body": {"error": str(error)}}


if __name__ == "__main__":
    api = LibraryApi(LibraryService(BookRepository()))
    print(api.post_borrow({"book_id": "1"}))
    print(api.post_borrow({"book_id": "1"}))
    print(api.post_borrow({"book_id": "1"}))  # out of stock now
    print(api.post_borrow({"book_id": "2"}))
    print(api.post_borrow({"book_id": "99"}))

# TRADE-OFFS
# + Easy to understand and explain. The most common structure in web apps.
# + Swap the API layer (REST -> CLI) without touching business rules.
# - The service layer still depends directly on the data layer.
#   Ports & adapters (next file) removes that coupling.
# - For tiny apps, three layers can feel like ceremony.
