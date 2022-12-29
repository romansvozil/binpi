import time

import binpi
from simple_structure_many_fields import *


if __name__ == "__main__":
    archive = SimpleStructureManyFieldsArchive()
    archive.amount = 100
    archive.items = []
    for i in range(archive.amount):
        item = SimpleStructureManyFields()
        item.a = i * 10
        item.b = i * 10
        item.c = i * 10
        item.d = i * 10
        item.e = i * 10
        item.f = i * 10
        item.g = i * 10
        item.h = i * 10
        item.i = i * 10
        item.j = i * 10
        item.k = i * 10
        item.l = i * 10
        item.m = i * 10
        item.n = i * 10
        item.o = i * 10
        item.p = i * 10
        item.q = i * 10
        item.r = i * 10
        item.s = i * 10
        item.t = i * 10
        item.u = i * 10
        item.v = i * 10
        item.w = i * 10
        item.x = i * 10
        item.y = i * 10
        item.z = i * 10
        archive.items.append(item)

    begin = time.time()
    binpi.serialize(archive, writer=binpi.FileWriter("../data/simple_structure_many_fields_writing.custom"))
    print(f"serializing took {time.time() - begin:.2f} seconds")