import collections
from lispeln.expressions import Symbol


class Environment(collections.MutableMapping):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        # convert keys to symbols
        self.store = dict()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self.store[self.keytransform(key)] = value

    def __getitem__(self, key):
        key = self.keytransform(key)

        # if the item is in this environment, fine ...
        if key in self.store:
            return self.store[key]
        if self.parent is not None:
            return self.parent[key]
        else:
            return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __delitem__(self, key):
        del self.store[self.keytransform(key)]

    def keytransform(self, key):
        return Symbol(key)