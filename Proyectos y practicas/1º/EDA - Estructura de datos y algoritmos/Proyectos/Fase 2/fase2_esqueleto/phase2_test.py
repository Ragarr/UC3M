import unittest

# from phase2_solution import AVLTree

from phase2 import AVLTree
from bst import BinarySearchTree

class TestAVL(unittest.TestCase):
    """
    Tests:
        - test_01 : The insertion of a node produces an unbalanced node (simple left rotation)
        - test_02 : The insertion of a node produces an unbalanced node (simple right rotation)
        - test_03:  insertion, right-left rotation
        - test_04:  insertion, left-right rotation
        - test_05:  removing, simple right rotation
        - test_06:  removing, simple left rotation
        - test_07:  removing: left-right rotation
        - test_08:  removing, right-left rotation
        - test_09:  inserting, root unbalanced, right rotation
        - test_10:  removing, root unbalanced, right rotation
        - test_11:  inserting, root unbalanced, left rotation
        - test_12:  removing, root unbalanced, left rotation
        - test_13:  inserting, root unbalanced, right-left rotation
        - test_14:  removing, root unbalanced, right-left rotation
        - test_15:  inserting, root unbalanced, left-right rotation
        - test_16:  removing, root unbalanced, left-right rotation
        - test_17:  insert a sorted sequence of numbers
        - test_18:  insert an unsorted sequence of numbers
        - test_19:  removing root, causes the right child is unbalanced
        - test_20:  remove(8) -> 7 is unbalanced, right rotation with subtrees
        - test_21:  remove(17) -> 27 is unbalance; left rotation with subtrees with subtrees
        - test_21:  removing twice, balancing twice
    """

    mark = 0

    def setUp(self):
        self.avl = AVLTree()

    def test_01(self):
        """  insertion, simple left rotation """
        data = [12, 8, 17, 6, 19]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()
        # inserting 20 will do 17 unbalanced
        # simple left rotation
        self.avl.insert(20)
        # self.avl.draw()
        data = [12, 8, 19, 6, 17, 20]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_02(self):
        """  insertion, simple right rotation """
        data = [12, 8, 17, 6, 19]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # inserting 4 will do 8 unbalance -> right rotation
        self.avl.insert(4)
        # self.avl.draw()

        data = [12, 6, 17, 8, 19, 4]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_03(self):
        """  insertion, right-left """
        data = [12, 8, 17, 6, 19]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # inserting 18 will do 17 unbalance
        # right - left rotation
        self.avl.insert(18)
        # self.avl.draw()

        data = [12, 8, 18, 6, 19, 17]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_04(self):
        """  insertion: left-right rotation """
        data = [12, 8, 17, 6, 19]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # inserting 7 will do 8 unbalance -> left - right rotation
        self.avl.insert(7)
        # self.avl.draw()

        data = [12, 7, 17, 6, 8, 19]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_05(self):
        """  inserting, root unbalanced, right rotation"""
        data = [12, 8]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we insert 6, the root 12 will be unbalanced
        # we have to apply a simple right rotation
        self.avl.insert(6)
        # self.avl.draw()

        data = [8, 6, 12]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_06(self):
        """  inserting,  root unbalanced, left rotation """
        data = [8, 12]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we insert 15, the root 8 will be unbalanced
        # we have to apply a simple left rotation
        self.avl.insert(15)
        # self.avl.draw()

        data = [12, 8, 15]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl,  expected)
        TestAVL.mark += 0.5

    def test_07(self):
        """  inserting,  root unbalanced,  right-left rotation """
        data = [8, 12]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we insert 9, the root 8 will be unbalanced
        # we have to apply a simple left rotation
        self.avl.insert(9)
        # self.avl.draw()

        data = [9, 8, 12]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_08(self):
        """  inserting, root unbalanced, right-left rotation """
        data = [8, 6]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we insert 8, the root 8 will be unbalanced
        # we have to apply a right-left rotation
        self.avl.insert(7)
        # self.avl.draw()

        data = [7, 8, 6]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_09(self):
        """  insert a sorted sequence of numbers """
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for e in data:
            self.avl.insert(e)
        # self.avl.draw()

        data = [4, 2, 6, 1, 3, 5, 8, 7, 9]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_10(self):
        """  insert an unsorted sequence of numbers """
        data = [5, 6, 7, 10, 11, 15, 20, 33, 2, 16]
        for e in data:
            self.avl.insert(e)
        # self.avl.draw()

        data = [10, 6, 15, 5, 7, 11, 20, 2, 16, 33]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.75

    """test for removing"""
    def test_11(self):
        """ removing: simple right rotation"""
        data = [12, 6, 18, 8, 20, 14, 4, 2]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 8, 6 will be unbalanced
        # simple right rotation
        self.avl.remove(8)
        # self.avl.draw()

        data = [12, 4, 18, 2, 14, 6, 20]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_12(self):
        """  removing, simple left rotation """
        data = [12, 8, 17, 6, 19, 16, 20]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 16, 17 will be unbalanced
        # we have to apply simple left rotation
        self.avl.remove(16)
        # self.avl.draw()

        data = [12, 8, 19, 6, 17, 20]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_13(self):
        """ removing: left-right rotation"""
        data = [12, 6, 18, 8, 20, 14, 4, 5]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 8, 6 will be unbalanced
        # it will be balanced by applying a double rotation: left-right
        self.avl.remove(8)
        # self.avl.draw()

        data = [12, 5, 18, 4, 14, 6, 20]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_14(self):
        """  removing, right-left rotation """
        data = [12, 8, 17, 6, 19, 16, 18]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 16, 17 will be unbalanced
        # we have to apply right-left rotation
        self.avl.remove(16)
        # self.avl.draw()

        data = [12, 8, 18, 6, 17, 19]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.25

    def test_15(self):
        """  removing, root unbalanced, right rotation """
        data = [8, 6, 12, 4]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 12, the root 8 will be unbalanced
        # we have to apply a simple right rotation
        self.avl.remove(12)
        # self.avl.draw()

        data = [6, 8, 4]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl,  expected)
        TestAVL.mark += 0.5

    def test_16(self):
        """  removing,  root unbalanced,  left rotation """
        data = [8, 6, 12, 15]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 6, the root 8 will be unbalanced
        # we have to apply a simple left rotation
        self.avl.remove(6)
        # self.avl.draw()

        data = [12, 8, 15]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_17(self):
        """  removing, root unbalanced, right-left rotation """
        data = [8, 6, 12, 10]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 6, the root 8 will be unbalanced
        # we have to apply a simple left rotation
        self.avl.remove(6)
        # self.avl.draw()

        data = [10, 8, 12]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_18(self):
        """  removing, root unbalanced, left-right rotation """
        data = [8, 6, 7, 10]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # if we remove 10, the root 8 will be unbalanced
        self.avl.remove(10)
        # self.avl.draw()

        data = [7, 6, 8]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_19(self):
        """  after removing the root, the tree is unbalanced """
        data = [17, 8, 12, 2, 7, 27, 48, 58, 3, 4]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()
        # we remove 12 (root), it will be replaced with 17

        self.avl.remove(12)  # root
        # self.avl.draw()

        data = [17, 7, 48, 3, 8, 27, 58, 2, 4]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.5

    def test_20(self):
        """  remove(8), 7 is unbalanced, right rotation with subtrees """
        data = [17, 8, 12, 2, 7, 27, 48, 58, 3, 4]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        # we remove 8 (root), it will be replaced with 7
        self.avl.remove(8)  # root
        # self.avl.draw()

        data = [12, 3, 27, 2, 7, 17, 48, 4, 58]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.75

    def test_21(self):
        """  remove(17) -> 27 is unbalance; left rotation with subtrees with subtrees """
        data = [17, 8, 12, 2, 7, 27, 48, 45, 58, 3, 4]
        for n in data:
            self.avl.insert(n)
        # self.avl.draw()

        self.avl.remove(17)  # root
        # self.avl.draw()

        data = [12, 7, 48, 3, 8, 27, 58, 2, 4, 45]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.75

    def test_22(self):
        """ removing twice, balancing twice"""
        data = [17, 8, 12, 2, 7, 27, 48, 58, 3, 4]

        for n in data:
            self.avl.insert(n)
        # self.avl.draw()
        self.avl.remove(7)
        # self.avl.draw()
        self.avl.remove(17)
        # self.avl.draw()

        data = [12, 3, 48, 2, 8, 27, 58, 4]
        expected = BinarySearchTree()
        for n in data:
            expected.insert(n)
        # expected.draw()
        self.assertEqual(self.avl, expected)
        TestAVL.mark += 0.75

    def test_z(self):
        print('Nota provisional: ', TestAVL.mark)

if __name__ == "__main__":
    unittest.main()
