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

if __name__ == "__main__":
    empty_roots_test()