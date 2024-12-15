import pytest

def test_add():
    assert 2 + 3 == 5
    assert -1 + 1 == 0

def test_divide_without_error():
    assert 5 / 2 == 2.5

def test_divide_error():
    with pytest.raises(ZeroDivisionError):
        10 / 0
