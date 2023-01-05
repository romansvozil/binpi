import os
import time

from advanced_structure import *


def print_node(node: AdvancedStructure, offset: int = 0):
    prefix = " " * offset

    print(f"{prefix}|--------")
    print(f"{prefix}| Child")
    print(f"{prefix}| - Children Length: {node.substructures_length}")
    for child in node.substructures:
        print_node(child, offset=offset+2)


if __name__ == "__main__":
    file_name = "../data/advanced.advanced_structure"

    begin = time.time()
    root = binpi.deserialize(AdvancedStructure, reader=binpi.FileReader(file_name))
    print(f"File Reader: Deserialization took {time.time() - begin} seconds, read {os.path.getsize(file_name) / (1024 * 1024)} MBs")
    # print_node(root)
