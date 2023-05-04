import unittest
from main import getIndices

class Test(unittest.TestCase):

    #variable estática para almacenar la nota
    mark=0
    
    def setUp(self):
      self.x=5
      self.y=8
      self.z=1
      self.input=[5,0,5,1,2,5,5,5,0]

    def test1_getIndices(self):
      print('Caso 1: data es [] (nota: 0.5)')
      print('input:',[],'value:',self.x)
      self.assertEqual(getIndices([],self.x), [], 'FAIL: debería ser []')
      print('\t\t mark += 5')
      Test.mark+=5

    def test2_getIndices(self):
      print('...Caso 2: x no existe en data (nota: 0.5)')
      print('input:',self.input,'value:',self.y)
      self.assertEqual(getIndices(self.input,self.y), [], 'FAIL: debería ser []')
      print('\t\t mark += 5')
      Test.mark+=5

    def test3_getIndices(self):
      print('...Caso 3: x existe sólo una vez\n.')
      result=getIndices(self.input,self.z)
      expected=[self.input.index(self.z)]
      print('input:',self.input,'value:',self.z)
      print('result:',result)
      print('expected:',expected)
      self.assertListEqual(result,expected, 'FAIL: debería ser []')
      print('\t\t mark += 5')
      Test.mark+=5

    def test4_getIndices(self):
      print('...Caso 4: x existe varias veces\n.')
      result=getIndices(self.input,self.x)
      expected=[0, 2, 5, 6,7]

      print('input:',self.input,'value:',self.z)
      print('result:',result)
      print('expected:',expected)

      self.assertListEqual(result,expected, 'FAIL: debería ser [0, 2, 5, 7]')
      print('\t\t mark += 5')
      Test.mark+=5

    def test_printNota(self):
      print('\n\n*************************')
      print("\n\t Provisional mark:  ",Test.mark)  
      print('*************************')


#Comentar para usarlo en spyder
#unittest.main(argv=['first-arg-is-ignored'], exit=False)

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    unittest.main()
