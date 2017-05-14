from minstrel.handling import simplify_dict, best_default_dict


def test_simplify_dict():
    assert simplify_dict({
        'str': 'bar',
        'bool': True,
        'int': 5,
        'none': None,
        'list': [5, 3, 2, 1, 0, -1],
    }) == {
        'str': 'foo',
        'bool': True,
        'int': 1,
        'none': None,
        'list': (0, 1, -1),
    }

def test_simplify_dict_hashable():
    hash(simplify_dict({
        'str': 'bar',
        'bool': True,
        'int': 5,
        'none': None,
        'list': [5, 3, 2, 1, 0, -1],
    }))


def test_best_default_dict():
    d1 = {
        'a': 1,
        'b': 1,
        'c': 1,
        'd': 1,
        'e': 1,
    }
    d2 = {
        'a': 1,
        'b': 1,
        'c': 1,
        'e': 1,
    }
    d3 = {
        'c': 1,
        'd': 1,
        'e': 1,
    }
    assert best_default_dict([d1, d2, d3]) == d1

    d4 = {
        'a': 1,
        'b': 1,
        'c': 1,
    }
    d5 = {
        'a': 1,
        'b': 1,
        'd': 1,
        'e': 1,
        'f': 1,
    }
    d6 = {
        'a': 1,
        'g': 1,
        'h': 1,
        'i': 1,
    }
    assert best_default_dict([d4, d5, d6]) == d4
