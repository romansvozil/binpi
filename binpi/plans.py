import struct
import typing
from dataclasses import dataclass
from functools import cache

from .utils import get_usable_fields
from .types import SerializableType, DeserializedT, SimpleSerializableType, RecursiveType, LITTLE_ENDIAN

if typing.TYPE_CHECKING:
    from .deserializer import Deserializer
    from .serializer import Serializer


@dataclass
class Plan:
    pattern: str
    total_size: int
    fields: list[str]
    serializable_type: typing.Optional[SerializableType] = None
    type_: typing.Optional[type[DeserializedT]] = None

    def read_using_plan(self, deserializer: "Deserializer", instance, parent_custom_type=None):
        if self.type_ is not None:
            setattr(instance, self.fields[0],
                    deserializer.deserialize(self.type_, parent_custom_type=parent_custom_type))
        elif self.serializable_type is not None:
            setattr(instance, self.fields[0],
                    self.serializable_type.load_from_bytes(deserializer, instance,
                                                           parent_custom_type=parent_custom_type))
        else:
            vals = struct.unpack(self.pattern, deserializer.reader.read_bytes(self.total_size))
            for field, value in zip(self.fields, vals):
                setattr(instance, field, value)

    def write_using_plan(self, serializer: "Serializer", instance, parent_custom_type=None):
        if self.type_ is not None:
            serializer.serialize(getattr(instance, self.fields[0]), parent_custom_type=parent_custom_type)
        elif self.serializable_type is not None:
            self.serializable_type.write_from_value(serializer, getattr(instance, self.fields[0]), parent_instance=instance,
                                                    parent_custom_type=parent_custom_type)
        else:
            fields_to_write = [getattr(instance, field) for field in self.fields]
            data_to_write = struct.pack(self.pattern, *fields_to_write)
            serializer.writer.write_bytes(data_to_write)


@cache
def generate_deserializing_plans(type_: type, first=None, last=None, endianness=LITTLE_ENDIAN):
    plans = []
    plan = None

    for key, val in get_usable_fields(type_, first, last):
        if isinstance(val, SimpleSerializableType):
            if plan is None:
                plan = Plan(endianness, 0, [])

            plan.pattern += val.STRUCT_PATTERN
            plan.total_size += val.get_SIZE()
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
