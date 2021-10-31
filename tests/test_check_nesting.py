import os
import sys
import unittest
import string

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


class TestCheckNesting(unittest.TestCase):

    def test_check_nesting_5_points(self):
        coords = [[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5]]
        names = string.ascii_uppercase[:len(coords)]

        self.vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vrc.create_graph()
        self.vrc.find_simplices()

        # Find all 0-simplexes.
        lower_simplices = self.vrc.find_faces_with_dim(0)

        # Find all 1-simplexes.
        higher_simplices = self.vrc.find_faces_with_dim(1)

        # There are 5 0-simplexes in a connected graph with 5 nodes.
        self.assertEqual(len(lower_simplices), 5)

        # There are 10 1-simplexes in a connected graph with 5 nodes.
        self.assertEqual(len(higher_simplices), 10)

        # Check which 0-simplexes are nested in 1-simplexes.
        boundary = self.vrc.check_nesting(
            higher_simplices,
            lower_simplices
        )

        # In a complete graph there are 10 choose 2 sides.
        self.assertEqual(len(boundary), 10)

        for k, v in boundary.items():
            for simplex in v:
                self.assertEqual(len(simplex), 1)

        # Keys are 1-simplexes, which are made of two 0-simplexes.
        for k, v in boundary.items():
            p1, p2 = k
            self.assertIn(tuple([p1]), v)
            self.assertIn(tuple([p2]), v)


if __name__ == '__main__':
    unittest.main()
