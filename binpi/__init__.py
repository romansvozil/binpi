import struct
import typing
from typing import Callable


class Reader(typing.Protocol):
    def read_bytes(self, n: int):
        raise NotImplementedError


class FileReader:
    def __init__(self, file_path=None, file=None):
        self.file = file or open(file_path, "rb")

    def read_bytes(self, n: int):
        return self.file.read(n)


class BufferReader:
    offset: int
    data: bytes

    def __init__(self, data: bytes, offset: int = 0):
        self.data = data
        self.offset = offset

    def read_bytes(self, n: int):
        data = self.data[self.offset: self.offset + n]
        self.offset += n
        return data


class Writer(typing.Protocol):
    def write_bytes(self, data: bytes):
        raise NotImplementedError


class FileWriter:
    def __init__(self, file_path=None, file=None):
        self.file = file or open(file_path, "wb")

    def write_bytes(self, data: bytes):
        self.file.write(data)


class SizeCalculatorWriter:
    def __init__(self):
        self.current_size = 0

    def write_bytes(self, data: bytes):
        self.current_size += len(data)


class BufferWriter:
    def __init__(self):
        self.buffer = bytes()

    def write_bytes(self, data: bytes):
        self.buffer += data # todo: probably use byte buffer or whatever is it


class SerializableType:
    def __init__(self, *args, use_if=None, **kwargs):
        self.use_if = use_if

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        raise NotImplementedError

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        raise NotImplementedError

    def should_be_used(self, instance):
        return self.use_if is None or self.use_if(instance)


class Skip():
    ...


def create_simple_number_class(format: str, size: int) -> type[int]:
    class _inner(SerializableType):
        def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
            return struct.unpack(format, reader.read_bytes(size))[0]

        def write_from_value(self, writer: Writer, value, *args, **kwargs):
            writer.write_bytes(struct.pack(format, value))

    return _inner  # type: ignore


def create_simple_float_class(format: str, size: int) -> type[float]:
    class _inner(SerializableType):
        def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
            return struct.unpack(format, reader.read_bytes(size))[0]

        def write_from_value(self, writer: Writer, value, *args, **kwargs):
            writer.write_bytes(struct.pack(format, value))

    return _inner  # type: ignore


LEInt = create_simple_number_class("<i", 4)
LEUInt = create_simple_number_class("<I", 4)
LEShort = create_simple_number_class("<h", 2)
LEUShort = create_simple_number_class("<H", 2)
LEByte = create_simple_number_class("<b", 1)
LEUByte = create_simple_number_class("<B", 1)
LEFloat = create_simple_float_class("<f", 4)
LEDouble = create_simple_float_class("<d", 8)

BEInt = create_simple_number_class(">i", 4)
BEUInt = create_simple_number_class(">I", 4)
BEShort = create_simple_number_class(">h", 2)
BEUShort = create_simple_number_class(">H", 2)
BEByte = create_simple_number_class(">b", 1)
BEUByte = create_simple_number_class(">B", 1)
BEFloat = create_simple_float_class(">f", 4)
BEDouble = create_simple_float_class(">d", 8)


class _List(SerializableType):
    size: int | str | Callable  # todo: for more complex time the Callable argument kinda fails to provide enough
    # context about where exactly are we during deserializing, especially in nested/recursive structures
    type: type

    def __init__(self, type_, size: int | str | Callable, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.type = type_

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        result = []
        for index in range(self.get_size(instance)):
            if issubclass(self.type, SerializableType):
                result.append(self.type().load_from_bytes(reader, instance))
            else:
                result.append(deserialize(self.type, reader))

        return result

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        for val in value:
            if issubclass(self.type, SerializableType):
                self.type().write_from_value(writer, val)
            else:
                serialize(val, writer)

    def get_size(self, instance):
        return self.size \
            if type(self.size) == int \
            else self.size(instance) \
            if callable(self.size) \
            else getattr(instance, self.size)


class _String(_List):
    def __init__(self, type_ = LEUByte, size: int | str | Callable = 0, encoding: str = "utf8", **kwargs):
        super().__init__(type_=type_, size=size, **kwargs)
        self.encoding = encoding

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        result = super().load_from_bytes(reader, instance, *args, **kwargs)
        return bytes(result).decode(self.encoding)

    def write_from_value(self, writer: Writer, value: str, *args, **kwargs):
        return super().write_from_value(writer, value.encode(self.encoding), *args, **kwargs)
    

def List(type_: type, size: int | str | Callable, *args, **kwargs) -> type[typing.List]:
    # quite hacky way of doing this, but it is what it is
    return _List(type_, size, *args, **kwargs)  # type: ignore


def String(type_: type = BEUByte, size: int | str | Callable = 0, encoding: str = "utf8", *args, **kwargs) -> type[str]:
    # quite hacky way of doing this, but it is what it is
    return _String(type_, size, encoding, *args, **kwargs)  # type: ignore


def get_usable_fields(class_, first=None, last=None):
    pairs = [(attr, val) for attr, val in class_.__annotations__.items() if
            not attr.startswith("__") and not isinstance(val, Skip)]

    first_index, last_index = 0, len(pairs)
    if first is not None:
        first_index = next(i for i in range(len(pairs)) if pairs[i][0] == first)
    if last is not None:
        last_index = next(i for i in range(len(pairs)) if pairs[i][0] == last)

    return pairs[first_index: min(last_index+1, len(pairs))]


def deserialize(class_: type, reader: Reader = None, first=None, last=None, bytes=None):
    result = class_()

    if bytes:
        reader = BufferReader(bytes)

    for key, type_ in get_usable_fields(class_, first=first, last=last):
        if hasattr(type_, "load_from_bytes"):
            setattr(result, key, type_.load_from_bytes(reader, result))
        else:
            setattr(result, key, deserialize(type_, reader=reader))

    return result


def serialize(value, writer: Writer, first=None, last=None):
    for key, type_ in get_usable_fields(type(value), first=first, last=last):
        if hasattr(type_, "write_from_value"):
            type_.write_from_value(writer, getattr(value, key))
        else:
            serialize(getattr(value, key), writer=writer)


def get_serialized_size(value, first=None, last=None) -> int:
    """ Useful for archive structures that stores headers and data separately and uses offsets for reading the data """
    """ NOTE: this function is quite expensive to call on big data structures """
    writer = SizeCalculatorWriter()
    serialize(value, writer, first=first, last=last)
    return writer.current_size
