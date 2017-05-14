from minstrel.handlers import number_handler, string_handler, dict_handler


def test_number_handler():
    assert number_handler(set(), [0, 1, -1]) == {0, 1, 1.5, -1, -1.5}
    assert number_handler(set(), [1, -1]) == {1, 1.5, -1, -1.5}
    assert number_handler(set(), [1, 5]) == {1, 1.5}


def test_string_handler():
    assert string_handler(set(), ['', 'bar']) == {'', 'foo'}
    assert string_handler(set(), ['']) == {''}
    assert string_handler(set(), ['bar']) == {'foo'}


def test_dict_handler():
    assert dict_handler(set(), [
        {
            'foo': 1,
            'bar': 'qux',
        },
        {
            'foo': 2,
            'bar': None,
        },
    ]) == ''
