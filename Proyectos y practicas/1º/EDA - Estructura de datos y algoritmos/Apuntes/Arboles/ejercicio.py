from pydoc import locate
import random
from BST.bst import BinarySearchTree, BinaryNode

def quick_sort(list):
    if len(list) < 2:
        return list
    else:
        pivot = list[0]
        less = [i for i in list[1:] if i <= pivot]
        greater = [i for i in list[1:] if i > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

class MyBinTree(BinarySearchTree):
    def __init__(self) -> None:
        super().__init__()
    
    def get_not_leaves(self) -> list:
        return self._get_not_leaves(self._root)

    def _get_not_leaves(self,node:BinaryNode):
        if node.right and node.left:
            return  self._get_not_leaves(node.right) + [node.elem] + self._get_not_leaves(node.left)
        elif node.right:
            return  self._get_not_leaves(node.right) + [node.elem]
        elif node.left:
            return  [node.elem] + self._get_not_leaves(node.left)
        return list()
    def depth(self,elem):
        if elem==self._root.elem:
            return 0
        if elem<self._root.elem:
            return 1 + self._depth(elem,self._root.left)
        elif elem>self._root.elem:
            return 1 + self._depth(elem,self._root.right)
    def _depth(self,elem,node:BinaryNode):
        if elem==node.elem:
            return 0
        if elem<node.elem:
            return 1 + self._depth(elem,node.left)
        elif elem>node.elem:
            return 1 + self._depth(elem,node.right)
        
    def locate_father(self,elem):
        return self._locate_father(self,elem,self._root)
    def _locate_father(self,elem,node:BinaryNode):
        if node.left.elem==elem or node.right.elem==elem:
            return node
        elif node.elem<elem:
            return self._locate_father(elem,node.left)
        elif node.elem>elem:
            return self._locate_father(elem,node.right)


    def locate_grandfather(self,elem):
        return self._locate_grandfather(self,elem,self._root)
    def _locate_grandfather(self,elem,node:BinaryNode):
        if node.left:
            if node.left.left and node.left.left.elem==elem:
                return node
            if node.left.right and node.left.left.elem==elem:
                return node
        if node.right:
            if node.right.left and node.right.left.elem==elem:
                return node
            if node.right.right and node.right.left.elem==elem:
                return node
        
    
    def checkCousins(self,a,b):
        if self.depth(a)==self.depth(b) and self.locate_father(a)!= self.locate_father(b):
            return True
        else: return False


t=MyBinTree()
for i in range(5):
    t.insert(random.randint(0,20))
t.draw()

input()

