from hashlib import sha256
from functools import reduce
from typing import Union

class SparseMerkleTree():

    def __init__(self, depth: int) -> None:
        self.empty_element = b'\0'
        self.cache_empty_values = {}
        self._setup_depth(depth)
        self._initialise_empty()

    def _setup_depth(self, depth: int) -> None:
        self.depth = depth
        self.max_elements = 2**depth

    def increase_depth(self, amount_of_level: int):
        old_depth = self.depth
        new_depth = self.depth + amount_of_level

        params = zip(range(old_depth, new_depth), [0] * amount_of_level)
        lists = self.lists + [{} for _ in range(old_depth, new_depth)]
        self.lists = reduce(self._calculate_and_update_leaf, params, lists)

        self._setup_depth(new_depth)

    def decrease_depth(self, amount_of_level: int):
        old_depth = self.depth
        new_depth = self.depth - amount_of_level

        levels_check = range(new_depth, old_depth)
        lists = self.lists
        if False in [False for l in levels_check if 1 in lists[l]]:
            raise Exception('Trying to remove non empty subtree')

        self._setup_depth(new_depth)

    def get_root(self) -> bytes:
        if 0 in self.lists[self.depth]:
            return self.lists[self.depth][0]
        
        return self._calculate_empty_leaf_hash(self.depth)

    def _calculate_level(self, levels, iteration):
        size = 2 ** (self.depth - iteration - 1)
        iterator = range(0, size)
        params = zip([iteration] * size, iterator)
        levels = levels + [{}]
        return reduce(self._calculate_and_update_leaf, params, levels)

    def _calculate_full_tree(self, elements, depth):
        hashed_elements = {
            k:self._calculate_hash(elements[k]) for k in elements
        }
        return reduce(self._calculate_level, range(0, depth), [hashed_elements])

    def set_elements(self, elements) -> None:
        if self.max_elements < len(elements):
            raise Exception("Too many elements")

        self.elements = {
            i:elements[i] for i in range(0, len(elements)) if elements[i] != self.empty_element
        }
        self.lists = self._calculate_full_tree(self.elements, self.depth)

    def _initialise_empty(self) -> None:
        self.elements = {}
        self.lists = [{} for _ in range(0, self.depth + 1)]

    def _calculate_empty_leaf_hash(self, level):

        if level in self.cache_empty_values:
            return self.cache_empty_values[level]

        if level == 0:
            v = self._calculate_hash(self.empty_element)
        else:
            prev = self._calculate_empty_leaf_hash(level - 1)
            v = self._calculate_hash(prev + prev)

        self.cache_empty_values[level] = v
        return v

    def _calculate_leaf(self, lists, level, i) -> Union[list, type(None)]:
        full_level = lists[level]

        i0 = 2*i
        i1 = 2*i+1

        v0_exist = i0 in full_level
        v1_exist = i1 in full_level

        if (not v0_exist) and (not v1_exist):
            return None

        if v0_exist:
            v0 = full_level[i0]
        else:
            v0 = self._calculate_empty_leaf_hash(level)

        if v1_exist:
            v1 = full_level[i1]
        else:
            v1 = self._calculate_empty_leaf_hash(level)

        return self._calculate_hash(v0 + v1)

    def _calculate_and_update_leaf(self, lists, params) -> list:
        (level, i) = params
        leaf = self._calculate_leaf(lists, level, i)
        if leaf:
            lists[level+1][i] = leaf
        else:
            if i in lists[level+1]:
                del lists[level+1][i]
        return lists

    def modify_element(self, index: int, value: bytes) -> None:

        if index not in range(0, self.max_elements):
            raise Exception('Incorrect index')

        if value == self.empty_element:
            if index in self.elements:
                del self.elements[index]
            if index in self.lists[0]:
                del self.lists[0][index]
        else:
            self.elements[index] = value
            hashed_element = self._calculate_hash(value)
            self.lists[0][index] = hashed_element

        levels = range(0, self.depth)
        indexs = [index // (2**power) for power in range(1, self.depth+1)]
        params = zip(levels, indexs)
        self.lists = reduce(self._calculate_and_update_leaf, params, self.lists)

    def add_element(self, index: int, value: bytes) -> None:
        if index not in self.elements:
            self.modify_element(index, value)
        else:
            raise Exception('Value exist')

    def remove_element(self, index: int) -> None:
        if index in self.elements:
            self.modify_element(index, self.empty_element)
        else:
            raise Exception("Value doesn't exist")

    def _calculate_hash(self, preimage) -> bytes:
        raise Exception("Please declare _calculate_hash")

class Sha256SparseMerkleTree(SparseMerkleTree):

    def _calculate_hash(self, preimage) -> bytes:
        return sha256(preimage).digest()
