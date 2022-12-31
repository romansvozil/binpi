import typing


class Writer(typing.Protocol):
    def write_bytes(self, data: bytes):
        raise NotImplementedError


class FileWriter:
    def __init__(self, file_path=None, file=None):
        self.file = file or open(file_path, "wb")

    def write_bytes(self, data: bytes):
        self.file.write(data)


class SizeCalculatorWriter:
    def __init__(self):
        self.current_size = 0

    def write_bytes(self, data: bytes):
        self.current_size += len(data)


class BufferWriter:
    def __init__(self):
        self.buffer = bytearray()

    def write_bytes(self, data: bytes):
        self.buffer.extend(data)
