from simple_image_archive_format import Archive, ArchiveItem

import binpi

if __name__ == "__main__":
    archive = binpi.deserialize(Archive, reader=binpi.FileReader("../data/archive.simple_image_archive_format"))
    print(f"{archive.items_count=}")

    for item in archive.items:
        item: ArchiveItem
        print(f"{item.id=} {item.image.width=} {item.image.height=} {item.name=} {item.is_compressed=}")
