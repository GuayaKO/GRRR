import pytest
import grrr

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

def test_correct_key_accepted():
    obj = grrr.Grrr("123ABC")
    assert True