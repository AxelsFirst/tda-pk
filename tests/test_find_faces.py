import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


class TestFindFaces(unittest.TestCase):

    def test_find_faces_4_vertices(self):
        names = ['A', 'B', 'C', 'D']
        coords = [[0, 0], [1, 0], [0, 1], [1, 1]]

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )

        self.vcr.create_graph()
        self.vcr.find_simplices()

        faces = list(self.vcr.find_faces())

        self.assertEqual(len(list(filter(lambda x: len(x) == 1, faces))), 4)
        self.assertEqual(len(list(filter(lambda x: len(x) == 2, faces))), 6)
        self.assertEqual(len(list(filter(lambda x: len(x) == 3, faces))), 4)
        self.assertEqual(len(list(filter(lambda x: len(x) == 4, faces))), 1)

        names = list()
        for face in faces:
            names.append(''.join(sorted(p.name for p in face)))
        names.sort()
        names = ''.join(names)
        self.assertEqual(names, 'AABABCABCDABDACACDADBBCBCDBDCCDD')

    def test_find_faces_2_disconnected_graphs(self):
        names = ['A', 'B', 'C', 'D', 'E', 'F']
        coords = [[0, 0], [1, 0], [0, 1],
                  [10, 10], [11, 10], [11, 11]]

        self.vcr = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=2
        )

        self.vcr.create_graph()
        self.vcr.find_simplices()

        faces = list(self.vcr.find_faces())

        self.assertEqual(len(list(filter(lambda x: len(x) == 1, faces))), 6)
        self.assertEqual(len(list(filter(lambda x: len(x) == 2, faces))), 6)
        self.assertEqual(len(list(filter(lambda x: len(x) == 3, faces))), 2)

        names = list()
        for face in faces:
            names.append(''.join(sorted(p.name for p in face)))
        names.sort()
        names = ''.join(names)

        self.assertEqual(names, 'AABABCACBBCCDDEDEFDFEEFF')


if __name__ == '__main__':
    unittest.main()
