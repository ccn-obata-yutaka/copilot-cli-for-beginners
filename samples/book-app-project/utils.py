from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from books import Book


@dataclass
class CollectionStats:
    total: int
    read_count: int
    unread_count: int
    oldest: "Book | None"
    newest: "Book | None"


def _prompt_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return None


def get_stats(books: list["Book"]) -> CollectionStats:
    """Return statistics for a list of Book objects."""
    if not books:
        return CollectionStats(
            total=0, read_count=0, unread_count=0, oldest=None, newest=None
        )

    read_count = sum(1 for b in books if b.read)
    books_with_year = [b for b in books if b.year > 0]

    oldest = min(books_with_year, key=lambda b: b.year) if books_with_year else None
    newest = max(books_with_year, key=lambda b: b.year) if books_with_year else None

    return CollectionStats(
        total=len(books),
        read_count=read_count,
        unread_count=len(books) - read_count,
        oldest=oldest,
        newest=newest,
    )


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = _prompt_input("Choose an option (1-5): ")
        if choice is None:
            return "5"

        choice = choice.strip()
        if choice in {"1", "2", "3", "4", "5"}:
            return choice

        print("Please enter a number from 1 to 5.")


def get_book_details() -> tuple[str, str, int]:
    title = ""
    while not title:
        raw_title = _prompt_input("Enter book title: ")
        if raw_title is None:
            return "", "", 0
        title = raw_title.strip()
        if not title:
            print("Title cannot be empty.")

    author = ""
    while not author:
        raw_author = _prompt_input("Enter author: ")
        if raw_author is None:
            return "", "", 0
        author = raw_author.strip()
        if not author:
            print("Author cannot be empty.")

    year = 0
    while True:
        year_input = _prompt_input("Enter publication year (leave blank for 0): ")
        if year_input is None:
            return "", "", 0

        year_text = year_input.strip()
        if not year_text:
            break

        try:
            year = int(year_text)
        except ValueError:
            print("Invalid year. Please enter a whole number or leave it blank.")
            continue

        if year < 0:
            print("Year cannot be negative.")
            continue

        break

    return title, author, year


def print_books(books: list["Book"]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
