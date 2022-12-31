from .plans import generate_deserializing_plans
from .types import RecursiveType
from .types import _WrapType
from .reader import Reader, BufferReader


class Deserializer:
    def __init__(self, reader: Reader = None, bytes: bytes = None):
        self.reader = reader or BufferReader(bytes)

    def deserialize(self, class_, parent_custom_type=None, first=None, last=None):
        if isinstance(class_, _WrapType):
            class_ = class_.type

        if isinstance(class_, RecursiveType):
            class_ = parent_custom_type

        result = class_()

        plans = generate_deserializing_plans(class_, first=first, last=last)
        for plan in plans:
            plan.read_using_plan(self, result, parent_custom_type=class_)

        return result
