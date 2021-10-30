import os
import sys
import unittest

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


if __name__ == '__main__':
    unittest.main()
