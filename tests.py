from hashlib import sha256
from spt import Sha256SparseMerkleTree

def empty_roots_test():

    check_size = range(0, 15)

    def empties(i):
        if i==0:
            return sha256(b'\0').digest()
        else:
            e = empties(i-1)
            return sha256(e + e).digest()

    empties_results = [empties(item) for item in check_size]

    def mt_roots(i):
        spt = Sha256SparseMerkleTree()
        spt.setup_depth(i)
        spt.initialise_empty()
        return spt.get_root()
    
    mt_roots_results = [mt_roots(item) for item in check_size]

    assert(empties_results == mt_roots_results)

def one_element_tests():

    def get_mt_4_root(elements):
        h_elements = [sha256(item).digest() for item in elements]
        left = sha256(h_elements[0] + h_elements[1]).digest()
        right = sha256(h_elements[2] + h_elements[3]).digest()
        root = sha256(left + right).digest()
        return root

    def get_mt_4_with_single_element(i, element):
        elements = [b'\0' for _ in range(0, 4)]
        elements[i] = element
        return get_mt_4_root(elements)
    
    value = b'apple'
    test_vec = [get_mt_4_with_single_element(i, value) for i in range(0, 4)]

    def generate_results(i):
        spt = Sha256SparseMerkleTree()
        spt.setup_depth(2)
        spt.initialise_empty()
        spt.add_element(i, value)
        return spt.get_root()

    result_vec = [generate_results(i) for i in range(0, 4)]

    assert(test_vec == result_vec)

if __name__ == "__main__":
    empty_roots_test()
    one_element_tests()
    print("All tests are correct")