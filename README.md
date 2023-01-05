# binpi

binpi aims to provide a simple interface for serializing and deserializing binary file formats.

## Usage:

```python
import binpi


class FileHeader:
    prop1 = binpi.Int()
    prop2 = binpi.Short()
    prop3 = binpi.Byte()
    some_data = binpi.List(binpi.Byte(), size="prop1")


# deserializing    
header_data = binpi.deserialize(FileHeader, binpi.FileReader("./some_path"))

# modify
header_data.prop2 = 200

# serializing 
binpi.serialize(header_data, binpi.FileWriter("./another_path"))
```

_For more complex examples, check `./examples/`_

## How to install:

```bash 
pip install binpi
```

## Supported Types:

- Int, UInt, Short, UShort, Byte, UByte, Float, Double
- List, String
- Boolean
- RecursiveType (for cases where the structure contains list of substructures of the same type, check the `advanced_structure` example)
- WrapType (for subtypes, check the `simple_image_archive_format` example)

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
    def load_from_bytes(self, reader: binpi.Reader, instance, *args, **kwargs):
        return struct.unpack("<i", reader.read_bytes(4))[0] * 2

    def write_from_value(self, writer: binpi.Writer, value, parent_instance, *args, **kwargs):
        writer.write_bytes(struct.pack("<i", value // 2))

""" In case we want to have functional typechecking """
CustomDoubleInt: typing.Callable[..., int]
```

## TODO:

- Find out how to make typechecking nicer
- Currently, we're kinda lacking in terms of performance on files with size 100MB+, some ideas:
  - Serializing:
    - Batch serializing, probably requires reworking the `SerializableType` class a bit, so we're able to extract the fstrings for `struct.pack` and serialize multiple fields at once
    - Splitting the data into multiple segments and serializing them in different threads (`ThreadPoolExecutor`)
  - Deserializing:
    - Since there we can't really take advantage of multiple processes, the only way how to make this faster is probably batch deserializing (same as first point for serializing)
  - Both:
    - A bit smarter data-types, for example string and list for primitive types are not efficient at all
    - Using Numba for some tasks, but that also requires quite some work, because we would have to refactor quite a lot of stuff that uses `**kwargs` since Numba is not supporting them
- Tests
