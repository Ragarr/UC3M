# -*- coding: utf-8 -*-
"""sol-bst-lowest-problema3.ipynb

# PROBLEMA 3 - ÁRBOLES

Sea MyBST la clase que implementa un árbol binario de búsqueda en Python (en realidad es una versión reducida que sólo incluye los métodos necesarios para este problema). 

En un árbol binario, el mínimo ascendiente común dos nodos n y m es el nodo cuyo subárbol contiene a los nodos n, m y a todos sus descendientes. 

Implementa una función, lwc, que reciba dos enteros a y b, encuentre sus nodos y obtenga el mínimo ascendiente común de ambos nodos. La función debe devolver el elemento asociado de dicho nodo ascendente.  
Si a o b, no existen, la función debe devolver None.
Si el árbol está vacío, la función debe devolver None.


Veamos algunos ejemplos:

<img src='https://www.sadev.co.za/sites/default/files/sftpk_bst.png' width='50%'>


- lwc(48,70)=50
- lwc(30,70)=50
- lwc(30,65)=50
- lwc(20,32)=30
- lwc(67,90)=70
- lwc(69,99)=70
- lwc(31,94)=50
- lwc(15,25)=20
- lwc(15,35)=30
- lwc(15,32)=30
- lwc(20,30)=30
- lwc(67,70)=70
- lwc(30,35)=30
"""

class Node: 
    def __init__(self,elem,left=None,right=None,parent=None):
        self.elem=elem
        self.left=left
        self.right=right
        self.parent=parent
        
    def __eq__(self,other):
        if other==None:
            return False
        
        return self.elem==other.elem and self.left==other.left and self.right==other.right

class MyBST:
    
    def __init__(self):
        self.root=None

    
    def __eq__(self,other):
        if other==None:
            return False

        return self.root==other.root
    
    def find(self,x):
        """Returns True if x exists into the True, eoc False"""
        return self._find(self.root,x)

    def _find(self,node,x):
        """Returns the node whose elem is x. 
        If this does not exist, it returns None"""
        if node==None:
            return None
        if node.elem==x:
            return node
        if x<node.elem:
            return self._find(node.left,x)
        if x>node.elem:
            return self._find(node.right,x)
        
    def insert(self,x):
        """inserts a new node, with element x, into the tree"""
        if self.root==None:
            self.root=Node(x)
        else:
            self._insertNode(self.root,x)


    def _insertNode(self,node,x):
        if node.elem==x:
            #print('Error: la clave ya existe. No permitimos duplicados')
            return 

        if x<node.elem:

            if node.left==None:
                #ya he encontrado su sitio
                newNode=Node(x)
                newNode.parent=node
                node.left=newNode
            else:
                self._insertNode(node.left,x)

        else: #x>node.elem

            if node.right==None:
                #ya he encontrado la posición
                newNode=Node(x)
                newNode.parent=node
                node.right=newNode
            else:
                 self._insertNode(node.right,x)
        

    def draw(self):
      """Function to draw the tree"""
      self._draw('',self.root,False)
      print()
      
    def _draw(self,prefix, node, isLeft):
        if node !=None:
            self._draw(prefix + "     ", node.right, False)
            print(prefix + ("|-- ") + str(node.elem))
            self._draw(prefix + "     ", node.left, True)


    def lwc(self,a,b):
        """returns the lowest common ancestor of a and b"""
        nodeA=self.find(a)
        if nodeA==None:
            return None
        
        nodeB=self.find(b)
        if nodeB==None:
            return None

        return self._lwc(self.root,nodeA,nodeB)

    def _lwc(self,node,nodeA,nodeB):
        if node==None:
            return None

        if nodeA.elem<node.elem and nodeB.elem<node.elem:
            return self._lwc(node.left,nodeA,nodeB)
        
        if nodeA.elem>node.elem and nodeB.elem>node.elem:
            return self._lwc(node.right,nodeA,nodeB)

        return node.elem

import random
tree=MyBST()

values=[50,48,70,30,65,90,20,32,67,98,15,25,31,35,66,69,94,99]

tree=MyBST()
for x in values:
    tree.insert(x)

tree.draw()

print(tree.lwc(48,70),50)
print(tree.lwc(30,70),50)
print(tree.lwc(30,65),50)
print(tree.lwc(20,32),30)
print(tree.lwc(67,90),70)
print(tree.lwc(69,99),70)
print(tree.lwc(31,94),50)
print(tree.lwc(15,25),20)
print(tree.lwc(15,35),30)
print(tree.lwc(67,70),70)
print(tree.lwc(30,35),30)

print(tree.lwc(90,94),90)

import unittest


class Test(unittest.TestCase):

    #provisional mark
    mark=0

    def setUp(self):
        values=[50,48,70,30,65,90,20,32,67,98,15,25,31,35,66,69,94,99]
        self.bst=MyBST()
        for x in values:
            self.bst.insert(x)
        
    
    def testz_printNota(self):
        print('\n\n*************************')
        print("\t Provisional mark:",Test.mark)  
        print('*************************')

    def test1_lwc(self):
        print('Case 1: a does not exist')
        self.assertEqual(self.bst.lwc(21,50),None)
        print('\t\t mark += 1')
        Test.mark+=1

    def test2_lwc(self):
        print('Case 2: b does not exist')
        self.assertEqual(self.bst.lwc(50,100),None)
        print('\t\t mark += 1')
        Test.mark+=1

    def test3_lwc(self):
        print('Case 3: tree is empty')
        empty=MyBST()
        self.assertEqual(empty.lwc(58,70),None)
        print('\t\t mark += 1')
        Test.mark+=1

    def test4_lwc(self):
        print('Case 4: a=30,b=90')
        self.assertEqual(self.bst.lwc(30,90),50)
        print('\t\t mark += 2')
        Test.mark+=2

    def test5_lwc(self):
        print('Case 5: a=67,b=98, same depth')
        self.assertEqual(self.bst.lwc(67,98),70)
        print('\t\t mark += 2.5')
        Test.mark+=2.5

    def test6_lwc(self):
        print('Case 6: a=15,b=32, different depth')
        self.assertEqual(self.bst.lwc(15,32),30)
        print('\t\t mark += 2.5')
        Test.mark+=2.5


    def test7_lwc(self):
        print('Case 7: a=15, b=35')
        self.assertEqual(self.bst.lwc(15,35),30)
        print('\t\t mark += 2.5')
        Test.mark+=2.5

    def test8_lwc(self):
        print('Case 8: a=67, b=99')
        self.assertEqual(self.bst.lwc(67,99),70)
        print('\t\t mark += 2.5')
        Test.mark+=2.5

    def test9_lwc(self):
        print('Case 9: a is the lowest common ancestor')
        self.assertEqual(self.bst.lwc(90,94),90)
        print('\t\t mark += 2.5')
        Test.mark+=2.5

    def test10_lwc(self):
        print('Case 10: b is the lowest common ancestor')
        self.assertEqual(self.bst.lwc(20,30),30)
        print('\t\t mark += 2.5')
        Test.mark+=2.5


#Comentar para usarlo en google colab
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()