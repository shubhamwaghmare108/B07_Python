import re
class Book:
    def __init__(self, title: str, author: str, year: int, genre: str, availability: bool=True):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.availability = availability

    def __str__(self):
        return f"{self.title} by {self.author}, published in {self.year} [{self.genre}]"

    def __repr__(self) -> str:
        return f"Book(title={self.title}, author={self.author}, year={self.year}, genre={self.genre}, availability={self.availability})"


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self):
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        year = int(input("Enter the year of publication: "))    
        genre = input("Enter the genre of the book: ")
        availability = input("Is the book available? (yes/no): ").strip().lower()
        availability = True if availability == "yes" else False

        new_book = Book(title, author, year, genre, availability)
        book_key = new_book.title  # Use the title as the key
        book_value = {"author": new_book.author, "year": new_book.year, "genre": new_book.genre, "availability": new_book.availability}  # Store the book object in a dictionary with the author as the key
        self.books[book_key] = book_value  # Store the book object in a dictionary with the title as the key

    def remove_book(self, title: str):
        if title in self.books.keys():
            del self.books[title]

    def list_books(self):
        for book in self.books.keys():
            print(book)
        return "list_books method executed successfully."

    def search_books(self, search_term: str):
        search_str_collection = [f"{i},{j}"for i,j in library.books.items()]
        results = []
        for item in search_str_collection:
            if search_term.lower() in item.lower():
                results.append(item.split(',')[0])  # Extract the title from the formatted string
        book_details = []
        for title in self.books.keys():
            if title in results:
                book_details.append((title, self.books[title]))  # Append the book details as a tuple

        return book_details

library = Library()
library.add_book()
print(library.list_books())
print(library.search_books("26"))