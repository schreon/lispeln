import collections
import logging

from lispeln.scheme.symbol import Symbol


__author__ = 'schreon'


class Environment(collections.MutableMapping):

    def __init__(self, parent, *args, **kwargs):
        logging.info("Creating new environment")
        self.parent = parent
        # convert keys to symbols
        self.store = dict()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        key = self.keytransform(key)
        self.store[key] = value

    def __getitem__(self, key):
        key = self.keytransform(key)
        # if the item is in this environment, fine ...
        try:
            return self.store[key]
        except KeyError:
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
        if isinstance(key, Symbol):
            return key.value
        else:
            return key