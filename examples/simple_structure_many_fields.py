import binpi


class SimpleStructureManyFields:
    a = binpi.LEUInt()
    b = binpi.LEUInt()
    c = binpi.LEUInt()
    d = binpi.LEUInt()
    e = binpi.LEUInt()
    f = binpi.LEUInt()
    g = binpi.LEUInt()
    h = binpi.LEUInt()
    i = binpi.LEUInt()
    j = binpi.LEUInt()
    k = binpi.LEUInt()
    l = binpi.LEUInt()
    m = binpi.LEUInt()
    n = binpi.LEUInt()
    o = binpi.LEUInt()
    p = binpi.LEUInt()
    q = binpi.LEUInt()
    r = binpi.LEUInt()
    s = binpi.LEUInt()
    t = binpi.LEUInt()
    u = binpi.LEUInt()
    v = binpi.LEUInt()
    w = binpi.LEUInt()
    x = binpi.LEUInt()
    y = binpi.LEUInt()
    z = binpi.LEUInt()


class SimpleStructureManyFieldsArchive:
    amount = binpi.LEUInt()
    items = binpi.List(SimpleStructureManyFields, size="amount")