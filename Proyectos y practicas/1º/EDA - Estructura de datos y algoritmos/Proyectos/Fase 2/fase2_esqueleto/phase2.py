from bst import BinaryNode, BinarySearchTree


class AVLTree(BinarySearchTree):
    # Override insert method from base class to keep it as AVL
    def insert(self, elem: object) -> None:
        """inserts a new node, with key and element elem"""
        self._root = self._insert(self._root, elem)

    def _insert(self, node: BinaryNode, elem: object) -> BinaryNode:
        """gets a node, searches the place to insert a new node with element e (using super()._insert),  and then,
        the function has to balance the node returned by the function super.()_insert"""
        node = super()._insert(node, elem)
        node = self._rebalance(node)
        return node

    # Override remove method from base class to keep it as AVL
    def remove(self, elem: object) -> None:
        self._root = self._remove(self._root, elem)

    def _remove(self, node: BinaryNode, elem: object) -> BinaryNode:
        """ gets a node, searches the node with element elem in the subtree that hangs down node , and
        then remove this node (using super()._remove). After this, the function has to balance the node returned by the function super()._remove"""
        node = super()._remove(node, elem)
        node = self._rebalance(node)
        return node

    def _rebalance(self, node: BinaryNode) -> BinaryNode:
        """gets node and balances it"""
        if node is None:
            return node
        if self._height(node.left)-self._height(node.right) > 1:
            if self._height(node.left.left) >= self._height(node.left.right):
                # Habria que hacer un rotación simple Izquierda: o una rotación doble derecha-izquierda
                node = self.__rotacion_simple_derecha(node)
            else:

                node = self.__rotacion_doble_izquierda_derecha(node)
        elif self._height(node.right)-self._height(node.left) > 1:
            if self._height(node.right.right) >= self._height(node.right.left):
                node = self.__rotacion_simple_izquierda(node)
            else:
                node = self.__rotacion_doble_derecha_izquierda(node)
        return node

    def __rotacion_simple_izquierda(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def __rotacion_simple_derecha(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def __rotacion_doble_derecha_izquierda(self, node):
        node.right = self.__rotacion_simple_derecha(node.right)
        return self.__rotacion_simple_izquierda(node)

    def __rotacion_doble_izquierda_derecha(self, node):
        node.left = self.__rotacion_simple_izquierda(node.left)
        return self.__rotacion_simple_derecha(node)


t = AVLTree()
for i in range(3, 0, -1):
    t.insert(i)
t.draw()

'''
input()
# rotacion doble derecha izquierda 35
t.insert(9)
t.insert(7)
t.insert(8)
t.draw()'''
