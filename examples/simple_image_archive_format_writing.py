from simple_image_archive_format import Archive, ArchiveItem
from simple_image_format import Image

import binpi

if __name__ == "__main__":
    archive_item = ArchiveItem()
    archive_item.id = 123
    archive_item.image = binpi.deserialize(Image, reader=binpi.FileReader("../data/image.simple_image_format"))
    archive_item.name = "Cool looking image"
    archive_item.name_length = len(archive_item.name) # might not be the case for non ASCII characters
    archive_item.is_compressed = True

    archive = Archive()
    archive.items_count = 1
    archive.items = [archive_item]

    binpi.serialize(archive, writer=binpi.FileWriter("../data/archive.simple_image_archive_format"))