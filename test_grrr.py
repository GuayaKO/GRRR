import pytest
import grrr
import json

KEY = None
with open("key.json") as file:
    KEY = json.load(file)['key']

def test_not_string_key_error():
    try:
        obj = grrr.Grrr(1234)
        print(obj.key)
        assert False
    except:
        assert True

def test_key_is_alphanumeric():
    try:
        obj = grrr.Grrr("12ds!")
        print(obj.key)
        assert False
    except:
        assert True

def test_book_query():
    obj = grrr.Grrr(KEY)
    query = obj.search_by_title('The Aleph')
    assert isinstance(query, dict)

def test_book_query_save():
    obj = grrr.Grrr(KEY)
    obj.search_by_title('The Aleph', save=True)
    assert len(obj.books) > 0