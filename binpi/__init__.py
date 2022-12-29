import struct
import typing
from dataclasses import dataclass
from functools import cache
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
        self.buffer = bytearray()

    def write_bytes(self, data: bytes):
        self.buffer.extend(data)


class SimpleSerializableType:
    STRUCT_PATTERN: str = ""
    SIZE: int = -1

    def get_SIZE(self):
        return self.SIZE

    def get_STRUCT_PATTERN(self):
        return self.STRUCT_PATTERN


class SerializableType:
    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        raise NotImplementedError

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        raise NotImplementedError


@cache
def get_usable_fields(class_, first=None, last=None):
    pairs = [(attr, val) for attr, val in class_.__dict__.items() if
             not attr.startswith("__") and not isinstance(val, Skip) and not callable(val)]

    first_index, last_index = 0, len(pairs)
    if first is not None:
        first_index = next(i for i in range(len(pairs)) if pairs[i][0] == first)
    if last is not None:
        last_index = next(i for i in range(len(pairs)) if pairs[i][0] == last)

    return pairs[first_index: min(last_index + 1, len(pairs))]


DeserializedT = typing.TypeVar("DeserializedT")


@dataclass
class Plan:
    pattern: str
    total_size: int
    fields: list[str]
    serializable_type: typing.Optional[SerializableType] = None
    type_: typing.Optional[type[DeserializedT]] = None

    def read_using_plan(self, reader: Reader, instance, parent_custom_type=None):
        if self.type_ is not None:
            setattr(instance, self.fields[0], deserialize(self.type_, reader=reader, parent_custom_type=parent_custom_type))
        elif self.serializable_type is not None:
            setattr(instance, self.fields[0],
                    self.serializable_type.load_from_bytes(reader, instance, parent_custom_type=parent_custom_type))
        else:
            vals = struct.unpack(self.pattern, reader.read_bytes(self.total_size))
            for field, value in zip(self.fields, vals):
                setattr(instance, field, value)

    def write_using_plan(self, writer: Writer, instance, parent_custom_type=None):
        if self.type_ is not None:
            serialize(getattr(instance, self.fields[0]), writer=writer, parent_custom_type=parent_custom_type)
        elif self.serializable_type is not None:
            self.serializable_type.write_from_value(writer, getattr(instance, self.fields[0]), parent_custom_type=parent_custom_type)
        else:
            fields_to_write = [getattr(instance, field) for field in self.fields]
            data_to_write = struct.pack(self.pattern, *fields_to_write)
            writer.write_bytes(data_to_write)


@cache
def generate_deserializing_plans(type_: type, first=None, last=None):
    plans = []
    plan = None

    for key, val in get_usable_fields(type_, first, last):
        if isinstance(val, SimpleSerializableType):
            if plan is None:
                plan = Plan("", 0, [])

            plan.pattern += val.STRUCT_PATTERN[1:] if plan.pattern else val.STRUCT_PATTERN # todo: do something with the endinianity
            plan.total_size += val.SIZE
            plan.fields.append(key)
        else:
            if plan is not None:
                plans.append(plan)
                plan = None

            if isinstance(val, SerializableType):
                if isinstance(val, RecursiveType):
                    val = type_
                plans.append(Plan(pattern="", total_size=0, fields=[key], serializable_type=val))
                continue

            if isinstance(val, RecursiveType):
                val = type_
            plans.append(Plan(pattern="", total_size=0, fields=[key], type_=val))

    if plan is not None:
        plans.append(plan)

    return plans


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
    STRUCT_PATTERN = "?"
    SIZE = 1


Boolean: Callable[..., bool] = _Boolean  # type: ignore


class RecursiveType:
    def __init__(self):
        self.type = None


