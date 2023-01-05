import struct
import typing

if typing.TYPE_CHECKING:
    from .deserializer import Deserializer
    from .serializer import Serializer

from .types import SerializableType, DeserializedT, SimpleSerializableType, UByte


class _List(SerializableType):
    size: int | str | typing.Callable
    type: type[DeserializedT]

    def __init__(self, type_, size: int | str | typing.Callable, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.type = type_

    def load_from_bytes(self, deserializer: "Deserializer", instance, *args, **kwargs):
        result = []

        if isinstance(self.type, SimpleSerializableType):
            size = self.get_size(instance)
            if size == 0:
                return result
            pattern = self.type.get_STRUCT_PATTERN()
            full_pattern = deserializer.endianness + str(size) + pattern
            bytes = deserializer.reader.read_bytes(size * self.type.get_SIZE())
            return list(struct.unpack(full_pattern, bytes))

        for index in range(self.get_size(instance)):
            if isinstance(self.type, SerializableType):
                result.append(self.type.load_from_bytes(deserializer, instance,
                                                        parent_custom_type=kwargs.get("parent_custom_type", None)))
            else:
                result.append(deserializer.deserialize(self.type, parent_custom_type=kwargs.get("parent_custom_type", None)))

        return result

    def write_from_value(self, serializer: "Serializer", value, parent_instance, *args, **kwargs):
        if isinstance(self.type, SimpleSerializableType):
            size = len(value)
            if size == 0:
                return
            pattern = self.type.get_STRUCT_PATTERN()
            full_pattern = serializer.endianness + str(size) + pattern

            serializer.writer.write_bytes(struct.pack(full_pattern, *value))
            return

        for val in value:
            if isinstance(self.type, SerializableType):
                self.type.write_from_value(serializer, val, parent_instance)
            else:
                serializer.serialize(val, *args, **kwargs)

    def get_size(self, instance):
        return self.size \
            if type(self.size) == int \
            else self.size(instance) \
            if callable(self.size) \
            else getattr(instance, self.size)


class _ByteArray(SerializableType):
    def __init__(self, size):
        self.size = size

    def get_size(self, instance):
        if isinstance(self.size, int): return self.size
        if isinstance(self.size, str): return getattr(instance, self.size)
        return self.size(instance)

    def load_from_bytes(self, deserializer: "Deserializer", instance, *args, **kwargs):
        return deserializer.reader.read_bytes(self.get_size(instance))

    def write_from_value(self, serializer: "Serializer", value, *args, **kwargs):
        serializer.writer.write_bytes(value)

class _String(_List):
    def __init__(self, type_=UByte(), size: int | str | typing.Callable = 0, encoding: str = "utf8", **kwargs):
        super().__init__(type_=type_, size=size, **kwargs)
        self.encoding = encoding

    def load_from_bytes(self, deserializer: "Deserializer", instance, *args, **kwargs):
        result = super().load_from_bytes(deserializer, instance, *args, **kwargs)
        return bytes(result).decode(self.encoding)

    def write_from_value(self, serializer: "Serializer", value: str, parent_instance, *args, **kwargs):
        return super().write_from_value(serializer, value.encode(self.encoding), parent_instance, *args, **kwargs)


ListItemT = typing.TypeVar("ListItemT")


def List(type_: type[ListItemT] | ListItemT, size: int | str | typing.Callable, *args, **kwargs) -> typing.List[ListItemT]:
    # quite hacky way of doing this, but it is what it is
    return _List(type_, size, *args, **kwargs)  # type: ignore

def ByteArray(size: int | str | typing.Callable, *args, **kwargs) -> bytearray:
    # quite hacky way of doing this, but it is what it is
    return _ByteArray(size, *args, **kwargs)  # type: ignore


def String(type_: type = UByte(), size: int | str | typing.Callable = 0, encoding: str = "utf8", *args, **kwargs) -> str:
    # quite hacky way of doing this, but it is what it is
    return _String(type_, size, encoding, *args, **kwargs)  # type: ignore