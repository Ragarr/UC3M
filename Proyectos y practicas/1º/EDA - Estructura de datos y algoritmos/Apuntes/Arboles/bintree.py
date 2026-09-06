# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 13:24:19 2022


"""

class BinaryNode:
    """This implementation only saves the references to the children"""

    def __init__(self, elem: object,
                 left: "BinaryNode" = None,
                 right: "BinaryNode" = None) -> None:
        self.elem = elem
        self.left = left
        self.right = right

    def __eq__(self, other: 'BinaryNode') -> bool:
        """checks if two nodes (subtrees) are equal o not"""
        return other is not None and self.elem == other.elem and \
               self.left == other.left and self.right == other.right


class BinaryTree:
    def __init__(self) -> None:
        """creates an empty binary tree
        I only has an attribute: _root"""
        self._root = None

    def __eq__(self, other: 'BinaryTree') -> bool:
        """checks if two binary trees are equal o not"""
        return other is not None and self._root == other._root

    def size(self) -> int:
        """Returns the number of nodes"""
        return self._size(self._root)

    def _size(self, node: 'BinaryNode') -> int:
        """return the size of the subtree from node"""
        if node is None:
            return 0
        else:
            return 1 + self._size(node.left) + self._size(node.right)

    def height(self) -> int:
        """Returns the height of the tree"""
        return self._height(self._root)

    def _height(self, node: 'BinaryNode') -> int:
        """return the height of node"""
        if node is None:
            return -1

        return 1 + max(self._height(node.left), self._height(node.right))

    def preorder(self) -> None:
        """prints the preorder (root, left, right) traversal of the tree"""
        self._preorder(self._root)

    def _preorder(self, node: 'BinaryNode') -> None:
        """prints the preorder (root, left, right) traversal of the subtree
        than hangs from node"""
        if node is not None:
            print(node.elem)
            self._preorder(node.left)
            self._preorder(node.right)

    def postorder(self) -> None:
        """prints the postorder (left, right, root)  traversal of the tree"""
        self._postorder(self._root)

    def _postorder(self, node: 'BinaryNode') -> None:
        """prints the postorder (left, right, root) traversal of the subtree
        than hangs from node"""
        if node is not None:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.elem)

    def inorder(self) -> None:
        """prints the inorder (left, root, right)  traversal of the tree"""
        self._inorder(self._root)

    def _inorder(self, node: 'BinaryNode') -> None:
        """prints the inorder (left, root, right) traversal of the subtree
        than hangs from node"""
        if node is not None:
            self._inorder(node.left)
            print(node.elem)
            self._inorder(node.right)

    def level_order(self) -> None:
        """prints the level order of the tree.
        We will use an array (Python List) to save the
        nodes that you are visiting. Instead of using an array,
        you could use a Queue (import queue)"""
        if self._root is None:
            print('tree is empty')
        else:
            # we use a Python list to save the binary nodes
            q = [self._root]
            while not q.empty():
                current = q.pop(0)  # dequeue, get the first node
                print(current.elem)
                if current.left is not None:
                    q.append(current.left)
                if current.right is not None:
                    q.append(current.right)

    def draw(self) -> None:
        """function to draw a tree. """
        if self._root:
            self._draw('', self._root, False)
        else:
            print('tree is empty')
        print('\n\n')

    def _draw(self, prefix: str, node: 'BinaryNode',is_left: bool) -> None:
        if node is not None:
            self._draw(prefix + "     ", node.right, False)
            print(prefix + "|-- " + str(node.elem))
            self._draw(prefix + "     ", node.left, True)

    