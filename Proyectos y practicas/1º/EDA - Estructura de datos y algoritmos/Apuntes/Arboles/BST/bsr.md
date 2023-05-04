## Arboles binarios de busqueda
estan ordenados de forma in order.
es un arbol binario (organizacion gerarquica dde la informacion) y complejidad logaritmica

Operaciones del TAD ABB:
- search(elem): recibe el valor de un elemento y devuelve el nodo que contiene
se elemento. Si el elemento no existe en el árbol, se muestra un mensaje y
22
devuelve None.
- insert(elem): recibe el valor de un elemento e inserta un nuevo nodo en el
árbol (por tanto, el árbol es modificado). Si el elemento ya existía,
simplemente se muestra un mensaje informando que elementos duplicados
no están permitidos.
- remove(elem): recibe el valor de un elemento a buscar. Una vez encontrado
dicho nodo es eliminado, y el árbol es modificado. Si el elemento no existe,
simplemente se muestra un mensaje informando que no existe.

el metodo **insert** devuelve un arbol nuevo modificado, es decir el objeto original no cambia, si no que se hace un return con el nuevo arbol 

search tiene dos casos base:
```
def search(elem):
    return self._search(self._root,elem)
def _search(node,elem)
    if node is None or node.elem==elem:
        return node
    elif elem < node.elem:
        return self._search(node._left, elem)
    elif elem > node.elem:
        return self._search(node.right,elem)
```
insert:
al insertar un nuevo nodo el nodo no tiene hijos, es decir solo se puede insertar como una hoja, no entre dos nodos
```
def insert(elem):
    self._root =self._insert(self._root,elem)
def _insert(node,elem):
    if not node:
        return node(elem)
    if node.elem==elem:
        print('error')
        return node
    if elem < node.elem:
        node.left=self._insert(node.left,elem)
    else:
        node.right=self._insert(node.left,elem)
    return node
```
remove:
si soy una hoja se sustituye por none
```
def remove(elem):
    self._root=self._remove(self._root,elem)
def _remove(node,elem):
    if elem<node.elem:
        node.left=self._remove(node.left)
    elif elem>node.elem:
        node.right= self.remove(node.right)
    else: node.elem==elem
        if node.left is None and node.right is None:
            return None
```
si solo tiene un hijo simplemente se salta al eliminado
```
def remove(elem):
    self._root=self._remove(self._root,elem)

def _remove(node,elem):
    if elem<node.elem:
        node.left=self._remove(node.left)
    elif elem>node.elem:
        node.right= self.remove(node.right)
    else: node.elem==elem
        if node.left is none:
            return node.right
        elif node.right is none:
            return node.left
```
si tiene dos hijos lo tiene que sustituir el mas pequeño de los mayores, lo buscamos. este solo tendra un hijo a derecha como maximo y volvemos al caso 2
```
def _minimun_node(node):
    min_node=node
    while min_node.left:
        min_node=min_node.left
    return min_node
```
```
def remove(elem):
    self._root=self._remove(self._root,elem)

def _remove(node,elem):
    if elem<node.elem:
        node.left=self._remove(node.left)
    elif elem>node.elem:
        node.right= self.remove(node.right)
    else: node.elem==elem
        if node.left is none:
            return node.right
        elif node.right is none:
            return node.left
        else:
            succesor = self._minimunnode(node.right)
            node.elem = succesor.elem
            node.right = self._remove(node.right,succesor.elem)
```

NO SE PUEDE NAVEGAR HACIA ARRIBA:
los nodos solo conocen sus hijos, no a su padre, no tienen atributo parent 