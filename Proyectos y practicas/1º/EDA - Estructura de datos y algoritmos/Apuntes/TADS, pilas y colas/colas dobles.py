'''In computer science, a double-ended queue (abbreviated to deque) is an abstract
data type that generalizes a queue. In a deque, elements can be added to or
removed from either the front (head) or back (tail). The operations allowed for a
double-ended queue are:
● __init__(self): creates an empty double-ended queue.
● addLast(self,e): adds the elements at the end of the deque.
● addFirst(self,e): adds the element at the beginning of the deque.
● removeFirst(self): returns and removes the first element of the deque.
● removeLast(self): returns and removes the last element of the deque.
● isEmpty(self): checks if the deque is empty.
● __len__(self): returns the numbers of element in the deque.'''


class deque:
    def __init__(self) -> None:
        self.items = []
        pass

    def __len__(self):
        return len(self.items)

    def __str__(self) -> str:
        return str(self.items)

    def addFirst(self, e):
        self.items.insert(0, e)

    def addLast(self, e):
        self.items.append(e)

    def removeFirst(self):
        if not self.isEmpty():
            del(self.items[0])
        else:
            raise IndexError("La lista esta vacia")

    def removeLast(self):
        if not self.isEmpty():
            del(self.items[-1])
        else:
            raise IndexError("La lista esta vacia")

    def isEmpty(self) -> bool:
        return len(self)==0

dq=deque()
for i in range(10):
    dq.addFirst(i)
for i in range(10):
    dq.addLast(i)
print(dq,dq.isEmpty())
dq.removeFirst()
dq.removeLast()
for i in range(len(dq)):
    dq.removeFirst()

print(dq)