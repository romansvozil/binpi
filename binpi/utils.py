from functools import cache
from inspect import ismethod, isfunction

from .types import Skip


@cache
def get_usable_fields(class_, first=None, last=None):
    pairs = []

    while class_ != object:
        pairs = [(attr, val) for attr, val in class_.__dict__.items() if
             not attr.startswith("__") and not isinstance(val, Skip) and not callable(val) and not ismethod(val) and not isfunction(val)] + pairs

        class_ = class_.__base__

    first_index, last_index = 0, len(pairs)
    if first is not None:
        first_index = next(i for i in range(len(pairs)) if pairs[i][0] == first)
    if last is not None:
        last_index = next(i for i in range(len(pairs)) if pairs[i][0] == last)

    return pairs[first_index: min(last_index + 1, len(pairs))]
