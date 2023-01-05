from .reader import Reader, BufferReader, FileReader
from .writer import Writer, BufferWriter, FileWriter, SizeCalculatorWriter
from .types import *
from .utils import get_usable_fields
from .deserializer import Deserializer
from .serializer import Serializer
from .list import List, String, ByteArray
from .into_type_instance import into_type_instance


def deserialize(class_: type[DeserializedT], reader: Reader = None, first=None, last=None, bytes=None,
                parent_custom_type=None, instance=None, endianness=LITTLE_ENDIAN) -> DeserializedT:
    return Deserializer(reader=reader, bytes=bytes, endianness=endianness).deserialize(class_=class_, first=first, last=last,
                                                                parent_custom_type=parent_custom_type, instance=instance)


def serialize(value, writer: Writer, first=None, last=None, parent_custom_type=None, endianness=LITTLE_ENDIAN):
    return Serializer(writer=writer, endianness=endianness).serialize(value=value, first=first, last=last,
                                               parent_custom_type=parent_custom_type)


def get_serialized_size(value, first=None, last=None) -> int:
    """ Useful for archive structures that stores headers and data separately and uses offsets for reading the data """
    """ NOTE: this function is quite expensive to call on big data structures """
    writer = SizeCalculatorWriter()
    serialize(value, writer, first=first, last=last)
    return writer.current_size
