import unittest

import numpy as np

from mckit.cell import _complement, _intersection, _union, Cell, GeometryNode
from mckit.surface import create_surface, Surface
from mckit.constants import *
from mckit.transformation import Transformation
from mckit.fmesh import Box
from mckit.universe import Universe

from tests.cell_test_data.geometry_test_data import *

surfaces = {}
geoms = []


def setUpModule():
    for name, (kind, params) in surface_data.items():
        surfaces[name] = create_surface(kind, *params, name=name)
    for g in create_geom:
        geoms.append(create_node(g[0], g[1]))

def create_node(kind, args):
    pos = set()
    neg = set()
    for g in args.get('positive', []):
        if isinstance(g, tuple):
            g = create_node(g[0], g[1])
        else:
            g = surfaces[g]
        pos.add(g)
    for g in args.get('negative', []):
        if isinstance(g, tuple):
            g = create_node(g[0], g[1])
        else:
            g = surfaces[g]
        neg.add(g)
    return GeometryNode(kind, positive=pos, negative=neg)


class TestGeometryNode(unittest.TestCase):
    def test_from_polish(self):
        for i, raw_data in enumerate(polish_geoms):
            data = []
            for t in raw_data:
                if isinstance(t, int):
                    data.append(surfaces[t])
                else:
                    data.append(t)
            with self.subTest(i=i):
                g = GeometryNode.from_polish_notation(data)
                self.assertEqual(g, geoms[i])

    def test_complement(self):
        for i, raw_data in enumerate(complement_geom):
            ans = create_node(raw_data[0], raw_data[1])
            with self.subTest(i=i):
                c = geoms[i].complement()
                self.assertEqual(c, ans)

    def test_intersection(self):
        for i, case in enumerate(intersection_geom):
            for j, g in enumerate(case):
                ans = create_node(g[0], g[1])
                with self.subTest(msg='i={0}, j={1}'.format(i, j)):
                    ind = j if j < i else j + 1
                    test = geoms[i].intersection(geoms[ind])
                    if test != ans:
                        print(test, ' =====> ', ans)
                    self.assertEqual(ans, test)

    def test_union(self):
        for i, case in enumerate(union_geom):
            for j, g in enumerate(case):
                ans = create_node(g[0], g[1])
                with self.subTest(msg='i={0}, j={1}'.format(i, j)):
                    ind = j if j < i else j + 1
                    test = geoms[i].union(geoms[ind])
                    if test != ans:
                        print(test, ' =====> ', ans)
                    self.assertEqual(ans, test)

