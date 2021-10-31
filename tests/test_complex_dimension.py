import os
import sys
import unittest
import string

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


class TestComplexDimension(unittest.TestCase):

    def test_complex_dimension_4_points(self):
        coords = [[0, 0], [1, 0], [0, 1], [1, 1]]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()
        self.assertEqual(self.vrc.complex_dimension, 3)

    def test_complex_dimension_3_points(self):
        coords = [[0, 0], [1, 0], [0, 1]]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=1e-9
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()
        self.assertEqual(self.vrc.complex_dimension, 0)


if __name__ == '__main__':
    unittest.main()
