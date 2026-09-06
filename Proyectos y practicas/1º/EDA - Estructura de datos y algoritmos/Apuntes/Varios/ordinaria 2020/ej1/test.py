import unittest
from BST import MyBST

class Test(unittest.TestCase):

    #provisional mark
    mark=0

    def setUp(self):
        values=[12, 16, 19, 20, 4, 14, 2, 18, 10, 8, 24, 6, 1, 13]
        self.bst=MyBST()
        for x in values:
            self.bst.insert(x)
        

        self.data=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        
        self.bst.draw()
    
    def test7_printNota(self):
        print('\n\n*************************')
        print("\t Provisional mark:",Test.mark)  
        print('*************************')

    def test1_checkCousins(self):
        print('Caso 1: a does not in the tree, a=',self.data[0],', b=',self.data[1])
        self.assertEqual(self.bst.checkCousins(self.data[0],self.data[1]), False)
        print('\t\t mark += 1')
        Test.mark+=1

    def test2_checkCousins(self):
        print('Caso 2: b does not in the tree, a=',self.data[1],', b=',self.data[5])
        self.assertEqual(self.bst.checkCousins(self.data[0],self.data[1]), False)
        print('\t\t mark += 1')
        Test.mark+=1

    def test3_checkCousins(self):
        print('Caso 3: a y b have different depths, a=',self.data[1],', b=',self.data[4])
        self.assertEqual(self.bst.checkCousins(self.data[1],self.data[4]), False)
        print('\t\t mark += 3')
        Test.mark+=3

    def test4_checkCousins(self):
        print('Caso 4: a and b are siblings, a=',self.data[2],', b=',self.data[10])
        self.assertEqual(self.bst.checkCousins(self.data[2],self.data[10]), False)
        print('\t\t mark += 5')
        Test.mark+=5

    def test5_checkCousins(self):
        print('Caso 5: a and b are not cousing and not siblings, a=',self.data[8],', b=',self.data[13])
        self.assertEqual(self.bst.checkCousins(self.data[8],self.data[13]), False)
        print('\t\t mark += 5')
        Test.mark+=5
    
    def test6_checkCousins(self):
        print('Caso 6: a and b are  cousins a=',self.data[2],', b=',self.data[19])
        self.assertEqual(self.bst.checkCousins(self.data[2],self.data[19]), True)
        print('\t\t mark += 5')
        Test.mark+=5
        
    


#Comentar para usarlo en google colab
# unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()