import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402


class TestFindSimplices(unittest.TestCase):

    def test_find_simplices_G1(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G1']['names'],
            coords=graphs['G1']['coords'],
            epsilon=graphs['G1']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 1)
        names = sorted(p.name for p in simplices[0])
        self.assertEqual(names, ['A', 'B', 'C', 'D'])

    def test_find_simplices_G2(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G2']['names'],
            coords=graphs['G2']['coords'],
            epsilon=graphs['G2']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 1)
        names = sorted(p.name for p in simplices[0])
        self.assertEqual(names, ['A', 'B', 'C'])

    def test_find_simplices_G3(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G3']['names'],
            coords=graphs['G3']['coords'],
            epsilon=graphs['G3']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 7)

    def test_find_simplices_G4(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G4']['names'],
            coords=graphs['G4']['coords'],
            epsilon=graphs['G4']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 6)

    def test_find_simplices_G5(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G5']['names'],
            coords=graphs['G5']['coords'],
            epsilon=graphs['G5']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 2)

    def test_find_simplices_G6(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G6']['names'],
            coords=graphs['G6']['coords'],
            epsilon=graphs['G6']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 4)

    def test_find_simplices_G7(self):

        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G7']['names'],
            coords=graphs['G7']['coords'],
            epsilon=graphs['G7']['epsilon']
        )

        self.vrc.create_graph()
        simplices = self.vrc.find_simplices()
        self.assertEqual(len(simplices), 8)

    def test_find_simplices_G8(self):
        pass

    def test_find_simplices_G9(self):
        pass


if __name__ == '__main__':
    unittest.main()
