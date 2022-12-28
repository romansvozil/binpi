import typing

import binpi


class AdvancedStructure:
    float_storage = binpi.List(binpi.LEFloat(), 10)
    int_storage = binpi.List(binpi.LEInt(), 10)
    uint_storage = binpi.List(binpi.LEUInt(), 10)

    data_length = binpi.LEUInt()
    data = binpi.List(binpi.LEUInt(), size="data_length")

    substructures_length = binpi.LEUInt()

    # we need to give python some hint
    substructures: typing.List["AdvancedStructure"] = binpi.List(binpi.RecursiveType(), size="substructures_length")
