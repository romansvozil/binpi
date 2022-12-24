# binpi

binpi is library that provides simple interface for serializing and deserializing binary file formats. binpi is currently in a state of being POC.

## Usage:
```python
import binpi

class FileHeader:
    prop1: binpi.LEInt()
    prop2: binpi.LEShort()
    prop3: binpi.LEByte()
    some_data: binpi.List(binpi.LEByte(), size="prop1")

    
header_data = binpi.deserialize(FileHeader, binpi.FileReader("./some_path"))
```