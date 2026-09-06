# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 21:06:49 2022

@author: ishernanz
"""
import unittest
from parcial281 import MyBST


class Test(unittest.TestCase):

    mark=0

    def setUp(self):
        self.T0,self.T1,self.T2,self.T3,self.T4,self.T5,self.T6,self.T7,self.T8,self.T9=MyBST(),MyBST(),MyBST(),MyBST(),MyBST(),MyBST(),MyBST(),MyBST(),MyBST(),MyBST()
        
        L2=[1,2,3,4,5,6,7,8,9,10,11]
        L3=[11,10,9,8,7,6,5,4,3,2,1]
        L4=[7,6,5,1,2,3,4]
        L5=[5,4,6,3,7,2,8,1,9]
        L6=[5,3,6,2,4,7,1]
        L7=[5,4,7,2,6,1,3]
        L8=[7,3,8,2,6,1,5,4]
        L9=[4,2,10,1,3,6,11,5,9,16,8,13,7,12,15,14]
        
        self.T1.insert(1)
        for i in L2:    
            self.T2.insert(i)
        
        for i in L3:
            self.T3.insert(i)
            
        for i in L4:
            self.T4.insert(i)
        
        for i in L5:
            self.T5.insert(i)
            
        for i in L6:
            self.T6.insert(i)
            
        for i in L7:
            self.T7.insert(i)
            
        for i in L8:
            self.T8.insert(i)
            
        for i in L9:
            self.T9.insert(i)
            
    def test1_emptyTree(self):  
        #T0: empty tree
        self.assertEqual(0,self.T0.get_diam(),'FAIL: should be none for an empty tree')
        
        print('test1_emptyTree was OK!!!: ', 0)
        Test.mark+=0.25
        
    def test2_1ElemTree(self):  
        #T1: single element tree
        self.assertEqual(1,self.T1.get_diam(),'FAIL: should be 1 for a single element tree')
        
        print('test2_1ElemTree was OK!!!: ', 1)
        Test.mark+=0.75
        
    def test2_RightUnbalancedTree(self):  
        #T2:Right unbalanced tree
        self.assertEqual(11,self.T2.get_diam(),'FAIL: should be 11 for this tree')
        
        print('test2_RightUnbalancedTree was OK!!!: ', 11)
        Test.mark+=0.5    
       
    def test3_LeftUnbalancedTree(self):  
        #T3: left unbalanced tree
        self.assertEqual(11,self.T3.get_diam(),'FAIL: should be be 11 for this tree')
        
        print('test3_LeftUnbalancedTree was OK!!!: ', 11)
        Test.mark+=0.5
        
    def test4_LeftRightUnbalancedTree(self):  
        #T4: left-right unbalanced tree
        self.assertEqual(7,self.T4.get_diam(),'FAIL: should be be 11 for this tree')
        
        print('test4_LefRighttUnbalancedTree was OK!!!: ', 7)
        Test.mark+=0.5 
        
    def test5_FullBalancedRootTree(self):  
        #T5: Full balanced root tree
        self.assertEqual(9,self.T5.get_diam(),'FAIL: should be be 9 for this tree')
        
        print('test5_FullBalancedRootTree was OK!!!: ', 7)
        Test.mark+=1
    def test6_get_diamThoughRootTree1(self):  
        #T6: get_diameter through root tree 1
        self.assertEqual(6,self.T6.get_diam(),'FAIL: should be be 6 for this tree')
        
        print('test6_get_diamThoughRootTree1 was OK!!!: ', 6)
        Test.mark+=0.5 
        
    def test7_get_diamThoughRootTree2(self):  
        #T7: get_diameter through root tree 2
        self.assertEqual(6,self.T7.get_diam(),'FAIL: should be be 6 for this tree')
        
        print('test7_get_diamThoughRootTree2 was OK!!!: ', 6)
        Test.mark+=1
        
    def test8_get_diamNotThoughRootTree1(self):  
        #T7: get_diameter not through root tree 1
        self.assertEqual(6,self.T8.get_diam(),'FAIL: should be be 6 for this tree')
        
        print('test8_get_diamNotThoughRootTree1 was OK!!!: ', 6)
        Test.mark+=2.5
        
    def test9_get_diamNotThoughRootTree2(self):  
        #T7: get_diameter not through root tree 2
        self.assertEqual(10,self.T9.get_diam(),'FAIL: should be be 10 for this tree')
        
        print('test9_get_diamNotThoughRootTree2 was OK!!!: ', 10)
        
        Test.mark+=2.5
        
    def test_showmark(self):
        print('Total mark is ', Test.mark)    
        
if __name__ == '__main__':
    unittest.main()
    