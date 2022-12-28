import binpi
import simple_image_format


class ArchiveItem:
    id = binpi.BEInt()
    name_length = binpi.BEInt()
    name = binpi.String(size="name_length")
    is_compressed = binpi.Boolean()
    image = binpi.WrapType(simple_image_format.Image)


class Archive:
    items_count = binpi.BEInt()
    items = binpi.List(ArchiveItem, size="items_count")
