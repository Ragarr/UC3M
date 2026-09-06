import unittest
from graph import Graph

class Test(unittest.TestCase):
    # save mark
    mark=0
    
    def setUp(self):
        labels=['A', 'B', 'C', 'D', 'E','F','G']    
        # Create a given graph  
        self.g = Graph(labels)  
        self.g.addEdge('A', 'B')
        self.g.addEdge('B', 'C')
        self.g.addEdge('B', 'D')
        self.g.addEdge('B', 'E')
        self.g.addEdge('C', 'E')
        self.g.addEdge('D', 'E')
        self.g.addEdge('E', 'F')
        self.g.addEdge('G', 'D')

    def test_printMark(self):
        print('\n\n*************************')
        print("\n Provisional mark:",Test.mark)  
        print('*************************')

    def test1_minimumPath(self):
        print('Case 1: start==end ')
        self.assertEqual(self.g.minimumPath('A','A'), [])
        print('\t\t mark += 2')
        Test.mark+=2
        print()
    
    def test2_minimumPath(self):
        print('Case 2: No path ')
        self.assertEqual(self.g.minimumPath('A','G'), [])
        print('\t\t mark += 2')
        Test.mark+=2
        print()

    def test3_minimumPath(self):
        
        print('Case 3: path with distance 1')
        result=self.g.minimumPath('A','B')
        expected=['A','B']
        print('result:',result)
        print('expected:',expected)
        
        self.assertListEqual(result, expected)
        print('\t\t mark += 4')
        Test.mark+=4
        print()

    def test4_minimumPath(self):
        
        print('Case 4: path with distance 2')
        result=self.g.minimumPath('A','C')
        expected=['A','B','C']
        print('result:',result)
        print('expected:',expected)
        
        self.assertListEqual(result, expected)
        print('\t\t mark += 6')
        Test.mark+=6
        print()

    def test5_minimumPath(self):
        
        print('Case 4: path with distance 4')
        result=self.g.minimumPath('A','F')
        expected=['A', 'B', 'E', 'F']
        print('result:',result)
        print('expected:',expected)
        
        self.assertListEqual(result, expected)
        print('\t\t mark += 6')
        Test.mark+=6
        print()
        

 


if __name__ == '__main__': 
    unittest.main()