from minstrel.weighted_set import WeightedSet

simple_set = ('a', 3), ('b', 2), ('c', 1)


def _iter_in_order(iterator, values):
    options = iter(values)
    for n in iterator:
        assert n == next(options)


def test_initialisation():
    WeightedSet(simple_set)


def test_iter():
    w = WeightedSet(simple_set)
    _iter_in_order(w, ('a', 'b', 'c'))


def test_len():
    w = WeightedSet(simple_set)
    assert len(w) == 3


def test_hashable():
    w = WeightedSet(simple_set)
    y = WeightedSet(simple_set)
    z = WeightedSet((('a', 1),))

    assert hash(w) == hash(y)
    assert hash(w) != hash(z)


def test_next():
    w = WeightedSet(simple_set)
    assert next(w) == 'a'
    assert next(w) == 'b'
    assert next(w) == 'c'


def test_add():
    w = WeightedSet(simple_set)
    w.add('b')
    w.add('b')
    _iter_in_order(w, ('b', 'a', 'c'))
