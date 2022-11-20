import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402


class TestCreateGraph(unittest.TestCase):

    def test_create_G1(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G1']['names'],
            coords=graphs['G1']['coords'],
            epsilon=graphs['G1']['epsilon']
        )

        self.vrc.create_graph()

        self.assertIsNotNone(self.vrc.graph)

        # The number of edges in a connected graph is n * (n - 1) / 2
        n = len(graphs['G1']['names'])
        number_of_edges = int(n * (n - 1) / 2)
        self.assertEqual(self.vrc.graph.number_of_edges(), number_of_edges)

        # In a connected graph, each there should be an edge between each
        # distinct pair of nodes.
        for p1 in self.vrc.points:
            for p2 in self.vrc.points:
                if p1 != p2:
                    self.assertTrue(self.vrc.graph.has_edge(p1, p2))

    def test_create_G2(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G2']['names'],
            coords=graphs['G2']['coords'],
            epsilon=graphs['G2']['epsilon']
        )

        self.vrc.create_graph()

        self.assertIsNotNone(self.vrc.graph)

        # The number of edges in a connected graph is n * (n - 1) / 2
        n = len(graphs['G2']['names'])
        number_of_edges = int(n * (n - 1) / 2)
        self.assertEqual(self.vrc.graph.number_of_edges(), number_of_edges)

    def test_create_G3(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G3']['names'],
            coords=graphs['G3']['coords'],
            epsilon=graphs['G3']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 14)

    def test_create_G4(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G4']['names'],
            coords=graphs['G4']['coords'],
            epsilon=graphs['G4']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 0)

    def test_create_G5(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G5']['names'],
            coords=graphs['G5']['coords'],
            epsilon=graphs['G5']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 6)

    def test_create_G6(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G6']['names'],
            coords=graphs['G6']['coords'],
            epsilon=graphs['G6']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 10)

    def test_create_G7(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G7']['names'],
            coords=graphs['G7']['coords'],
            epsilon=graphs['G7']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 14)

    def test_create_G8(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G8']['names'],
            coords=graphs['G8']['coords'],
            epsilon=graphs['G8']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 22)

    def test_create_G9(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G9']['names'],
            coords=graphs['G9']['coords'],
            epsilon=graphs['G9']['epsilon']
        )

        self.vrc.create_graph()
        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 45)


if __name__ == '__main__':
    unittest.main()
