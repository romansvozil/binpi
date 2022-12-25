import binpi
import simple_image_format


class ArchiveItem:
    id: binpi.BEInt()
    image: simple_image_format.Image


class Archive:
    items_count: binpi.BEInt()
    items: binpi.List(ArchiveItem, size="items_count")
