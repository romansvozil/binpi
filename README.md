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

_For more examples, check `./examples/`_

## How to install:

```bash 
pip install binpi
```

## Supported Types:

- LEInt, LEUInt, LEShort, LEUShort, LEByte, LEUByte, LEFloat, LEDouble
- BEInt, BEUInt, BEShort, BEUShort, BEByte, BEUByte, BEFloat, BEDouble
- List, String

## TODO:

- Tests
