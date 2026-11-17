"""Independent final-state check and topology check for the published exhibit."""

import cmath
import json
import math
import struct
import unittest
from collections import Counter

from tools import print_relief as relief


def direct_probability(case, gamma_delta, beta_delta):
    """Small reference: propagate the *whole* state through all five layers."""
    n = len(case['h'])
    e = relief.energies(case['J'], case['h'])
    psi = [2**(-n/2)] * 2**n
    gammas, betas = list(case['gamma']), list(case['beta'])
    gammas[-1] += gamma_delta
    betas[-1] += beta_delta
    for g, b in zip(gammas, betas):
        psi = [z*cmath.exp(1j*g*v) for z, v in zip(psi, e)]
        c, s = math.cos(b), -1j*math.sin(b)
        for k in range(n):
            psi = [c*z + s*psi[i ^ (1 << k)] for i, z in enumerate(psi)]
    low = min(e)
    return sum(abs(z)**2 for z, v in zip(psi, e) if v <= low + 1e-9)


class ReliefTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((relief.ROOT/'exhibits/qaoa-case-0.json').read_text())
        cls.rows = relief.sample(cls.case)

    def test_slice_matches_full_state(self):
        end = relief.GRID-1
        for x, y in [(end//2, end//2), (end, 0), (3, 9)]:
            with self.subTest(x=x, y=y):
                p = direct_probability(self.case, relief.RADIUS*(2*y/end-1), relief.RADIUS*(2*x/end-1))
                self.assertAlmostEqual(self.rows[y][x], p, places=11)
        self.assertAlmostEqual(self.rows[end//2][end//2], 0.46958855, places=7)

    def test_tied_ground_states_are_summed(self):
        case = dict(J=[[0, 0], [0, 0]], h=[0, 0], gamma=[.2], beta=[.3])
        self.assertTrue(all(abs(p-1) < 1e-12 for row in relief.sample(case) for p in row))

    def test_published_mesh_is_closed_and_uses_sample_heights(self):
        stl = (relief.ROOT/'exhibits/qaoa-relief.stl').read_bytes()
        count, = struct.unpack_from('<I', stl, 80)
        end = relief.GRID-1
        self.assertEqual(count, 2*end**2 + 12*end)
        self.assertEqual(len(stl), 84 + 50*count)
        edges = Counter()
        tops = set()
        for *f, _ in struct.iter_unpack('<12fH', stl[84:]):
            vertices = [tuple(f[i:i+3]) for i in (3, 6, 9)]
            for a, b in zip(vertices, vertices[1:]+vertices[:1]):
                edges[a, b] += 1
            for x, y, z in vertices:
                if z != 0:
                    i, j = round(x*end/64), round(y*end/64)
                    self.assertAlmostEqual(z, 1.5 + 66*self.rows[j][i], places=5)
                    tops.add((i, j))
        self.assertEqual(len(tops), relief.GRID**2)
        self.assertTrue(all(n == 1 and edges[b, a] == 1 for (a, b), n in edges.items()))


if __name__ == '__main__':
    unittest.main()
