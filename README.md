# binpi

binpi aims to provide simple interface for serializing and deserializing binary file formats. 

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

#serializing 
binpi.serialize(header_data, binpi.FileWriter("./another_path"))
```

## How to install:
```bash 
pip install binpi
```

## Notes:
- As previously mentioned, binpi is in state of being a POC, so the whole API might drastically change. Currently, the library uses `__annotations__` to gather data about class, this might change later to the "django" style of defining models (`prop1 = binpi.LEInt()` instead of `prop1: binpi.LEInt()`), which might (might not).

## TODO:
- Currently, do not support custom sub-structures
- ~~Fix autocompletion (since we're using for annotation `binpi.LEInt()` the IDE's cannot guess correctly the expected type)~~ kinda fixed, but it's quite hacky
- Performance improvements (batch struct.un/pack should help)
