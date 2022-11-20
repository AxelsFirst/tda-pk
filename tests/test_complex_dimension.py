import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402


class TestComplexDimension(unittest.TestCase):

    def test_complex_dimension_G1(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G1']['names'],
            coords=graphs['G1']['coords'],
            epsilon=graphs['G1']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 3)

    def test_complex_dimension_G2(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G2']['names'],
            coords=graphs['G2']['coords'],
            epsilon=graphs['G2']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 2)

    def test_complex_dimension_G3(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G3']['names'],
            coords=graphs['G3']['coords'],
            epsilon=graphs['G3']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 2)

    def test_complex_dimension_G4(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G4']['names'],
            coords=graphs['G4']['coords'],
            epsilon=graphs['G4']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 0)

    def test_complex_dimension_G5(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G5']['names'],
            coords=graphs['G5']['coords'],
            epsilon=graphs['G5']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 2)

    def test_complex_dimension_G6(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G6']['names'],
            coords=graphs['G6']['coords'],
            epsilon=graphs['G6']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 2)

    def test_complex_dimension_G7(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G7']['names'],
            coords=graphs['G7']['coords'],
            epsilon=graphs['G7']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 2)

    def test_complex_dimension_G8(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G8']['names'],
            coords=graphs['G8']['coords'],
            epsilon=graphs['G8']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 4)

    def test_complex_dimension_G9(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G9']['names'],
            coords=graphs['G9']['coords'],
            epsilon=graphs['G9']['epsilon']
        )

        self.assertEqual(self.vrc.complex_dimension, 9)


if __name__ == '__main__':
    unittest.main()
