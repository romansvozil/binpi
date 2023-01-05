from .plans import generate_deserializing_plans
from .types import RecursiveType, LITTLE_ENDIAN
from .types import _WrapType
from .reader import Reader, BufferReader


class Deserializer:
    def __init__(self, reader: Reader = None, bytes: bytes = None, endianness=LITTLE_ENDIAN):
        self.reader = reader or BufferReader(bytes)
        self.endianness = endianness

    def deserialize(self, class_, parent_custom_type=None, first=None, last=None, instance=None):
        if isinstance(class_, _WrapType):
            class_ = class_.type

        if isinstance(class_, RecursiveType):
            class_ = parent_custom_type

        result = instance or class_()

        plans = generate_deserializing_plans(class_, first=first, last=last, endianness=self.endianness)
        for plan in plans:
            plan.read_using_plan(self, result, parent_custom_type=class_)

        return result
