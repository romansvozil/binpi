import struct

from .plans import generate_deserializing_plans
from .types import RecursiveType, LITTLE_ENDIAN
from .writer import Writer


class Serializer:
    def __init__(self, writer: Writer = None, endianness=LITTLE_ENDIAN):
        self.writer = writer
        self.endianness = endianness

    def serialize(self, value, first=None, last=None, parent_custom_type=None):
        value_type_ = type(value)

        if isinstance(value_type_, RecursiveType):
            value_type_ = parent_custom_type

        plans = generate_deserializing_plans(value_type_, first=first, last=last)
        for plan in plans:
            plan.write_using_plan(self, value, parent_custom_type=value_type_)

    def write_simple_type(self, type, value):
        self.writer.write_bytes(struct.pack(self.endianness + type.get_STRUCT_PATTERN(), value))
