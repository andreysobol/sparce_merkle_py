from hashlib import sha256
from functools import reduce

class SparseMerkleTree():

    def __init__(self) -> None:
        pass

    def initialise_empty(self) -> None:
        max_elements = 1024
        depth = 10
        empty_element = b'\0'

        elements = [empty_element for _ in range(0, max_elements)]
        self.elements = elements

        def calculate_level(levels, iteration):
            prev_level = levels[iteration]
            new_level = [sha256(prev_level[i] + prev_level[i+1]).digest() for i in range(0, prev_level // 2)]
            return levels + [new_level]

        def calculate_full_tree(elememts, depth):
            hashed_elements = [sha256(element).digest() for element in elements]
            reduce(calculate_level, range(0, depth-1), hashed_elements)

        self.lists = calculate_full_tree(self.elements, depth)

        return 

if __name__ == "__main__":
    spt = SparseMerkleTree()
    spt.initialise_empty()