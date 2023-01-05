import binpi


class SimpleStructureManyFields:
    a = binpi.UInt()
    b = binpi.UInt()
    c = binpi.UInt()
    d = binpi.UInt()
    e = binpi.UInt()
    f = binpi.UInt()
    g = binpi.UInt()
    h = binpi.UInt()
    i = binpi.UInt()
    j = binpi.UInt()
    k = binpi.UInt()
    l = binpi.UInt()
    m = binpi.UInt()
    n = binpi.UInt()
    o = binpi.UInt()
    p = binpi.UInt()
    q = binpi.UInt()
    r = binpi.UInt()
    s = binpi.UInt()
    t = binpi.UInt()
    u = binpi.UInt()
    v = binpi.UInt()
    w = binpi.UInt()
    x = binpi.UInt()
    y = binpi.UInt()
    z = binpi.UInt()


class SimpleStructureManyFieldsArchive:
    amount = binpi.UInt()
    items = binpi.List(SimpleStructureManyFields, size="amount")