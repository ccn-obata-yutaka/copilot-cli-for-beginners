import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_list_unread():
    books = collection.get_unread_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search_year():
    print("\nFind Books by Year Range\n")

    start_year_str = input("Start year: ").strip()
    end_year_str = input("End year: ").strip()

    try:
        start_year = int(start_year_str)
        end_year = int(end_year_str)
        books = collection.find_by_year_range(start_year, end_year)
        show_books(books)
    except ValueError as e:
        print(f"\nError: {e}\n")


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  unread   - Show only books not marked as read
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  find-year - Find books by publication year range
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    commands = {
        "list": handle_list,
        "unread": handle_list_unread,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "find-year": handle_search_year,
        "help": show_help,
    }

    handler = commands.get(command)
    if handler is None:
        print("Unknown command.\n")
        show_help()
        return

    handler()


if __name__ == "__main__":
    main()
