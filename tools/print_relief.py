"""Print the QAOA exhibit from instance 0. Python 3.10+, offline, no dependencies."""

import cmath
import json
import math
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRID = 25                         # odd: the original pair is a sample, not an interpolation
RADIUS = 0.75                     # radians on either side of the CSV value


def energies(j, h):
    """Bit order and sign convention of overbaffe1/QAOA, QAOA.py."""
    n = len(h)
    pairs = [(a, b, (j[a][b] + j[b][a]) / 2) for a in range(n) for b in range(a)]
    result = []
    for state in range(2**n):
        s = [2 * (state >> (n - 1 - i) & 1) - 1 for i in range(n)]
        result.append(sum(x*y for x, y in zip(h, s)) + sum(w*s[a]*s[b] for a, b, w in pairs))
    return result


def mix(state, beta):
    """Apply the mixer exp(-i beta X) to each qubit, in place."""
    c, s = math.cos(beta), -1j*math.sin(beta)
    stride = 1
    while stride < len(state):
        for start in range(0, len(state), 2*stride):
            for a in range(start, start + stride):
                b = a + stride
                u, v = state[a], state[b]
                state[a], state[b] = c*u + s*v, s*u + c*v
        stride *= 2


def sample(case):
    n = len(case['h'])
    energy = energies(case['J'], case['h'])
    low = min(energy)
    ground = [k for k, e in enumerate(energy) if e <= low + 1e-9]
    state = [1/math.sqrt(len(energy))] * len(energy)
    for gamma, beta in zip(case['gamma'][:-1], case['beta'][:-1]):
        state = [z * cmath.exp(1j*gamma*e) for z, e in zip(state, energy)]
        mix(state, beta)

    delta = [RADIUS * (2*i/(GRID-1) - 1) for i in range(GRID)]
    # In the final mixer the amplitude from k to g depends only on their
    # Hamming distance d: cos(beta)^(n-d) * (-i sin(beta))^d. Group by d so
    # we need not construct 625 full final states just to read P(ground).
    distances = [[(k ^ g).bit_count() for k in range(len(state))] for g in ground]
    weights = [[math.cos(b)**(n-d) * (-1j*math.sin(b))**d for d in range(n+1)]
               for b in (case['beta'][-1] + offset for offset in delta)]
    rows = []                       # y: gamma; x: beta, both increasing
    for offset in delta:
        gamma = case['gamma'][-1] + offset
        phased = [z * cmath.exp(1j*gamma*e) for z, e in zip(state, energy)]
        sums = []
        for dist in distances:
            bins = [0j] * (n+1)
            for d, z in zip(dist, phased):
                bins[d] += z
            sums.append(bins)
        rows.append([sum(abs(sum(w*a for w, a in zip(ws, bins)))**2 for bins in sums)
                     for ws in weights])
    return rows


def solid(rows):
    """Closed Z-up relief. Side and bottom edges match the top grid exactly."""
    end = len(rows) - 1
    pts = [[(64*x/end, 64*y/end, 1.5 + 66*p) for x, p in enumerate(row)]
           for y, row in enumerate(rows)]
    faces = bytearray()

    def triangle(a, b, c):
        ux, uy, uz = (q-p for q, p in zip(b, a))
        vx, vy, vz = (q-p for q, p in zip(c, a))
        normal = (uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx)
        length = math.hypot(*normal)
        faces.extend(struct.pack('<12fH', *(v/length for v in normal), *a, *b, *c, 0))

    for y in range(end):
        for x in range(end):
            a, b = pts[y][x:x+2]
            d, c = pts[y+1][x:x+2]
            triangle(a, b, c)
            triangle(a, c, d)
    rim = pts[0] + [row[-1] for row in pts[1:]] + pts[-1][-2::-1] + [row[0] for row in pts[-2:0:-1]]
    for a, b in zip(rim, rim[1:]+rim[:1]):
        lo, hi = (*a[:2], 0), (*b[:2], 0)
        triangle(lo, hi, b)
        triangle(lo, b, a)
        triangle((32, 32, 0), hi, lo)
    return struct.pack('<80sI', b'overbaffe1 | QAOA | id 0 | x=beta_4 y=gamma_4 z=1.5+66P', len(faces)//50) + faces


def plate(rows):
    """A copperplate impression of the same samples, occluded back to front."""
    end = len(rows) - 1
    peak = max(map(max, rows))

    def point(x, y, p):
        return f'{155 + 106*(x-y)/end:.1f},{102 + 40*(x+y)/end - 74*p/peak:.1f}'

    bands = []
    for y in range(end):
        near = [point(x, y+1, rows[y+1][x]) for x in range(end+1)]
        far = [point(x, y, rows[y][x]) for x in range(end+1)]
        cuts = ' '.join(f'M{a} {b}' for a, b in zip(far[::2], near[::2]))
        bands.append(f'<path d="M{" ".join(far + near[::-1])}Z" fill="#365661"/>'
                     f'<path d="M{" ".join(near)}" fill="none" stroke="#e1c695" stroke-width="1.3"/>'
                     f'<path d="{cuts}" stroke="#87a79f" stroke-width=".6"/>')
    front = [point(x, end, rows[end][x]) for x in range(end+1)] + [point(end, y, rows[y][end]) for y in range(end-1, -1, -1)]
    mid = end//2
    center = point(mid, mid, rows[mid][mid]).split(',')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="310" height="220" viewBox="0 0 310 220" role="img" aria-labelledby="title desc">
  <title id="title">07 · Ландшафт вероятности</title>
  <desc id="desc">Сечение P(ground) для задачи 0. Справа и слева изменяются два угла последнего слоя. Метка на поверхности — исходная пара.</desc>
  <!-- Generated by tools/print_relief.py from exhibits/qaoa-case-0.json. -->
  <defs><pattern id="dust" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r=".65" fill="#779095"/></pattern></defs>
  <path fill="#233e49" d="M0 0h310v220H0z"/><path fill="url(#dust)" d="M9 9h292v202H9z"/>
  <rect x="8.5" y="8.5" width="293" height="203" fill="none" stroke="#859a92"/>
  <path d="M49 142 155 102 261 142v5l-106 40-106-40Z" fill="#152f3b" stroke="#91a09a"/>
  <path d="M{' '.join(front)} L261 147 155 187 49 147Z" fill="#94a598"/>
  {''.join(bands)}
  <circle cx="{center[0]}" cy="{center[1]}" r="3.4" stroke="#263d43" fill="#ff9c70"/>
  <g fill="#f0e2c5" font-family="Consolas,'DejaVu Sans Mono',monospace"><text x="19" y="32" font-size="16">07</text><text x="290" y="202" text-anchor="end" font-size="13">P(ground)</text></g>
</svg>\n'''


if __name__ == '__main__':
    case = json.loads((ROOT/'exhibits/qaoa-case-0.json').read_text())
    rows = sample(case)
    (ROOT/'exhibits/qaoa-relief.stl').write_bytes(solid(rows))
    (ROOT/'assets/qaoa-proof.svg').write_bytes(plate(rows).encode('utf-8'))
    print(f'{GRID}×{GRID} samples, P(center)={rows[GRID//2][GRID//2]:.8f}, max={max(map(max, rows)):.8f}')
