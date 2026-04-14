import json
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    @contextmanager
    def _open_data_file(self, mode: str):
        with Path(DATA_FILE).open(mode, encoding="utf-8") as file:
            yield file

    def _validate_book_data(
        self, title: object, author: object, year: object, read: object = False
    ) -> tuple[str, str, int, bool]:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("author must be a non-empty string")
        if not isinstance(year, int) or isinstance(year, bool) or year < 0:
            raise ValueError("year must be a non-negative integer")
        if not isinstance(read, bool):
            raise ValueError("read must be a boolean")

        return title.strip(), author.strip(), year, read

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with self._open_data_file("r") as f:
                data = json.load(f)
                self.books = [book for book in (self._load_book_entry(b) for b in data) if book is not None]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def _load_book_entry(self, raw_book: object) -> Optional[Book]:
        if not isinstance(raw_book, dict):
            return None

        try:
            title, author, year, read = self._validate_book_data(
                raw_book["title"],
                raw_book["author"],
                raw_book["year"],
                raw_book.get("read", False),
            )
        except (KeyError, ValueError):
            return None

        return Book(title=title, author=author, year=year, read=read)

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        with self._open_data_file("w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        title, author, year, _ = self._validate_book_data(title, author, year)
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return [book for book in self.books if book is not None]

    def get_unread_books(self) -> List[Book]:
        """Return all books that are not marked as read."""
        return [book for book in self.books if book is not None and not book.read]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        query = author.lower()
        return [b for b in self.books if b is not None and query in b.author.lower()]

    def find_by_year_range(self, start_year: int, end_year: int) -> List[Book]:
        """Find all books published within an inclusive year range."""
        if not isinstance(start_year, int) or isinstance(start_year, bool) or start_year < 0:
            raise ValueError("start_year must be a non-negative integer")
        if not isinstance(end_year, int) or isinstance(end_year, bool) or end_year < 0:
            raise ValueError("end_year must be a non-negative integer")

        lower_year, upper_year = sorted((start_year, end_year))
        return [
            book
            for book in self.books
            if book is not None and lower_year <= book.year <= upper_year
        ]
