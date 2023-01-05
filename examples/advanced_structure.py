import typing

import binpi


class AdvancedStructure:
    float_storage = binpi.List(binpi.Float(), 10)
    int_storage = binpi.List(binpi.Int(), 10)
    uint_storage = binpi.List(binpi.UInt(), 10)

    data_length = binpi.UInt()
    data = binpi.List(binpi.UInt(), size="data_length")

    substructures_length = binpi.UInt()

    # we need to give python some hint
    substructures: typing.List["AdvancedStructure"] = binpi.List(binpi.RecursiveType(), size="substructures_length")
