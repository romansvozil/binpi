from advanced_structure import *


def create_structure() -> AdvancedStructure:
    structure = AdvancedStructure()
    structure.float_storage = [0.1 * i for i in range(10)]
    structure.int_storage = [i - 5 for i in range(10)]
    structure.uint_storage = [i for i in range(10)]

    structure.data_length = 100000
    structure.data = [i % 256 for i in range(structure.data_length)]

    structure.substructures = []
    structure.substructures_length = 0

    return structure


def push_substructures(n: int, structure: AdvancedStructure):
    for i in range(n):
        sub = create_structure()
        push_substructures(n - 1, sub)
        structure.substructures.append(sub)
        structure.substructures_length += 1


if __name__ == "__main__":
    root = create_structure()
    push_substructures(2, root)
    binpi.serialize(root, writer=binpi.FileWriter("../data/advanced.advanced_structure"))


