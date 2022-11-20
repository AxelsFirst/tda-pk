import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402


class TestFindFacesWithDim(unittest.TestCase):

    def test_find_faces_with_dim_G1(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G1']['names'],
            coords=graphs['G1']['coords'],
            epsilon=graphs['G1']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 4)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 6)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 4)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 1)

    def test_find_faces_with_dim_G2(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G2']['names'],
            coords=graphs['G2']['coords'],
            epsilon=graphs['G2']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 3)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 3)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 1)

    def test_find_faces_with_dim_G3(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G3']['names'],
            coords=graphs['G3']['coords'],
            epsilon=graphs['G3']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 8)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 14)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 7)

    def test_find_faces_with_dim_G4(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G4']['names'],
            coords=graphs['G4']['coords'],
            epsilon=graphs['G4']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 6)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 0)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 0)

    def test_find_faces_with_dim_G5(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G5']['names'],
            coords=graphs['G5']['coords'],
            epsilon=graphs['G5']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 6)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 6)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 2)

    def test_find_faces_with_dim_G6(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G6']['names'],
            coords=graphs['G6']['coords'],
            epsilon=graphs['G6']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 7)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 4)

    def test_find_faces_with_dim_G7(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G7']['names'],
            coords=graphs['G7']['coords'],
            epsilon=graphs['G7']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 9)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 14)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 6)

    def test_find_faces_with_dim_G8(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G8']['names'],
            coords=graphs['G8']['coords'],
            epsilon=graphs['G8']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 22)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 19)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 7)

    def test_find_faces_with_dim_G9(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G9']['names'],
            coords=graphs['G9']['coords'],
            epsilon=graphs['G9']['epsilon']
        )

        self.assertEqual(len(self.vrc.find_faces_with_dim(0)), 10)
        self.assertEqual(len(self.vrc.find_faces_with_dim(1)), 45)
        self.assertEqual(len(self.vrc.find_faces_with_dim(2)), 120)
        self.assertEqual(len(self.vrc.find_faces_with_dim(3)), 210)


if __name__ == '__main__':
    unittest.main()
