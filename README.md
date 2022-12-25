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

## Notes:
- As previously mentioned, binpi is in a state of being a POC, so the whole API might drastically change. Currently, the library uses `__annotations__` to gather data about a class. This might change later to the "django" style of defining models (`prop1 = binpi.LEInt()` instead of `prop1: binpi.LEInt()`), which might (might not).

## TODO:
- ~~Fix autocompletion (since we're using for annotation `binpi.LEInt()` the IDE's cannot guess the expected type correctly)~~ kinda fixed, but it's quite hacky
- Performance improvements (batch struct.un/pack should help)
- Partial structure (de)serializing (optional `from`/`to` arguments)
- String structure (custom encoding support, sized/c-like)
- Maybe get rid of LE/BE type prefixes and make it the reader's responsibility, not sure if any formats use both LE and BE.
