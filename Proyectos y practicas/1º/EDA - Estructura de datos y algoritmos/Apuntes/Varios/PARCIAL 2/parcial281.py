# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:00:17 2022

@author: SECRETARIA
"""

from bintree import BinaryTree
from bst import BinarySearchTree


class MyBST(BinarySearchTree):
    
    def get_diam(self):
        if self.size()==0:
            return 0
        elif self.size()==1:
            return 1
        return self.__diam(self._root)

    def __diam(self,node):
        if node.left and node.right and node != self._root:
            return 1 + max(self.__diam(node.left),self.__diam(node.right))
        if node.left and node.right and node == self._root:
            return 1 + self.__diam(node.left) + self.__diam(node.right)
        elif node.left:
            return 1 + self.__diam(node.left)
        elif node.right:
            return 1 + self.__diam(node.right)
        return 1