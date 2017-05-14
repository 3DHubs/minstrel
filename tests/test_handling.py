from functools import partial
import pytest
from unittest import mock
from minstrel.handling import handle_values

_handler_dict = {
    (int,): lambda *_: {'foo'},
    (str,): lambda *_: {'bar'},
}

bound_handle_values = partial(handle_values, handler_dict=_handler_dict)


@mock.patch('minstrel.handling.WeightedSet', new=set)
def test_handle_values():
    assert bound_handle_values([0, 1]) == {'foo'}
    assert bound_handle_values(['', 'boo']) == {'bar'}
    assert bound_handle_values([None, 'boo']) == {None, 'bar'}

    with pytest.raises(TypeError):
        assert bound_handle_values([0.1])
