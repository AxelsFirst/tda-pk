import os
import sys
import unittest
import string
import random

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402

class TestCreateGraph(unittest.TestCase):

    def test_create_graph_4_points(self):
        coords = [[0, 0], [1, 0], [0, 1], [1, 1]]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vrc.create_graph()

        self.assertIsNotNone(self.vrc.graph)

        number_of_edges = int(len(names) * (len(names) - 1) / 2)
        self.assertEqual(self.vrc.graph.number_of_edges(), number_of_edges)
        for p1 in self.vrc.points:
            for p2 in self.vrc.points:
                if p1 != p2:
                    self.assertTrue(self.vrc.graph.has_edge(p1, p2))

    def test_create_graph_7_points(self):
        coords = [
            [1.0, 0.0],
            [0.623, 0.782],
            [-0.223, 0.975],
            [-0.901, 0.434],
            [-0.901, -0.434],
            [-0.223, -0.975],
            [0.623, -0.782],
            [0, 0]
        ]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1
        )

        self.vrc.create_graph()

        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 9)

    def test_create_graph_3_points(self):
        coords = [[0, 0], [0, 1], [1, 0]]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1e-9
        )

        self.vrc.create_graph()

        self.assertIsNotNone(self.vrc.graph)
        self.assertEqual(self.vrc.graph.number_of_edges(), 0)

        for p1 in self.vrc.points:
            for p2 in self.vrc.points:
                if p1 != p2:
                    self.assertFalse(self.vrc.graph.has_edge(p1, p2))