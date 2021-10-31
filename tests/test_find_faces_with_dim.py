import os
import sys
import unittest
import string
import random

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


class TestFindFacesWithDim(unittest.TestCase):

    def test_find_faces_with_dim_4_vertices(self):
        names = ['A', 'B', 'C', 'D']
        coords = [[0, 0], [1, 0], [0, 1], [1, 1]]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 4)

    def test_find_faces_with_dim_random_graph_1(self):
        names = string.ascii_uppercase[:10]
        coords = [
            [0.05, 0.87],
            [0.40, 0.08],
            [0.90, 0.38],
            [0.53, 0.32],
            [0.85, 0.60],
            [0.33, 0.34],
            [0.24, 0.02],
            [0.43, 0.88],
            [0.59, 0.70],
            [0.31, 0.48],
        ]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1/2
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 22)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 19)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 7)

    def test_find_faces_with_dim_random_graph_2(self):
        names = string.ascii_uppercase[:10]
        coords = [
            [0.533, 0.529],
            [0.627, 0.981],
            [0.031, 0.280],
            [0.824, 0.075],
            [0.667, 0.698],
            [0.216, 0.677],
            [0.126, 0.859],
            [0.511, 0.944],
            [0.128, 0.040],
            [0.091, 0.493]
        ]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=2
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 45)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 120)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 210)

    def test_find_faces_with_dim_random_graph_3(self):
        random.seed(123456)
        names, coords = list(), list()
        for i in range(10):
            names.append(str(i))
            coords.append([random.random() for _ in range(2)])

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=3/4
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 35)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 60)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 55)


if __name__ == '__main__':
    unittest.main()
