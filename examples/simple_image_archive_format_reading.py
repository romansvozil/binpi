import time

from simple_image_archive_format import Archive

import binpi

if __name__ == "__main__":
    begin = time.time()
    archive = binpi.deserialize(Archive, reader=binpi.FileReader("../data/archive.simple_image_archive_format"))
    print(f"deserializing took {time.time() - begin:.2f} seconds")
    print(f"{archive.items_count=}")

    for item in archive.items:
        print(f"{item.id=} {item.image.width=} {item.image.height=} {item.name=} {item.is_compressed=} {item.image.image_type=}")