# class TestCell(unittest.TestCase):
#     def test_creation(self):
#         for i, (pol_data, ans_data) in enumerate(ag_polish_data):
#             pol_geom = []
#             for x in pol_data:
#                 if isinstance(x, int):
#                     pol_geom.append(surfaces[x])
#                 else:
#                     pol_geom.append(x)
#             with self.subTest(msg="polish #{0}".format(i)):
#                 ans = [produce_term(a) for a in ans_data]
#                 ans_geom = AdditiveGeometry(*ans)
#                 cell = Cell(pol_geom)
#                 # print(str(ag))
#                 self.assertEqual(cell, ans_geom)
#         for i, ag in enumerate(additives):
#             with self.subTest(msg="additive geom #{0}".format(i)):
#                 cell = Cell(ag)
#                 self.assertEqual(cell, ag)
#
#     def test_intersection(self):
#         for i, ag1 in enumerate(additives):
#             c1 = Cell(ag1, **cell_kwargs)
#             for j, ag2 in enumerate(additives):
#                 with self.subTest(msg='additive i={0}, j={1}'.format(i, j)):
#                     c2 = Cell(ag2)
#                     u = c1.intersection(c2)
#                     ans = [produce_term(a) for a in ag_intersection1[i][j]]
#                     ans_geom = AdditiveGeometry(*ans)
#                     self.assertEqual(u, ans_geom)
#                     self.assertDictEqual(u, c1)
#
#     def test_union(self):
#         for i, ag1 in enumerate(additives):
#             c1 = Cell(ag1, **cell_kwargs)
#             for j, ag2 in enumerate(additives):
#                 with self.subTest(msg='additive i={0}, j={1}'.format(i, j)):
#                     c2 = Cell(ag2)
#                     u = c1.union(c2)
#                     ans = [produce_term(a) for a in ag_union1[i][j]]
#                     ans_geom = AdditiveGeometry(*ans)
#                     self.assertEqual(u, ans_geom)
#                     self.assertDictEqual(u, c1)
#
#     def test_populate(self):
#         for i, ag_out in enumerate(additives):
#             c_out = Cell(ag_out, name='Outer', U=4)
#             cells = []
#             geoms = []
#             for j, ag in enumerate(additives):
#                 if j != i:
#                     cells.append(Cell(ag, name=j))
#                     geoms.append(ag.intersection(ag_out))
#             universe = Universe(cells)
#             with self.subTest(i=i):
#                 output = c_out.populate(universe)
#                 for j in range(len(cells)):
#                     self.assertEqual(output[j], geoms[j])
#                     if 'U' in c_out.keys():
#                         self.assertEqual(c_out['U'], output[j]['U'])
#                         output[j].pop('U')
#                     self.assertDictEqual(output[j], cells[j])
#                 c_out['FILL'] = universe
#                 output = c_out.populate()
#                 for j in range(len(cells)):
#                     self.assertEqual(output[j], geoms[j])
#                     if 'U' in c_out.keys():
#                         self.assertEqual(c_out['U'], output[j]['U'])
#                         output[j].pop('U')
#                     self.assertDictEqual(output[j], cells[j])
#
#     @unittest.expectedFailure  # Surface equality should be developed.
#     def test_transform(self):
#         tr = Transformation(translation=[1, 3, -2])
#         surfaces_tr = {k: s.transform(tr) for k, s in surfaces.items()}
#         for i, (pol_data, ans_data) in enumerate(ag_polish_data):
#             pol_geom = []
#             for x in pol_data:
#                 if isinstance(x, int):
#                     pol_geom.append(surfaces[x])
#                 else:
#                     pol_geom.append(x)
#             with self.subTest(msg="cell transform #{0}".format(i)):
#                 ans = [produce_term(a, surf=surfaces_tr) for a in ans_data]
#                 ans_geom = AdditiveGeometry(*ans)
#                 cell = Cell(pol_geom).transform(tr)
#                 print(str(cell), '->', str(ans_geom), '->', len(cell.terms), '->', len(ans_geom.terms))
#                 self.assertSetEqual(cell.terms, ans_geom.terms)
#
#     # @unittest.skip
#     def test_simplify(self):
#         for i, ag in enumerate(additives):
#             cell = Cell(ag)
#             with self.subTest(i=i):
#                 s = cell.simplify(min_volume=0.1, box=Box([-10, -10, -10], [26, 0, 0], [0, 20, 0], [0, 0, 20]))
#                 # print(i, len(s))
#                 # for ss in s:
#                 #     print(str(ss))
#                 ans = [produce_term(a) for a in ag_simplify[i]]
#                 ans_geom = AdditiveGeometry(*ans)
#                 self.assertEqual(ans_geom == s, True)


class TestOperations(unittest.TestCase):
    def test_complement(self):
        for i, (arg, ans) in enumerate(cell_complement_cases):
            with self.subTest(i=i):
                comp = _complement(np.array(arg))
                if isinstance(comp, np.ndarray):
                    for x, y in zip(ans, comp):
                        self.assertEqual(x, y)
                else:
                    self.assertEqual(comp, ans)

    def test_intersection(self):
        for i, (arg1, arg2, ans) in enumerate(cell_intersection_cases):
            with self.subTest(i=i):
                res = _intersection(arg1, arg2)
                if isinstance(res, np.ndarray):
                    for x, y in zip(ans, res):
                        self.assertEqual(x, y)
                else:
                    self.assertEqual(res, ans)

    def test_union(self):
        for i, (arg1, arg2, ans) in enumerate(cell_union_cases):
            with self.subTest(i=i):
                res = _union(arg1, arg2)
                if isinstance(res, np.ndarray):
                    for x, y in zip(ans, res):
                        self.assertEqual(x, y)
                else:
                    self.assertEqual(res, ans)


if __name__ == '__main__':
    unittest.main()
