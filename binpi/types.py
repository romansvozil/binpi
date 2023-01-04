import typing
from typing import Callable

if typing.TYPE_CHECKING:
    from .serializer import Serializer
    from .deserializer import Deserializer

DeserializedT = typing.TypeVar("DeserializedT")


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

    def write_from_value(self, serializer: "Serializer", value, *args, **kwargs):
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


LEInt: Callable[..., int] = create_simple_number_class("<i", 4)
LEUInt: Callable[..., int] = create_simple_number_class("<I", 4)
LEShort: Callable[..., int] = create_simple_number_class("<h", 2)
LEUShort: Callable[..., int] = create_simple_number_class("<H", 2)
LEByte: Callable[..., int] = create_simple_number_class("<b", 1)
LEUByte: Callable[..., int] = create_simple_number_class("<B", 1)
LEFloat: Callable[..., float] = create_simple_float_class("<f", 4)
LEDouble: Callable[..., float] = create_simple_float_class("<d", 8)

BEInt: Callable[..., int] = create_simple_number_class(">i", 4)
BEUInt: Callable[..., int] = create_simple_number_class(">I", 4)
BEShort: Callable[..., int] = create_simple_number_class(">h", 2)
BEUShort: Callable[..., int] = create_simple_number_class(">H", 2)
BEByte: Callable[..., int] = create_simple_number_class(">b", 1)
BEUByte: Callable[..., int] = create_simple_number_class(">B", 1)
BEFloat: Callable[..., float] = create_simple_float_class(">f", 4)
BEDouble: Callable[..., float] = create_simple_float_class(">d", 8)


class _Boolean(SimpleSerializableType):
    STRUCT_PATTERN = "<?"
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
