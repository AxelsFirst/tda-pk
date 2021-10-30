import os
import sys
import unittest
import random

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


class TestFindSimplices(unittest.TestCase):

    def test_find_simplices_4_vertices(self):
        names = ['A', 'B', 'C', 'D']
        coords = [[0, 0], [1, 0], [0, 1], [1, 1]]

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vcr.create_graph()

        simplices = self.vcr.find_simplices()

        self.assertEqual(len(simplices), 1)
        names = sorted(p.name for p in simplices[0])
        self.assertEqual(names, ['A', 'B', 'C', 'D'])

    def test_find_simplices_all_disconnected(self):
        names = ['A', 'B', 'C', 'D', 'E', 'F']
        coords = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1/2
        )

        self.vcr.create_graph()

        simplices = self.vcr.find_simplices()
        names = list()
        for simplex in simplices:
            names.append(simplex[0].name)

        self.assertEqual(len(simplices), 6)
        self.assertEqual(sorted(names), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_find_simplices_2_disconnected_graphs(self):
        names = ['A', 'B', 'C', 'D', 'E', 'F']
        coords = [[0, 0], [1, 0], [0, 1],
                  [10, 10], [11, 10], [11, 11]]

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=2
        )

        self.vcr.create_graph()

        simplices = self.vcr.find_simplices()

        self.assertEqual(len(simplices), 2)

        first = tuple(sorted(p.name for p in simplices[0]))
        second = tuple(sorted(p.name for p in simplices[1]))
        graphs = set([first, second])
        self.assertIn(first, graphs)
        self.assertIn(second, graphs)

    def test_find_simplices_random_graph_1(self):
        random.seed(123)
        names, coords = list(), list()
        for i in range(25):
            names.append(str(i))
            coords.append([random.random() for _ in range(2)])

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1/5
        )

        self.vcr.create_graph()

        simplices = self.vcr.find_simplices()
        self.assertEqual(len(simplices), 17)

    def test_find_simplices_random_graph_2(self):
        random.seed(123)
        names, coords = list(), list()
        for i in range(50):
            names.append(str(i))
            coords.append([random.random() for _ in range(2)])

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1/2
        )

        self.vcr.create_graph()

        simplices = self.vcr.find_simplices()
        self.assertEqual(len(simplices), 58)


if __name__ == '__main__':
    unittest.main()
