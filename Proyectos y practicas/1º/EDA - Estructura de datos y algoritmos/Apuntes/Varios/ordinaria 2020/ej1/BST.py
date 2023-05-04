from turtle import right


class Node:
    def __init__(self, elem, left=None, right=None, parent=None):
        self.elem = elem
        self.left = left
        self.right = right
        self.parent = parent


class MyBST:

    def __init__(self):
        self.root = None

    def depth(self, node):
        if node == None or node.parent == None:
            return 0

        return 1 + self.depth(node.parent)

    def find(self, x):
        """Returns True if x exists into the True, eoc False"""
        return self._find(self.root, x)

    def _find(self, node, x):
        """Returns the node whose elem is x. 
        If this does not exist, it returns None"""
        if node == None:
            return None
        if node.elem == x:
            return node
        if x < node.elem:
            return self._find(node.left, x)
        if x > node.elem:
            return self._find(node.right, x)

    def insert(self, x):
        """inserts a new node, with element x, into the tree"""
        if self.root == None:
            self.root = Node(x)
        else:
            self._insertNode(self.root, x)

    def _insertNode(self, node, x):
        if node.elem == x:
            #print('Error: la clave ya existe. No permitimos duplicados')
            return

        if x < node.elem:

            if node.left == None:
                # ya he encontrado su sitio
                newNode = Node(x)
                newNode.parent = node
                node.left = newNode
            else:
                self._insertNode(node.left, x)

        else:  # x>node.elem

            if node.right == None:
                # ya he encontrado la posición
                newNode = Node(x)
                newNode.parent = node
                node.right = newNode
            else:
                self._insertNode(node.right, x)

    def draw(self):
        """Function to draw the tree"""
        self._draw('', self.root, False)
        print()

    def _draw(self, prefix, node, isLeft):
        if node != None:
            self._draw(prefix + "     ", node.right, False)
            print(prefix + ("|-- ") + str(node.elem))
            self._draw(prefix + "     ", node.left, True)

    def checkCousins(self, x, y):
        """returns True if x and y are cousins, and False eoc"""
        parent_x=self.find_parent(x)
        parent_y=self.find_parent(y)
        if parent_x and parent_y:
            return parent_x!=parent_y and self.find_parent(parent_x.elem)==self.find_parent(parent_y.elem)
        return False
    
    def find_parent(self,x):
        parent=self.root
        while True:
            if parent:
                if x<parent.elem and parent.left and x!= parent.left.elem:
                    parent=parent.left
                elif x>parent.elem and parent.right and x!= parent.right.elem:
                    parent=parent.right 
                else:
                    return parent
            else:
                return None
                
