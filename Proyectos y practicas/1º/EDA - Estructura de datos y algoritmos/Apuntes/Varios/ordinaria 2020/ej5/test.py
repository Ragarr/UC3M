import unittest
from main import SList2 as SList

class Test(unittest.TestCase):
  
    #static variable to save your mark
    mark=0
    
    def setUp(self):
        self.l=SList()
        for i in ['a','b','c','d','e','f','g','h','i','k']:
            self.l.add(i)
      
        self.expected0='a,b,c,d,e,f,g,h,i,k'
        self.expected1='k,a,b,c,d,e,f,g,h,i'
        self.expected2='f,g,h,i,k,a,b,c,d,e'
        self.expected3='b,c,d,e,f,g,h,i,k,a'

    def test8_printMark(self):
        print('\n\n*************************')
        print("\tProvisional mark:",Test.mark)  
        print('*************************') 

    def test1_moveLastToFront(self):
        k=len(self.l)
        print('\nCase 1: k= len(l) k=',k)
        print('input:   ',str(self.l))
        self.l.moveLastToFront(k)
        result=str(self.l)
        print('result:  ',result)
        print('expected:',self.expected0)
        self.assertEqual(result,self.expected0)
        print('\t\t mark += 1')
        Test.mark+=1


    

    '''def test2_moveLastToFront(self):
        k=0
        print('\nCase 3: k= 0, k=',0)
        print('input:   ',str(self.l))
        self.l.moveLastToFront(k)
        result=str(self.l)
        print('result:  ',result)
        print('expected:',self.expected0)
        self.assertEqual(result,self.expected0)
        print('\t\t mark += 1')
        Test.mark+=1

    def test4_moveLastToFront(self):
        k=1
        print('\nCase 4: k<len(l), k=',k)
        print('input:   ',str(self.l))
        self.l.moveLastToFront(k)
        result=str(self.l)
        print('result:  ',result)
        print('expected:',self.expected1)
        self.assertEqual(result,self.expected1)
        print('\t\t mark += 2')
        Test.mark+=2

    def test5_moveLastToFront(self):
        k=len(self.l)//2
        print('\nCase 5: k=len(l)//2, k=',k)
        print('input:   ',str(self.l))
        self.l.moveLastToFront(k)
        result=str(self.l)
        print('result:  ',result)
        print('expected:',self.expected2)
        self.assertEqual(result,self.expected2)
        print('\t\t  mark += 3')
        Test.mark+=3

    def test6_moveLastToFront(self):
        k=len(self.l)-1
        print('\nCase 6: k=len(l)-1, k=',k)
        print('input:   ',str(self.l))
        self.l.moveLastToFront(k)
        result=str(self.l)
        print('result:  ',result)
        print('expected:',self.expected3)
        self.assertEqual(result,self.expected3)
        print('\t\t mark += 3')
        Test.mark+=3'''
   


#Comentar para usarlo en spyder
unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()