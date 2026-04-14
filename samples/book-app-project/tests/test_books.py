import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    return temp_file


@pytest.fixture
def collection():
    return BookCollection()


def test_load_books_from_existing_json(use_temp_data_file):
    books_data = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "read": False},
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": True},
    ]
    use_temp_data_file.write_text(json.dumps(books_data))

    collection = BookCollection()

    assert len(collection.books) == 2
    assert collection.books[0].title == "The Hobbit"
    assert collection.books[1].read is True


def test_load_books_missing_file_starts_empty(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing_file))

    collection = BookCollection()

    assert collection.books == []


def test_load_books_with_invalid_json_warns_and_recovers(tmp_path, monkeypatch, capsys):
    broken_file = tmp_path / "data.json"
    broken_file.write_text("{not valid json")
    monkeypatch.setattr(books, "DATA_FILE", str(broken_file))

    collection = BookCollection()

    captured = capsys.readouterr()
    assert "data.json is corrupted" in captured.out
    assert collection.books == []


def test_load_books_ignores_null_and_invalid_entries(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    data_file.write_text(
        json.dumps(
            [
                {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "read": False},
                None,
                {"title": "Broken Book"},
            ]
        )
    )
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].title == "The Hobbit"


def test_save_books_writes_current_collection(use_temp_data_file, collection):
    collection.add_book("1984", "George Orwell", 1949)

    saved = json.loads(use_temp_data_file.read_text())

    assert saved == [
        {"title": "1984", "author": "George Orwell", "year": 1949, "read": False}
    ]


def test_add_book(collection):
    initial_count = len(collection.books)

    book = collection.add_book("1984", "George Orwell", 1949)

    assert len(collection.books) == initial_count + 1
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


@pytest.mark.parametrize("query", ["Dune", "DUNE", "dUnE"])
def test_find_book_by_title_is_case_insensitive(collection, query):
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.find_book_by_title(query)

    assert result is not None
    assert result.title == "Dune"


def test_find_book_by_title_missing_returns_none(collection):
    assert collection.find_book_by_title("Nonexistent Book") is None


def test_list_books_returns_current_collection(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)

    books_list = collection.list_books()

    assert books_list == collection.books


def test_list_books_empty_collection_returns_empty_list(collection):
    assert collection.list_books() == []


def test_get_unread_books_returns_only_unread_books(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")

    unread_books = collection.get_unread_books()

    assert [book.title for book in unread_books] == ["The Hobbit", "Dune"]


def test_get_unread_books_returns_empty_list_when_all_books_are_read(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("The Hobbit")
    collection.mark_as_read("1984")

    assert collection.get_unread_books() == []


def test_get_unread_books_returns_empty_list_for_empty_collection(collection):
    assert collection.get_unread_books() == []


def test_mark_book_as_read(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.mark_as_read("Dune")

    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book is not None
    assert book.read is True


def test_mark_book_as_read_persists_to_file(use_temp_data_file, collection):
    collection.add_book("Dune", "Frank Herbert", 1965)

    collection.mark_as_read("Dune")

    saved = json.loads(use_temp_data_file.read_text())
    assert saved == [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": True}
    ]


def test_mark_book_as_read_invalid(collection):
    result = collection.mark_as_read("Nonexistent Book")

    assert result is False


def test_find_by_author_matches_partial_name(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Children of Dune", "Frank Herbert", 1976)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.find_by_author("Herbert")

    assert [book.title for book in result] == ["Dune", "Children of Dune"]


@pytest.mark.parametrize("query", ["Frank Herbert", "frank herbert", "FRANK HERBERT", "frAnK hErBeRt"])
def test_find_by_author_matches_case_variations(collection, query):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Children of Dune", "Frank Herbert", 1976)

    result = collection.find_by_author(query)

    assert [book.title for book in result] == ["Dune", "Children of Dune"]


def test_find_by_author_returns_empty_list_when_no_matches(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.find_by_author("Asimov")

    assert result == []


def test_find_by_author_empty_collection_returns_empty_list(collection):
    assert collection.find_by_author("Frank Herbert") == []


def test_remove_book(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.remove_book("The Hobbit")

    assert result is True
    assert collection.find_book_by_title("The Hobbit") is None


def test_remove_book_persists_to_file(use_temp_data_file, collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    collection.remove_book("The Hobbit")

    saved = json.loads(use_temp_data_file.read_text())
    assert saved == []


def test_remove_book_invalid(collection):
    result = collection.remove_book("Nonexistent Book")

    assert result is False
