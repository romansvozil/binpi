# binpi

binpi aims to provide a simple interface for serializing and deserializing binary file formats.

## Usage:

```python
import binpi


class FileHeader:
    prop1: binpi.LEInt()
    prop2: binpi.LEShort()
    prop3: binpi.LEByte()
    some_data: binpi.List(binpi.LEByte(), size="prop1")


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

- LEInt, LEUInt, LEShort, LEUShort, LEByte, LEUByte, LEFloat, LEDouble
- BEInt, BEUInt, BEShort, BEUShort, BEByte, BEUByte, BEFloat, BEDouble
- List, String

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

## TODO:

- Tests
