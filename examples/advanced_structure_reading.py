from advanced_structure import *


def print_node(node: AdvancedStructure, offset: int = 0):
    prefix = " " * offset

    print(f"{prefix}|--------")
    print(f"{prefix}| Child")
    print(f"{prefix}| - Children Length: {node.substructures_length}")
    for child in node.substructures:
        print_node(child, offset=offset+2)


if __name__ == "__main__":
    root = binpi.deserialize(AdvancedStructure, reader=binpi.FileReader("../data/advanced.advanced_structure"))
    print_node(root)
