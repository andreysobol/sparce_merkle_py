import unittest
from hashlib import sha256
from spt import Sha256SparseMerkleTree, SparseMerkleTree

class UnitTest(unittest.TestCase):

    def get_mt_4_root(self, elements):
        h_elements = [sha256(item).digest() for item in elements]
        left = sha256(h_elements[0] + h_elements[1]).digest()
        right = sha256(h_elements[2] + h_elements[3]).digest()
        root = sha256(left + right).digest()
        return root

    def test_empty_roots(self):

        check_size = range(1, 15)

        def empties(i):
            if i==0:
                return sha256(b'\0').digest()

            emp = empties(i-1)
            return sha256(emp + emp).digest()

        empties_results = [empties(item) for item in check_size]

        def mt_roots(i):
            spt = Sha256SparseMerkleTree(i)
            return spt.get_root()

        mt_roots_results = [mt_roots(item) for item in check_size]

        self.assertTrue(empties_results == mt_roots_results)

    def test_one_element(self):

        def get_mt_4_with_single_element(i, element):
            elements = [b'\0' for _ in range(0, 4)]
            elements[i] = element
            return self.get_mt_4_root(elements)

        value = b'apple'
        test_vec = [get_mt_4_with_single_element(i, value) for i in range(0, 4)]

        def generate_results(i):
            spt = Sha256SparseMerkleTree(2)
            spt.add_element(i, value)
            return spt.get_root()

        result_vec = [generate_results(i) for i in range(0, 4)]

        self.assertTrue(test_vec == result_vec)

    def test_step_by_step(self):

        spt = Sha256SparseMerkleTree(2)

        spt.add_element(0, b'apple')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'apple', b'\0', b'\0', b'\0'])
        self.assertTrue(root == test_result)

        spt.add_element(1, b'avocado')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'apple', b'avocado', b'\0', b'\0'])
        self.assertTrue(root == test_result)

        spt.add_element(2, b'clock')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'apple', b'avocado', b'clock', b'\0'])
        self.assertTrue(root == test_result)

        spt.add_element(3, b'great')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'apple', b'avocado', b'clock', b'great'])
        self.assertTrue(root == test_result)

    def test_step_by_step_equel_to_calculate_full_tree_result(self):

        spt = Sha256SparseMerkleTree(2)

        spt.add_element(0, b'beef')
        spt1 = Sha256SparseMerkleTree(2)
        spt1.set_elements([b'beef', b'\0', b'\0', b'\0'])
        self.assertTrue(spt.get_root() == spt1.get_root())

        spt.add_element(1, b'cost')
        spt2 = Sha256SparseMerkleTree(2)
        spt2.set_elements([b'beef', b'cost', b'\0', b'\0'])
        self.assertTrue(spt.get_root() == spt2.get_root())

        spt.add_element(2, b'enjoy')
        spt3 = Sha256SparseMerkleTree(2)
        spt3.set_elements([b'beef', b'cost', b'enjoy', b'\0'])
        self.assertTrue(spt.get_root() == spt3.get_root())

        spt.add_element(3, b'fox')
        spt4 = Sha256SparseMerkleTree(2)
        spt4.set_elements([b'beef', b'cost', b'enjoy', b'fox'])
        self.assertTrue(spt.get_root() == spt4.get_root())

    def test_remove(self):

        spt = Sha256SparseMerkleTree(2)

        spt.add_element(1, b'fish')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'\0', b'fish', b'\0', b'\0'])
        self.assertTrue(root == test_result)

        spt.add_element(3, b'ice')
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'\0', b'fish', b'\0', b'ice'])
        self.assertTrue(root == test_result)

        spt.remove_element(1)
        root = spt.get_root()
        test_result = self.get_mt_4_root([b'\0', b'\0', b'\0', b'ice'])
        self.assertTrue(root == test_result)

    def test_value_exist(self):
        spt = Sha256SparseMerkleTree(2)
        spt.add_element(0, b'first try')
        is_e = False
        try:
            spt.add_element(0, b'second try')
        except KeyError as k_e:
            is_e = True
            self.assertEqual(str(k_e), "'Value exist'")
        self.assertTrue(is_e)

    def test_value_doesnt_exist(self):
        spt = Sha256SparseMerkleTree(2)
        is_e = False
        try:
            spt.remove_element(0)
        except KeyError as k_e:
            is_e = True
            self.assertEqual(str(k_e), "'Value does not exist'")
        self.assertTrue(is_e)

    def test_incorrect_index(self):
        spt = Sha256SparseMerkleTree(2)
        is_e = False
        try:
            spt.add_element(4, b'el')
        except IndexError as i_e:
            is_e = True
            self.assertEqual(str(i_e), 'Incorrect index')
        self.assertTrue(is_e)

    def test_many_element(self):
        spt = Sha256SparseMerkleTree(2)
        is_e = False
        try:
            spt.set_elements([b'\0', b'\0', b'\0', b'\0', b'5el'])
        except IndexError as i_e:
            is_e = True
            self.assertEqual(str(i_e), 'Too many elements')
        self.assertTrue(is_e)

    def test_increase_depth(self):

        spt = Sha256SparseMerkleTree(1)
        spt.set_elements([b'zero', b'one'])
        spt.increase_depth(1)
        root = spt.get_root()

        test_result = self.get_mt_4_root([b'zero', b'one', b'\0', b'\0'])

        self.assertTrue(root == test_result)

    def test_decrease_depth(self):

        spt = Sha256SparseMerkleTree(3)
        spt.set_elements([b'z', b'o'])
        spt.decrease_depth(2)
        root = spt.get_root()

        test_result = sha256(sha256(b'z').digest() + sha256(b'o').digest()).digest()

        self.assertTrue(root == test_result)

    def test_decrease_non_empty(self):

        spt = Sha256SparseMerkleTree(2)
        spt.set_elements([b'blue', b'apple', b'dog'])

        is_e = False
        try:
            spt.decrease_depth(1)
        except IndexError as i_e:
            is_e = True
            self.assertEqual(str(i_e), 'Trying to remove non empty subtree')
        self.assertTrue(is_e)

    def test_init_0(self):

        is_e = False
        try:
            _ = Sha256SparseMerkleTree(0)
        except ValueError as v_e:
            is_e = True
            self.assertEqual(str(v_e), 'Depth should be > 0')
        self.assertTrue(is_e)

    def test_no_hash(self):

        is_e = False
        try:
            spt = SparseMerkleTree(2)
            spt.set_elements([b'just', b'els'])
        except NotImplementedError as n_i_e:
            is_e = True
            self.assertEqual(str(n_i_e), 'Please declare _calculate_hash')
        self.assertTrue(is_e)

if __name__ == '__main__':
    unittest.main()