class _List(SerializableType):
    size: int | str | Callable
    type: type[DeserializedT]

    def __init__(self, type_, size: int | str | Callable, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.type = type_

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        result = []

        if isinstance(self.type, SimpleSerializableType):
            size = self.get_size(instance)
            if size == 0:
                return result
            pattern = self.type.get_STRUCT_PATTERN()
            full_pattern = pattern[0] + str(size) + pattern[1:] # todo: again the endianity is annoying
            bytes = reader.read_bytes(size * self.type.get_SIZE())
            return list(struct.unpack(full_pattern, bytes))

        for index in range(self.get_size(instance)):
            if isinstance(self.type, SerializableType):
                result.append(self.type.load_from_bytes(reader, instance,
                                                        parent_custom_type=kwargs.get("parent_custom_type", None)))
            else:
                result.append(deserialize(self.type, reader, parent_custom_type=kwargs.get("parent_custom_type", None)))

        return result

    def write_from_value(self, writer: Writer, value, *args, **kwargs):
        if isinstance(self.type, SimpleSerializableType):
            size = len(value)
            if size == 0:
                return
            pattern = self.type.get_STRUCT_PATTERN()
            full_pattern = pattern[0] + str(size) + pattern[1:] # todo: the endinianity is annoying

            writer.write_bytes(struct.pack(full_pattern, *value))
            return

        for val in value:
            if isinstance(self.type, SerializableType):
                self.type.write_from_value(writer, val)
            else:
                serialize(val, writer)

    def get_size(self, instance):
        return self.size \
            if type(self.size) == int \
            else self.size(instance) \
            if callable(self.size) \
            else getattr(instance, self.size)


class _String(_List):
    def __init__(self, type_=LEUByte, size: int | str | Callable = 0, encoding: str = "utf8", **kwargs):
        super().__init__(type_=type_, size=size, **kwargs)
        self.encoding = encoding

    def load_from_bytes(self, reader: Reader, instance, *args, **kwargs):
        result = super().load_from_bytes(reader, instance, *args, **kwargs)
        return bytes(result).decode(self.encoding)

    def write_from_value(self, writer: Writer, value: str, *args, **kwargs):
        return super().write_from_value(writer, value.encode(self.encoding), *args, **kwargs)


ListItemT = typing.TypeVar("ListItemT")


def List(type_: type[ListItemT] | ListItemT, size: int | str | Callable, *args, **kwargs) -> typing.List[ListItemT]:
    # quite hacky way of doing this, but it is what it is
    return _List(type_, size, *args, **kwargs)  # type: ignore


def String(type_: type = BEUByte(), size: int | str | Callable = 0, encoding: str = "utf8", *args, **kwargs) -> str:
    # quite hacky way of doing this, but it is what it is
    return _String(type_, size, encoding, *args, **kwargs)  # type: ignore


class _WrapType:
    def __init__(self, type_):
        self.type = type_


WrapTypeT = typing.TypeVar('WrapTypeT')


def WrapType(type_: WrapTypeT) -> WrapTypeT:
    return _WrapType(type_)


def deserialize(class_: type[DeserializedT], reader: Reader = None, first=None, last=None, bytes=None,
                parent_custom_type=None) -> DeserializedT:
    if isinstance(class_, _WrapType):
        class_ = class_.type

    if isinstance(class_, RecursiveType):
        class_ = parent_custom_type

    result = class_()

    if bytes:
        reader = BufferReader(bytes)

    plans = generate_deserializing_plans(class_, first=first, last=last)
    for plan in plans:
        plan.read_using_plan(reader, result, parent_custom_type=class_)

    return result


def serialize(value, writer: Writer, first=None, last=None, parent_custom_type=None):
    value_type_ = type(value)

    if isinstance(value_type_, RecursiveType):
        value_type_ = parent_custom_type

    plans = generate_deserializing_plans(value_type_, first=first, last=last)
    for plan in plans:
        plan.write_using_plan(writer, value, parent_custom_type=value_type_)


def get_serialized_size(value, first=None, last=None) -> int:
    """ Useful for archive structures that stores headers and data separately and uses offsets for reading the data """
    """ NOTE: this function is quite expensive to call on big data structures """
    writer = SizeCalculatorWriter()
    serialize(value, writer, first=first, last=last)
    return writer.current_size
