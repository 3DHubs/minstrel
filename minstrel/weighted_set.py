from collections import OrderedDict


class WeightedSet:

    _values = None
    _index = 0

    def __init__(self, values=()):
        self._values = OrderedDict(values)
        self._sort()

    def __iter__(self):
        for key in self._values:
            yield key

    def __next__(self):
        if self._index == len(self._values):
            raise StopIteration

        value = list(self._values.keys())[self._index]
        self._index += 1
        return value

    def __len__(self):
        return len(self._values)

    def __hash__(self):
        return hash(tuple(self))

    def _add(self, value):
        if value not in self._values:
            self._values[value] = 0
        self._values[value] += 1

    def add(self, value):
        self._add(value)
        self._sort()

    def add_multiple(self, values):
        for value in values:
            self._add(value)
        self._sort()

    def _sort(self):
        self._values = OrderedDict(sorted(
            self._values.items(),
            key=lambda i: i[1],
            reverse=True,
        ))
