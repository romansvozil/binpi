import time

from simple_structure_many_fields import *


if __name__ == "__main__":
    file_name = "../data/simple_structure_many_fields_writing.custom"
    begin = time.time()
    archive = binpi.deserialize(SimpleStructureManyFieldsArchive, reader=binpi.FileReader(file_name))
    print(f"deserializing took {time.time() - begin:.2f} seconds")