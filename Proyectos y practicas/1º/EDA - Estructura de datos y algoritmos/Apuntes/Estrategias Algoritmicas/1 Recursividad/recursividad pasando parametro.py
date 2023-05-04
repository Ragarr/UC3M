class MyBST(BinarySearchTree):
    
    def get_odd_siblings(self):
        
        L=[]
        return self._get_odd_siblings(self._root,L,None)
    
    def _get_odd_siblings(self,node,L,sibling):
        # l es la lista que queremos devolver con los primos en ella
        if node is None:
            return L
        self._get_odd_siblings(node.right,L,node.left)
        
        if sibling and sibling.elem%2!=0:
            L.append(node.elem)
             
        self._get_odd_siblings(node.left,L,node.right)
        return L