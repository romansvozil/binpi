import typing
from typing import Callable

if typing.TYPE_CHECKING:
    from .serializer import Serializer
    from .deserializer import Deserializer

DeserializedT = typing.TypeVar("DeserializedT")


LITTLE_ENDIAN = "<"
BIG_ENDIAN = ">"

class SimpleSerializableType:
    STRUCT_PATTERN: str = ""
    SIZE: int = -1

    def get_SIZE(self):
        return self.SIZE

    def get_STRUCT_PATTERN(self):
        return self.STRUCT_PATTERN


class SerializableType:
    def load_from_bytes(self, deserializer: "Deserializer", instance, *args, **kwargs):
        raise NotImplementedError

    def write_from_value(self, serializer: "Serializer", value, parent_instance, *args, **kwargs):
        raise NotImplementedError


class Skip():
    ...


def create_simple_number_class(format: str, size: int) -> type[int]:
    class _inner(SimpleSerializableType):
        STRUCT_PATTERN = format
        SIZE = size

    return _inner  # type: ignore


def create_simple_float_class(format: str, size: int) -> type[float]:
    class _inner(SimpleSerializableType):
        STRUCT_PATTERN = format
        SIZE = size

    return _inner  # type: ignore


Int: Callable[..., int] = create_simple_number_class("i", 4)
UInt: Callable[..., int] = create_simple_number_class("I", 4)
Short: Callable[..., int] = create_simple_number_class("h", 2)
UShort: Callable[..., int] = create_simple_number_class("H", 2)
Byte: Callable[..., int] = create_simple_number_class("b", 1)
UByte: Callable[..., int] = create_simple_number_class("B", 1)
Float: Callable[..., float] = create_simple_float_class("f", 4)
Double: Callable[..., float] = create_simple_float_class("d", 8)


class _Boolean(SimpleSerializableType):
    STRUCT_PATTERN = "?"
    SIZE = 1


Boolean: Callable[..., bool] = _Boolean  # type: ignore


class _WrapType:
    def __init__(self, type_):
        self.type = type_


WrapTypeT = typing.TypeVar('WrapTypeT')


def WrapType(type_: WrapTypeT) -> WrapTypeT:
    return _WrapType(type_)


class RecursiveType:
    def __init__(self):
        self.type = None
