
class Node:
    def __init__(self, elem, l=None,r=None,p=None) -> None:
        self.elem=elem
        self.parent=p
        self.left=l
        self.right=r

class BTree:
    def __init__(self, root=None) -> None:
        self.root=root
    def size(self):
        if self.root==None:
            return 0
        return self.__size(self.root)
    def __size(self, node:Node):
        if not node:
            return 0
        return 1+self.__size(node.left)+self.__size(node.right)
    
    def height(self):
        if self.root==None:
            return -1
        return self.__height(self.root) - 1
    def __height(self,node:Node):
        if not node:
            return 0
        # en realdad hay que hacer una excepcion para cuando no tiene hijos el root
        return  1+ max(self.__height(node.left),self.__height(node.right))
    
    def pre_order(self):
        return self.__preorder(self.root)
    
    def __preorder(self,node:Node):
        if node != None:
            print(node.elem)
            self.__preorder(node.left)
            self.__preorder(node.right)

N1,N2,N3,N4,N5,N6 = Node(5),Node(7),Node(2),Node(9),Node(45),Node("asd")
N6=Node(6,None,None,N4)
N4 = Node(9,N6,None,N3)
N5 =Node(8,None,None,N3)
N3 = Node(2,N5,N4,N1)
N2 = Node(7,None,None,N1)
N1 = Node(5,N3,N2,None)
trea=BTree(N1)
print(trea.height())
trea.pre_order()