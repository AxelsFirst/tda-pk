import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402


class TestCheckNesting(unittest.TestCase):

    def check(self, n):

        lower_simplices = self.vrc.find_faces_with_dim(n)
        higher_simplices = self.vrc.find_faces_with_dim(n + 1)

        boundary = self.vrc.check_nesting(
            higher_simplices,
            lower_simplices
        )

        for k in boundary.keys():
            self.assertEqual(len(k), n + 2)

        for v in boundary.values():
            for simplex in v:
                self.assertEqual(len(simplex), n + 1)

        # Keys are (n+1)-simplexes
        # Values are lists of n-simplexes
        for k, v in boundary.items():
            for simplex in v:
                s1 = set([p.name for p in k])
                s2 = set([p.name for p in simplex])
                self.assertTrue(s2.issubset(s1))

    def test_check_nesting_G1(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G1']['names'],
            coords=graphs['G1']['coords'],
            epsilon=graphs['G1']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        lower_simplices = self.vrc.find_faces_with_dim(0)
        higher_simplices = self.vrc.find_faces_with_dim(1)

        self.assertEqual(len(lower_simplices), 4)
        self.assertEqual(len(higher_simplices), 6)

        boundary = self.vrc.check_nesting(
            higher_simplices,
            lower_simplices
        )

        self.assertEqual(len(boundary), 6)

        for k, v in boundary.items():
            for simplex in v:
                self.assertEqual(len(simplex), 1)

        # Keys are 1-simplexes, which are made of two 0-simplexes.
        for k, v in boundary.items():
            p1, p2 = k
            self.assertIn(tuple([p1]), v)
            self.assertIn(tuple([p2]), v)

    def test_check_nesting_G2(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G2']['names'],
            coords=graphs['G2']['coords'],
            epsilon=graphs['G2']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)
        self.check(2)

    def test_check_nesting_G3(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G3']['names'],
            coords=graphs['G3']['coords'],
            epsilon=graphs['G3']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)
        self.check(2)

    def test_check_nesting_G4(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G4']['names'],
            coords=graphs['G4']['coords'],
            epsilon=graphs['G4']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)
        self.check(2)

    def test_check_nesting_G5(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G5']['names'],
            coords=graphs['G5']['coords'],
            epsilon=graphs['G5']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        lower_simplices = self.vrc.find_faces_with_dim(1)
        higher_simplices = self.vrc.find_faces_with_dim(2)

        self.assertEqual(len(lower_simplices), 6)
        self.assertEqual(len(higher_simplices), 2)

        boundary = self.vrc.check_nesting(
            higher_simplices,
            lower_simplices
        )

        self.assertEqual(len(boundary), 2)

        for k in boundary.keys():
            self.assertEqual(len(k), 3)

        for k, v in boundary.items():
            for simplex in v:
                self.assertEqual(len(simplex), 2)

        # Keys are 2-simplexes, which are made of 1-simplexes.
        for k, v in boundary.items():
            for simplex in v:
                s1 = set([p.name for p in k])
                s2 = set([p.name for p in simplex])
                self.assertTrue(s2.issubset(s1))

    def test_check_nesting_G6(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G6']['names'],
            coords=graphs['G6']['coords'],
            epsilon=graphs['G6']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)

    def test_check_nesting_G7(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G7']['names'],
            coords=graphs['G7']['coords'],
            epsilon=graphs['G7']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)

    def test_check_nesting_G8(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G8']['names'],
            coords=graphs['G8']['coords'],
            epsilon=graphs['G8']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)
        self.check(2)
        self.check(3)

    def test_check_nesting_G9(self):
        self.vrc = VietorisRipsComplex.from_list(
            names=graphs['G9']['names'],
            coords=graphs['G9']['coords'],
            epsilon=graphs['G9']['epsilon']
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        self.check(0)
        self.check(1)
        self.check(2)
        self.check(3)


if __name__ == '__main__':
    unittest.main()
