import struct
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

    def get_SIZE(self):
        return struct.calcsize(self.get_STRUCT_PATTERN())

    def get_STRUCT_PATTERN(self):
        return self.STRUCT_PATTERN


class SerializableType:
    def load_from_bytes(self, deserializer: "Deserializer", instance, *args, **kwargs):
        raise NotImplementedError

    def write_from_value(self, serializer: "Serializer", value, parent_instance, *args, **kwargs):
        raise NotImplementedError


class Skip():
    ...


def create_simple_number_class(format: str) -> type[int]:
    class _inner(SimpleSerializableType):
        STRUCT_PATTERN = format

    return _inner  # type: ignore


def create_simple_float_class(format: str) -> type[float]:
    class _inner(SimpleSerializableType):
        STRUCT_PATTERN = format

    return _inner  # type: ignore


Int: Callable[..., int] = create_simple_number_class("i")
UInt: Callable[..., int] = create_simple_number_class("I")
Short: Callable[..., int] = create_simple_number_class("h")
UShort: Callable[..., int] = create_simple_number_class("H")
Byte: Callable[..., int] = create_simple_number_class("b")
UByte: Callable[..., int] = create_simple_number_class("B")
Float: Callable[..., float] = create_simple_float_class("f")
Double: Callable[..., float] = create_simple_float_class("d")


class _Boolean(SimpleSerializableType):
    STRUCT_PATTERN = "?"


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
