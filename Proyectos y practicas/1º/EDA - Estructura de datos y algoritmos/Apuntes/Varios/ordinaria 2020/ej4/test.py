import unittest
from main import are_adjacent

class Test(unittest.TestCase):
  
    #static attribute to store the provisional mark
    mark=0
    
    def setUp(self):
      self.c1='e'
      self.c2='f'

    def test1_are_adjacent(self):
      print('Case 1: w=None')
      self.assertFalse(are_adjacent(None, self.c1,self.c2))
      print('\t\t mark += 0.3')
      Test.mark+=0.3

    def test2_are_adjacent(self):
      print('Case 2: len(w)=0 ')
      self.assertFalse(are_adjacent('', self.c1,self.c2))
      print('\t\t mark += 0.3')
      Test.mark+=0.3

    def test3_are_adjacent(self):
      print('Case 3: len(w)=1 ')
      self.assertFalse(are_adjacent('', self.c1,self.c2))
      print('\t\t mark += 0.3')
      Test.mark+=0.3

    def test4_are_adjacent(self):
      print('Caso 4: w=ef, c1=e, c2=f - are adjacent')
      w='ef'
      self.assertTrue(are_adjacent(w, self.c1,self.c2),'FAIL: for w=ef should be True')
      print('\t\t mark += 0.55')
      Test.mark+=0.55

    def test5_are_adjacent(self):
      print('Caso 5: w=ez, c1=e, c2=f - are not adjacent')
      w='ez'
      self.assertFalse(are_adjacent(w, self.c1,self.c2),'FAIL: for w=ez should be False')
      print('\t\t mark += 0.55')
      Test.mark+=0.55

    def test6_are_adjacent(self):
      print('Case 6: len(w)>2, w=ezf, c1=e,c2=f - are not adjacent')
      w='ezf'
      self.assertFalse(are_adjacent(w, self.c1,self.c2),'FAIL: for w=ezf should be  False')
      print('\t\t mark += 1')
      Test.mark+=1

    def test7_are_adjacent(self):
      print('Case 7: len(w)>2, w=aezfefg, c1=e,c2=f - are adjacent')
      w='aezfefg'
      self.assertTrue(are_adjacent(w, self.c1,self.c2),'FAIL: for w=aezfefg should be True')
      print('\t\t mark += 1')
      Test.mark+=1


    def test8_are_adjacent(self):
      print('Case 8: len(w)>2, w=aezfeg, c1=e,c2=f - are not adjacent')
      w='aezfeg'
      self.assertFalse(are_adjacent(w, self.c1,self.c2),'FAIL: for w=aezfeg should be  False')
      print('\t\t mark += 1')
      Test.mark+=1



    def test_printMark(self):
      print('\n\n*************************************')
      print("\tProvisional Mark:",Test.mark)  
      print('*************************************')


#For google colab
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Uncomment for Spyder
if __name__ == '__main__':
    unittest.main()
