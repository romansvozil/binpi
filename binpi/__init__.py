from .reader import *
from .writer import *
from .types import *
from .utils import *
from .deserializer import *
from .serializer import *
from .list import *
from .into_type_instance import *


def deserialize(class_: type[DeserializedT], reader: Reader = None, first=None, last=None, bytes=None,
                parent_custom_type=None) -> DeserializedT:
    return Deserializer(reader=reader, bytes=bytes).deserialize(class_=class_, first=first, last=last,
                                                                parent_custom_type=parent_custom_type)


def serialize(value, writer: Writer, first=None, last=None, parent_custom_type=None):
    return Serializer(writer=writer).serialize(value=value, first=first, last=last,
                                               parent_custom_type=parent_custom_type)


def get_serialized_size(value, first=None, last=None) -> int:
    """ Useful for archive structures that stores headers and data separately and uses offsets for reading the data """
    """ NOTE: this function is quite expensive to call on big data structures """
    writer = SizeCalculatorWriter()
    serialize(value, writer, first=first, last=last)
    return writer.current_size
