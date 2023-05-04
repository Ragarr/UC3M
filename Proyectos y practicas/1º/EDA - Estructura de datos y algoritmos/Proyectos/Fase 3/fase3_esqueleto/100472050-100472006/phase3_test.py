import unittest

from phase3 import Graph2

class Graph2Test(unittest.TestCase):
    mark = 0
    """
    Tests:
        - test1: directed_graph.min_number_edges('A', 'B')
        - test2: directed_graph.min_number_edges('A', 'E')
        - test3: directed_graph.min_number_edges('A', 'G')
        - test4: directed_graph.min_number_edges('G', 'A')
        - test5: undirected_graph.min_number_edges('G', 'A')
        - test6: undirected_graph.min_number_edges('E', 'A')
        - test7: directed_graph.transpose()
        - test8: undirected_graph.transpose()

    """
    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.directed_graph = Graph2(self.vertices)
        self.directed_graph.add_edge('A', 'B')
        self.directed_graph.add_edge('A', 'C')
        self.directed_graph.add_edge('B', 'C')
        self.directed_graph.add_edge('B', 'D')
        self.directed_graph.add_edge('C', 'E')
        self.directed_graph.add_edge('D', 'E')
        self.directed_graph.add_edge('E', 'F')
        self.directed_graph.add_edge('F', 'G')
        # print(self.directed_graph)

        self.undirected_graph = Graph2(self.vertices, False)
        self.undirected_graph.add_edge('A', 'B')
        self.undirected_graph.add_edge('A', 'C')
        self.undirected_graph.add_edge('B', 'C')
        self.undirected_graph.add_edge('B', 'D')
        self.undirected_graph.add_edge('C', 'E')
        self.undirected_graph.add_edge('D', 'E')
        self.undirected_graph.add_edge('E', 'F')
        self.undirected_graph.add_edge('F', 'G')
        # print(self.undirected_graph)

    def test1(self):
        """ directed_graph.min_number_edges('A', 'B')"""
        print("\n test1: directed_graph.min_number_edges('A', 'B')")
        actual = self.directed_graph.min_number_edges('A', 'B')
        expected = 1
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.70

    def test2(self):
        """ directed_graph.min_number_edges('A', 'E')"""
        print("\n test2: directed_graph.min_number_edges('A', 'E')")
        actual = self.directed_graph.min_number_edges('A', 'E')
        expected = 2
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.70

    def test3(self):
        """ directed_graph.min_number_edges('A', 'G')"""
        print("\n test3: directed_graph.min_number_edges('A', 'G')")
        actual = self.directed_graph.min_number_edges('A', 'G')
        expected = 4
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.70

    def test4(self):
        """ directed_graph.min_number_edges('G', 'A')"""
        print("\n test4: directed_graph.min_number_edges('G', 'A')")
        actual = self.directed_graph.min_number_edges('G', 'A')
        expected = 0
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.70

    def test5(self):
        """ undirected_graph.min_number_edges('G', 'A')"""
        print("\n test5: undirected_graph.min_number_edges('G', 'A')")
        actual = self.undirected_graph.min_number_edges('G', 'A')
        expected = 4
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.80

    def test6(self):
        """ undirected_graph.min_number_edges('E', 'A')"""
        print("\n test6: undirected_graph.min_number_edges('E', 'A')")
        actual = self.undirected_graph.min_number_edges('E', 'A')
        expected = 2
        print('actual = ', actual)
        print('expected = ', expected)
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.70

    def test7(self):
        """ undirected_graph.transpose """
        print("\n test7: undirected_graph.transpose()")
        actual = self.undirected_graph.transpose()
        expected = self.undirected_graph
        # print('actual = \n', str(actual))
        # print('expected = \n', str(expected))
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.60

    def test8(self):
        """ directed_graph.transpose """
        print("\n test8: directed_graph.transpose()")
        actual = self.directed_graph.transpose()
        expected = Graph2(self.vertices)
        expected.add_edge('B', 'A')
        expected.add_edge('C', 'A')
        expected.add_edge('C', 'B')
        expected.add_edge('D', 'B')
        expected.add_edge('E', 'C')
        expected.add_edge('E', 'D')
        expected.add_edge('F', 'E')
        expected.add_edge('G', 'F')

        # print('actual = \n', str(actual))
        #print('expected = \n', str(expected))
        self.assertEqual(actual, expected)
        Graph2Test.mark += 0.60

    def test9(self):
        """ directed_graph.is_strongly_connected"""
        result = self.directed_graph.is_strongly_connected()
        assert result is not None
        self.assertFalse(result)
        Graph2Test.mark += 0.75

    def test_10(self):
        """ undirected_graph.is_strongly_connected"""
        result = self.undirected_graph.is_strongly_connected()
        assert result is not None
        self.assertTrue(result)
        Graph2Test.mark += 0.75

    def test_11(self):
        """ strongly connected graph """
        labels = ['a', 'b', 'c', 'e']
        graph = Graph2(labels)
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'a')
        result = graph.is_strongly_connected()
        assert result is not None
        self.assertTrue(result)
        Graph2Test.mark += 0.75

    def test_12(self):
        """ strongly connected graph """
        labels = ['a', 'b', 'c', 'e', 'f', 'g']
        graph = Graph2(labels)
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'a')
        graph.add_edge('e', 'f')
        graph.add_edge('f', 'g')
        graph.add_edge('g', 'e')
        result = graph.is_strongly_connected()
        assert result is not None
        self.assertTrue(result)
        Graph2Test.mark += 0.75

    def test_13(self):
        """ débilmente conexo (su no dirigido sería conexo) """
        labels = ['a', 'b', 'c', 'e', 'f', 'g']
        graph = Graph2(labels)
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'a')
        graph.add_edge('f', 'g')
        graph.add_edge('g', 'e')

        result = graph.is_strongly_connected()
        assert result is not None
        self.assertFalse(result)
        Graph2Test.mark += 0.75

    def test_14(self):
        """ (grafo no conexo) """
        labels = ['a', 'b', 'c', 'e', 'f', 'g']
        graph = Graph2(labels, False)
        graph.add_edge('a', 'b')
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'a')
        graph.add_edge('f', 'g')

        result = graph.is_strongly_connected()
        assert result is not None
        self.assertFalse(result)
        Graph2Test.mark += 0.75

    def test_z(self):
        print('Nota provisional: ', Graph2Test.mark)

if __name__ == "__main__":
    unittest.main()
