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

    def calculate_level(self, levels, iteration):
        prev_level = levels[iteration]
        iterator = range(0, len(prev_level) // 2)
        new_level = [sha256(prev_level[i] + prev_level[i+1]).digest() for i in iterator]
        return levels + [new_level]

    def calculate_full_tree(self, elements, depth):
        hashed_elements = [sha256(element).digest() for element in elements]
        return reduce(self.calculate_level, range(0, depth), [hashed_elements])

    def initialise_empty(self) -> None:
        self.empty_element = b'\0'

        elements = [self.empty_element for _ in range(0, self.max_elements)]
        self.elements = elements

        self.lists = self.calculate_full_tree(self.elements, self.depth)

    def calculate_leaf(self, lists, level, i) -> bytes:
        full_level = lists[level]
        return sha256(full_level[2*i] + full_level[2*i+1]).digest()

    def calculate_and_update_leaf(self, lists, params) -> list:
        (level, i) = params
        leaf = self.calculate_leaf(lists, level, i)
        lists[level+1][i] = leaf
        return lists

    def modify_element(self, index: int, value: bytes) -> None:
        self.elements[index] = value
        hashed_element = sha256(value).digest()
        self.lists[0][index] = hashed_element
        levels = range(0, self.depth)
        indexs = [index // (2**power) for power in range(1, self.depth+1)]
        params = zip(levels, indexs)
        self.lists = reduce(self.calculate_and_update_leaf, params, self.lists)

    def add_element(self, index: int, value: bytes) -> None:
        if self.elements[index] == self.empty_element:
            self.modify_element(index, value)
        else:
            raise Exception('Value exist')

    def remove_element(self, index: int) -> None:
        if self.elements[index] != self.empty_element:
            self.modify_element(index, self.empty_element)
        else:
            raise Exception("Value doesn't exist")


if __name__ == "__main__":
    spt = SparseMerkleTree()
    spt.setup_depth(10)
    spt.initialise_empty()
    spt.get_root()
    spt.add_element(0, b"1234")
    for item in spt.lists:
        print(item)
        print()