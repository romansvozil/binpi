import typing


class Reader(typing.Protocol):
    def read_bytes(self, n: int):
        raise NotImplementedError


class FileReader:
    def __init__(self, file_path=None, file=None):
        self.file = file or open(file_path, "rb")

    def read_bytes(self, n: int):
        return self.file.read(n)


class BufferReader:
    offset: int
    data: bytes

    def __init__(self, data: bytes, offset: int = 0):
        self.data = data
        self.offset = offset

    def read_bytes(self, n: int):
        data = self.data[self.offset: self.offset + n]
        self.offset += n
        return data
