from BST.bst  import BinarySearchTree
from BST.bst  import BinaryNode

class AVLTree(BinarySearchTree):
    def __init__(self) -> None:
        super().__init__()
    def rebalance(self) -> None:
        self._rebalance(node=self._root)
    def _rebalance(self, node: BinaryNode) -> None:
        """rebalance the subtree rooted at node"""
        if node is not None:
            self._rebalance(node.left)
            self._rebalance(node.right)
            if self._height(node.left) > self._height(node.right) + 1:
                if self._height(node.left.left) > self._height(node.left.right):
                    self._rotate_right(node)
                else:
                    self._rotate_left(node.left)
                    self._rotate_right(node)
            elif self._height(node.right) > self._height(node.left) + 1:
                if self._height(node.right.right) > self._height(node.right.left):
                    self._rotate_left(node)
                else:
                    self._rotate_right(node.right)
                    self._rotate_left(node)

    def _rotate_left(self, node: BinaryNode) -> None:
        """Rotate the subtree to the left"""
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        node = new_root
    def _rotate_right(self, node: BinaryNode) -> None:
        """Rotate the subtree to the right"""
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        node = new_root 


t=AVLTree()
l=[1,2,3]
for i in l:
    t.insert(i)
t.inorder()
t.draw()
t.rebalance()
t.inorder()
t.draw()

