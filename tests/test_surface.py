# -*- coding: utf-8 -*-

import unittest

import numpy as np

from mckit.surface import Plane
from mckit.transformation import Transformation


tr_glob = Transformation(translation=[1, 2, -3], indegrees=True,
                         rotation=[30, 60, 90, 120, 30, 90, 90, 90, 0])


class TestPlaneSurface(unittest.TestCase):
    def test_plane_creation(self):
        for i, (v, k, tr, v_ref, k_ref) in enumerate(plane_creation_cases):
            with self.subTest(i=i):
                p = Plane(v, k, transform=tr)
                self.assertAlmostEqual(p._k, k_ref)
                for j in range(3):
                    self.assertAlmostEqual(p._v[j], v_ref[j])

    def test_point_test(self):
        plane = Plane([1, 0, 0], 0, tr_glob)
        for i, (p, ans) in enumerate(plane_point_test_cases):
            with self.subTest(i=i):
                p1 = tr_glob.apply2point(p)
                sense = plane.test_point(p1)
                if isinstance(sense, np.ndarray):
                    for s, a in zip(sense, ans):
                        self.assertEqual(s, a)
                else:
                    self.assertEqual(sense, ans)

    def test_region_test(self):
        for i, (v, k, ans) in enumerate(plane_region_test_cases):
            with self.subTest(i=i):
                plane = Plane(v, k)
                result = plane.test_region(region)
                self.assertEqual(result, ans)


plane_creation_cases = [
    (np.array([0, 0, 1]), -2, None, np.array([0, 0, 1]), -2),
    (np.array([0, 0, 1]), -2, tr_glob, np.array([0, 0, 1]), 1),
    (np.array([1, 0, 0]), -2, None, np.array([1, 0, 0]), -2),
    (np.array([1, 0, 0]), -2, tr_glob, np.array([np.sqrt(3) / 2, 0.5, 0]), -3 - 0.5 * np.sqrt(3)),
    (np.array([0, 1, 0]), -2, None, np.array([0, 1, 0]), -2),
    (np.array([0, 1, 0]), -2, tr_glob, np.array([-0.5, np.sqrt(3) / 2, 0]), -1.5 - np.sqrt(3))
]

plane_point_test_cases = [
    (np.array([1, 0, 0]), +1), (np.array([-1, 0, 0]), -1),
    (np.array([1, 0, 0]), +1), (np.array([-1, 0, 0]), -1),
    (np.array([0.1, 0, 0]), +1), (np.array([-0.1, 0, 0]), -1),
    (np.array([1.e-6, 100, -300]), +1), (np.array([-1.e-6, 200, -500]), -1),
    (np.array([[1, 0, 0], [-1, 0, 0], [0.1, 0, 0], [-0.1, 0, 0], [1.e-6, 100, -300],
               [-1.e-6, 200, -500]]), np.array([1, -1, 1, -1, 1, -1]))
]

region = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1],
                   [1, -1, -1],  [1, -1, 1],  [1, 1, -1],  [1, 1, 1]])
plane_region_test_cases = [
    ([1, 0, 0], 0, 0),
    ([1, 0, 0], 1.001, 1),
    ([1, 0, 0], -1.001, -1),
    ([1, 0, 0], 0.999, 0),
    ([1, 0, 0], -0.999, 0),
    ([0, 1, 0], 0, 0),
    ([0, 1, 0], 1.001, 1),
    ([0, 1, 0], -1.001, -1),
    ([0, 1, 0], 0.999, 0),
    ([0, 1, 0], -0.999, 0),
    ([0, 0, 1], 0, 0),
    ([0, 0, 1], 1.001, 1),
    ([0, 0, 1], -1.001, -1),
    ([0, 0, 1], 0.999, 0),
    ([0, 0, 1], -0.999, 0),
    ([1, 1, 1], -2.999, 0),
    ([1, 1, 1], -3.001, -1),
    ([1, 1, 1], 2.999, 0),
    ([1, 1, 1], 3.001, 1)
]