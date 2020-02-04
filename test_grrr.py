import pytest
from grrr import Grrr
import json

KEY = None
with open("key.json") as file:
    KEY = json.load(file)['key']

def test_not_string_key_error():
    try:
        obj = Grrr(1234)
        print(obj.key)
        assert False
    except:
        assert True

def test_key_is_alphanumeric():
    try:
        obj = Grrr("12ds!")
        print(obj.key)
        assert False
    except:
        assert True

def test_book_query():
    obj = Grrr(KEY)
    query = obj.search_by_title('The Aleph')
    assert isinstance(query, dict)

def test_book_query_save():
    obj = Grrr(KEY)
    obj.search_by_title('The Aleph', save=True)
    assert len(obj.books) > 0

def test_book_query_results():
    obj = Grrr(KEY)
    result = obj.search_by_title('The Aleph')
    year = result['year'] == 1945
    author = result['author'] == 'Jorge Luis Borges'
    title = result['title'] == 'The Aleph and Other Stories'
    assert year and author and title

def test_get_book_tags():
    obj = Grrr(KEY)
    result = obj.get_book_tags("Harry Potter and the Sorcerer's Stone")
    assert 'own' in result.keys()

def test_book_tags_count():
    obj = Grrr(KEY)
    result = obj.get_book_tags("Harry Potter and the Sorcerer's Stone")
    assert result['own'] > 20000

def test_book_reviews_type():
    obj = Grrr(KEY)
    result = obj.get_book_reviews(39088592)
    assert isinstance(result, list) and len(result) == 10 and isinstance(result[0], str) and len(result[0]) > 0
    