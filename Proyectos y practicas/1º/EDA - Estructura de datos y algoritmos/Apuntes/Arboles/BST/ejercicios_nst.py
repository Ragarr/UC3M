import random 
from bst import BinaryNode
from bst import BinarySearchTree
class mybst(BinarySearchTree):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    
    def minimun(self):
        if not self._root:
            return None
        return self.__minimun(self._root)
    def __minimun(self,node:BinaryNode):
        if node.left:
            return self.__minimun(node.left)
        else:
            return node.elem
    def sum_elem(self):
        return self.__sum_elem(self._root)
    def __sum_elem(self,node:BinaryNode):   
        if node.left and node.right:
            return node.elem + self.__sum_elem(node.left) + self.__sum_elem(node.right)
        elif node.left:
            return node.elem + self.__sum_elem(node.left)
        elif node.right:
            return node.elem + self.__sum_elem(node.right)
        return node.elem
    
    def multiplo10(self):
        self.__multiplo10(self._root)
    
    def __multiplo10(self,node:BinaryNode):
        if node.left:
            self.__multiplo10(node.left)
        if node.right:
            self.__multiplo10(node.right)
        if node.elem%10==0 and node.elem != 0:
            if node.left:
                if node.left.left:
                    print(node.left.left.elem)
                if node.left.right:
                    print(node.left.right.elem)
            if node.right:
                if node.right.left:
                    print(node.right.left.elem)
                if node.right.right:
                    print(node.right.right.elem)
    
        

tree=mybst()
l=[]
for i in range(0,50):
    a=random.randint(0,10)
    if not a in l:
        l.append(a*5)
for i in l:
    tree.insert(i)

tree.draw()
tree.multiplo10()



