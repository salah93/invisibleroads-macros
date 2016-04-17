from collections import Callable, OrderedDict


class OrderedDefaultDict(OrderedDict):
    # http://stackoverflow.com/a/6190500/192092

    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
                not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (
            self.default_factory, OrderedDict.__repr__(self))


def flatten(list_of_lists):
    # http://stackoverflow.com/a/952952/192092
    return [item for sublist in list_of_lists for item in sublist]


def merge_dictionaries(*ds):
    'Overwrite duplicate keys with subsequent keys to produce a dictionary'
    # http://stackoverflow.com/a/26853961
    x = {}
    for d in ds:
        x.update(d)
    return x


def get_lists_from_tuples(xs):
    'Convert tuples to lists'
    # http://stackoverflow.com/a/1014669
    if isinstance(xs, (list, tuple)):
        return list(map(get_lists_from_tuples, xs))
    return xs
