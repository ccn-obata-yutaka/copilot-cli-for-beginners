import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


def test_handle_list_unread_shows_only_unread_books(tmp_path, monkeypatch, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")
    monkeypatch.setattr(book_app, "collection", collection)

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "1984" not in output and "The Hobbit" in output and "Dune" in output


def test_handle_list_unread_empty_collection_shows_no_books_message(tmp_path, monkeypatch, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()
    monkeypatch.setattr(book_app, "collection", collection)

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "No books found." in output


def test_main_dispatches_unread_command(monkeypatch):
    called = []

    def fake_handle_list_unread():
        called.append(True)

    monkeypatch.setattr(book_app, "handle_list_unread", fake_handle_list_unread)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "unread"])

    book_app.main()

    assert called == [True]


def test_handle_search_year_shows_matching_books(tmp_path, monkeypatch, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr("builtins.input", lambda prompt="": "1937" if "Start" in prompt else "1965")

    book_app.handle_search_year()

    output = capsys.readouterr().out
    assert "The Hobbit" in output and "Dune" in output and "Neuromancer" not in output


def test_main_dispatches_find_year_command(monkeypatch):
    called = []

    def fake_handle_search_year():
        called.append(True)

    monkeypatch.setattr(book_app, "handle_search_year", fake_handle_search_year)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "find-year"])

    book_app.main()

    assert called == [True]


def test_show_help_includes_unread_command(capsys):
    book_app.show_help()

    output = capsys.readouterr().out
    assert "unread   - Show only books not marked as read" in output
    assert "find-year - Find books by publication year range" in output
