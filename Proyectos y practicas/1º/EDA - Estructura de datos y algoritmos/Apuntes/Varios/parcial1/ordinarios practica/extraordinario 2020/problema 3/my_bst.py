from bst import BinaryNode, BinarySearchTree


class my_bst(BinarySearchTree):
    def __init__(self) -> None:
        super().__init__()

    def iwc(self, a, b):
        return self.__iwc(self._root, a, b)

    def __iwc(self, parent: BinaryNode, a, b):
        if parent:
            if a < parent.elem and b < parent.elem:
                return self.__iwc(parent.left, a, b)
            if a > parent.elem and b > parent.elem:
                return self.__iwc(parent.right, a, b)
            searching = True
            a_dad = parent
            b_dad = parent
            while searching:
                if a < a_dad.elem:
                    a_dad = a_dad.left
                elif a > a_dad.elem:
                    a_dad = a_dad.right
                if not a_dad:
                    return
                if b < b_dad.elem:
                    b_dad = b_dad.left
                elif b > b_dad.elem:
                    b_dad = b_dad.right
                if not b_dad:
                    return
                if a_dad.elem==a and b_dad.elem==b:
                    searching=False

            return parent.elem

tree=my_bst()
l=[50,48,70,30,65,90,20,32,67,98,15,25,31,35,66,69,94,99]
for i in l:
    tree.insert(i)
tree.draw()

print(tree.iwc(20,30))