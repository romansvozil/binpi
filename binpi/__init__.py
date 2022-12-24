import struct
from typing import Callable


class Reader:
    def read_bytes(self, n: int):
        raise NotImplementedError


class FileReader(Reader):
    def __init__(self, file_path=None, file=None):
        self.file = file if file is not None else open(file_path, "rb")

    def read_bytes(self, n: int):
        return self.file.read(n)


class BufferReader(Reader):
    offset: int
    data: bytes

    def __init__(self, data: bytes, offset: int = 0):
        self.data = data
        self.offset = offset

    def read_bytes(self, n: int):
        data = self.data[self.offset: self.offset + n]
        self.offset += n
        return data


class Writer:
    def write_bytes(self, data: bytes):
        raise NotImplementedError


class FileWriter(Writer):
    def __init__(self, file_path=None, file=None):
        self.__file = file or open(file_path, "wb")

    def write_bytes(self, data: bytes):
        self.__file.write(data)


class SizeCalculatorWriter(Writer):
    def __init__(self):
        self.current_size = 0

    def write_bytes(self, data: bytes):
        self.current_size += len(data)


class SerializableType:
    def __init__(self, *args, use_if=None, **kwargs):
        self.use_if = use_if

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        raise

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        raise NotImplementedError

    def should_be_used(self, instance):
        return self.use_if is None or self.use_if(instance)


class Skip():
    ...


def create_simple_class(format: str, size: int) -> type:
    class _inner(SerializableType):
        def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
            return struct.unpack(format, reader.read_bytes(size))[0]

        def write_from_value(self, writer: Writer, value, *args, **kwargs):
            writer.write_bytes(struct.pack(format, value))

    return _inner


LEInt = create_simple_class("<i", 4)
LEUInt = create_simple_class("<I", 4)
LEShort = create_simple_class("<h", 2)
LEUShort = create_simple_class("<H", 2)
LEByte = create_simple_class("<b", 1)
LEUByte = create_simple_class("<B", 1)

BEInt = create_simple_class(">i", 4)
BEUInt = create_simple_class(">I", 4)
BEShort = create_simple_class(">h", 2)
BEUShort = create_simple_class(">H", 2)
BEByte = create_simple_class(">b", 1)
BEUByte = create_simple_class(">B", 1)


class List(SerializableType):
    __size: int | str | Callable
    __type: type

    def __init__(self, type_: type, size: int | str | Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__size = size
        self.__type = type_

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        result = []
        for index in range(self.get_size(instance)):
            if issubclass(self.__type, SerializableType):
                result.append(self.__type().load_from_bytes(reader, instance))
            else:
                result.append(deserialize(self.__type, reader))

        return result

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        for val in value:
            if issubclass(self.__type, SerializableType):
                self.__type().write_from_value(writer, val)
            else:
                serialize(val, writer)

    def get_size(self, instance):
        return self.__size \
            if type(self.__size) == int \
            else self.__size(instance) \
            if callable(self.__size) \
            else getattr(instance, self.__size)


def deserialize(class_: type, reader: Reader):
    result = class_()

    for key, type_ in [(attr, val) for attr, val in class_.__annotations__.items() if
                       not callable(val) and not attr.startswith("__") and not isinstance(val, Skip)]:
        setattr(result, key, type_.load_from_bytes(reader, result))

    return result


def serialize(value, writer: Writer):
    for key, type_ in [(attr, val) for attr, val in type(value).__annotations__.items() if
                       not callable(val) and not attr.startswith("__") and not isinstance(val, Skip)]:
        type_.write_from_value(writer, getattr(value, key))


def get_deserialized_size(value) -> int:
    writer = SizeCalculatorWriter()
    serialize(value, writer)
    return writer.current_size
