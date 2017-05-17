import pytest
from minstrel.handling import handle_dicts


def test_handle_dicts():
    d1 = {
        "a": 5,
        "b": None,
    }
    d2 = {
        "a": 4,
        "b": None,
    }
    d3 = {
        "a": -1,
        "b": None,
    }

    base, derivatives = handle_dicts([d1, d2, d3])
    assert len(derivatives) == 1


def test_nested_dicts():
    d1 = {
        "a": {
            "e": 1,
            "f": None,
        },
    }
    d2 = {
        "a": {
            "e": 1,
            "f": 1,
        },
    }
    d3 = d2.copy()

    base, derivatives = handle_dicts([d1, d2, d3])
    assert len(derivatives) == 1

    d4 = {
        "a": {
            "c": True,
            "d": "hello",
        },
    }

    d5 = d3.copy()

    base, derivatives = handle_dicts([d1, d2, d3, d4, d5])
    assert len(derivatives) == 2
    assert base == d1 or base == d2 or base == d3
    assert d4 in derivatives


def test_arrays():
    d1 = {
        "b": [1, 4, 3],
    }
    d2 = {
        "b": [],
    }
    d3 = {
        "b": [4, 2],
    }
    d4 = {
        "b": ['a', 'b', 1],
    }

    base, derivatives = handle_dicts([d1, d2, d3, d4])
    assert len(derivatives) == 2
