from hashlib import sha256

class SparseMerkleTree():

    def __init__(self) -> None:
        pass

    def initialise_empty(self) -> None:
        max_elements = 1024
        depth = 10
        empty_element = b'\0'
        elements = [sha256(empty_element).digest() for _ in range(0, max_elements)]
        self.elements = elements
        return 

if __name__ == "__main__":
    spt = SparseMerkleTree()
    spt.initialise_empty()