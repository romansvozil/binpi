import binpi
import simple_image_format


class ArchiveItem:
    id = binpi.Int()
    name_length = binpi.Int()
    name = binpi.String(size="name_length")
    is_compressed = binpi.Boolean()
    image = binpi.WrapType(simple_image_format.Image)


class Archive:
    items_count = binpi.Int()
    items = binpi.List(ArchiveItem, size="items_count")
