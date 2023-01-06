# binpi

binpi aims to provide a simple interface for serializing and deserializing binary file formats.

## Usage:

```python
import binpi

class Data:
    ...

class FileHeader:
    prop1 = binpi.Int()
    prop2 = binpi.Short()
    prop3 = binpi.Byte()
    is_compressed = binpi.Boolean()
    float_prop = binpi.Float()
    some_data = binpi.ByteArray(size="prop1")
    other_data = binpi.List(Data, size="prop3")
    sub_struct = binpi.WrapType(Data)
    children_count = binpi.Int()
    children = binpi.List(binpi.RecursiveType(), size="children_count")
    
# deserializing    
header_data = binpi.deserialize(FileHeader, binpi.FileReader("./some_path"), endianness=binpi.LITTLE_ENDIAN)

# modify
header_data.prop2 = 200

# serializing 
binpi.serialize(header_data, binpi.FileWriter("./another_path"), endianness=binpi.LITTLE_ENDIAN)
```

_For more complex examples, check `./examples/`_

## How to install:

```bash 
pip install binpi
```

## Supported Types:

- Int, UInt, Short, UShort, Byte, UByte, Float, Double
- IntEnumType
- List, String, ByteArray
- Boolean
- RecursiveType (for cases where the structure contains list of substructures of the same type, check the `advanced_structure` example)
- WrapType (for subtypes, check the `simple_image_archive_format` example)
- All the types above support LE/BE

## Comparing with other (de)serializing libraries
- `pickle` - should be used for completely different use-cases than `binpi`, which is just simple deserializing of python objects, without having to care about its structure. 
- `struct` - anything `binpi` does can be implemented using `struct`, but `binpi` provides simpler interface for defining data structure, for the cost of performance.
- `origami` - origami might be a better choice for (de)serializing fixed size data, since it doesn't provide an interface for lists.
- `bstruct` - same as `origami`
- `construct` - probably the most comparable library to `binpi`, has even more feature, but instead of `binpi`, the data structures and output is represented using dictionaries

## Interface

### Serializing
```python
def serialize(
    value,           # value to be serialized
    writer: Writer,  # the output writer
    first=None,      # first field to serialize
    last=None        # last field to serialize
) -> None: ...

class Writer(Protocol):
    """ writer can be anything that implements method write_bytes """
    def write_bytes(self, data: bytes) -> None: ...
```

binpi contains `FileWriter` and `BufferWriter`

### Deserializing
```python
def deserialize(
    class_: type,    # type of the target object 
    reader: Reader,  # the input reader
    first=None,      # first field to serialize
    last=None        # last field to serialize
) -> None: ...

class Reader(Protocol):
    """ reader can be anything that implements method read_bytes """
    def read_bytes(self, n: int) -> bytes: ...
```

binpi contains `FileReader` and `BufferReader`

## Extending with custom types

To create your own custom (de)serializable type, you have to just create a new child class of `SerializableType` that implements `load_from_bytes` and `write_from_value`

```python
import typing, binpi, struct

class CustomDoubledInt(binpi.SerializableType):
    def load_from_bytes(self, deserializer: binpi.Deserializer, instance, *args, **kwargs):
        return struct.unpack("<i", deserializer.reader.read_bytes(4))[0] * 2

    def write_from_value(self, serializer: binpi.Serializer, value, parent_instance, *args, **kwargs):
        serializer.writer.write_bytes(struct.pack("<i", value // 2))

""" In case we want to have functional typechecking """
CustomDoubleInt: typing.Callable[..., int]
```

## TODO:

- Tests
