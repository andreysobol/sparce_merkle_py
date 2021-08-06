from hashlib import sha256
from functools import reduce

class SparseMerkleTree():

    def __init__(self) -> None:
        pass

    def setup_depth(self, depth: int) -> None:
        self.depth = depth
        self.max_elements = 2**depth

    def get_root(self) -> bytes:
        depth = 10
        return self.lists[depth][0]

    def initialise_empty(self) -> None:
        empty_element = b'\0'

        elements = [empty_element for _ in range(0, self.max_elements)]
        self.elements = elements

        def calculate_level(levels, iteration):
            prev_level = levels[iteration]
            iterator = range(0, len(prev_level) // 2)
            new_level = [sha256(prev_level[i] + prev_level[i+1]).digest() for i in iterator]
            return levels + [new_level]

        def calculate_full_tree(elements, depth):
            hashed_elements = [sha256(element).digest() for element in elements]
            return reduce(calculate_level, range(0, depth), [hashed_elements])

        self.lists = calculate_full_tree(self.elements, self.depth)

        return 

if __name__ == "__main__":
    spt = SparseMerkleTree()
    spt.setup_depth(10)
    spt.initialise_empty()
    spt.get_root()