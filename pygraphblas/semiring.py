import re, sys
from itertools import chain

from .base import lib

class Semiring:

    def __init__(self, name, semiring):
        self.name = name
        self.semiring = semiring

    def __enter__(self):
        return self

    def __exit__(self, *errors):
        return False

non_boolean_re = re.compile('^GxB_(MIN|MAX|PLUS|TIMES)_(FIRST|SECOND|MIN|MAX|PLUS|MINUS|RMINUS|TIMES|DIV|RDIV|ISEQ|ISNE|ISGT|ISLT|ISGE|ISLE|LOR|LAND|LXOR)_(INT64|FP64)$')

boolean_re = re.compile('^GxB_(LOR|LAND|LXOR|EQ)_(EQ|NE|GT|LT|GE|LE)_(INT64|FP64)$')

pure_bool_re = re.compile('^GxB_(LOR|LAND|LXOR|EQ)_(FIRST|SECOND|LOR|LAND|LXOR|EQ|GT|LT|GE|LE)_BOOL$')

def ring_group(reg):
    return [Semiring(n.string[4:].lower(), getattr(lib, n.string))
            for n in filter(None, [reg.match(i) for i in dir(lib)])]

def build_semirings():
    this = sys.modules[__name__]
    for r in chain(ring_group(non_boolean_re), ring_group(boolean_re), ring_group(pure_bool_re)):
        setattr(this, r.name, r)