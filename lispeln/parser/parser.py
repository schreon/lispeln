from lispeln.scheme.derived import Begin

__author__ = 'schreon'

def parse(items):
    return Begin([_parse(item) for item in items])

def _parse(item):
    pass