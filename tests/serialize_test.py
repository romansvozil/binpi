import unittest
import binpi

from .shared import BasicStructure


class SerializeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = BasicStructure()
        data.le_int = 100
        data.le_uint = 100
        data.le_short = 100
        data.le_ushort = 100
        data.le_byte = 100
        data.le_ubyte = 100
        data.le_float = 100
        data.le_double = 100
        data.be_int = 100
        data.be_uint = 100
        data.be_short = 100
        data.be_ushort = 100
        data.be_byte = 100
        data.be_ubyte = 100
        data.be_float = 100
        data.be_double = 100
        self.data = data

    def test_size(self):
        self.assertEqual(binpi.get_serialized_size(self.data), 52)

    def test_serialize_all(self):
        writer = binpi.BufferWriter()
        binpi.serialize(self.data, writer=writer)
        self.assertEqual(len(writer.buffer), 52)
        # todo: assert the data

    def test_serialize_half(self):
        writer = binpi.BufferWriter()
        binpi.serialize(self.data, writer=writer, last="le_double")
        self.assertEqual(len(writer.buffer), 26)
        # todo: assert the data

    def test_serialize_second_half(self):
        writer = binpi.BufferWriter()
        binpi.serialize(self.data, writer=writer, first="be_int", last="be_double")
        self.assertEqual(len(writer.buffer), 26)
        # todo: assert the data


if __name__ == '__main__':
    unittest.main()
