'''Implement a Python class, PrinterQueue, to manage a network printer. The printer
can receive requests from different machines in a network. The requests should be
printed by entry order. Each request includes the following information: id (String)
of the machine that performs it (for example “I3493”) and the name of the file to
print (for example “unit2.pdf”). Please, write a class, named Request, to represent a
request.
The class, PrinterQueue, must implement the following operations:
● addRequest: takes a request as input and adds it to the set of requests.
● printWork: gets the first request and shows its data (id and name file) by
console (it only simulates the imprension of the request) . The request has
to be removed from the set of requests.
● getNumRequest(): returns the total number of requests.
● (): shows all the requests that have have been not printed.
● printAll(): print all the requests.
Include the needed instructions to test all the methods explained above.'''

from aiohttp import request
from pyparsing import col
from urllib3 import Retry


class Request:
    def __init__(self,id,file) -> None:
        self.id=id
        self.file=file
    def __str__(self) -> str:
        return "id: {}, file: {}".format(self.id,self.file)

class PrinterQueue:
    def __init__(self) -> None:
        self.items=[]
    def __str__(self) -> str:
        return str(self.items)
    def __len__(self):
        return len(self.items)
    def addRequest(self,r:Request):
        '''takes a request as input and adds it to the set of requests.'''
        self.items.insert(0,r)
    def printWork(self):
        '''gets the first request and shows its data (id and name file) by
        console (it only simulates the imprension of the request) . The request has
        to be removed from the set of requests.'''
        print("impreso request: '{}'".format(self.items.pop()))
    def getNumRequest(self):
        return len(self)
    def showAll(self):
        for r in self.items:
            print(r)
        
    def printAll(self):
        for _ in range(len(self)):
            self.printWork()

        

cola=PrinterQueue()
for i in range(10):
    cola.addRequest(Request(str(i),"file"+str(i)))
print(cola.getNumRequest())
cola.showAll()
cola.printWork()
cola.showAll()
cola.printAll()
cola.showAll()