"""en lugar de push se llama encolar (enqueue) u sacar de la cola (dequeue)
se entra por un sitio (tail) y se sale por el otro(queue)
las operaciones son front() el proximo que va a salir
imEmpty() y len()"""

class Queue:
    def __init__(self) -> None: # las pilas se crean vacias y se rellenan con push
        self.items=[]
    def __str__(self) -> str:
        return str(self.items)
    def __len__(self):
        return len(self.items)
    def isEmpty(self)->bool:
        return len(self)==0
    def enqueue(self,e):
        self.items.insert(0,e)
    def dequeue(self):
        if self.isEmpty():
            raise IndexError("la cola esta vacia")
        return self.items.pop()
    def front(self):
        return self.items[-1]

if __name__=="main":
    c=Queue()
    for i in range(5):
        c.enqueue(i)
    print(c)
    c.dequeue()
    print(c)
    print(c.front())
    c.dequeue()
    print(c)
    print(c.front())

    def joseph(personas,n):
        c=cola()
        for i in range(personas):
            c.enqueue(i+1)
        while len(c)>1:
            for i in range(n):
                c.enqueue(c.dequeue())
            c.dequeue()
        return c

    print(joseph(41,2))# expected output: 31
