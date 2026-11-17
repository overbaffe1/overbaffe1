"""Export the rest-pose geometry of the MyWorkAiBrain lighthouse for GitHub's STL viewer."""

import hashlib
import json
import struct
import sys
from math import hypot
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# This is an exhibit-specific export, not a general-purpose glTF reader. In this
# asset, mesh positions are in model space at bind pose; mesh nodes have no TRS.
SOURCE_SHA256 = 'ad919db4755b7dc76b0a94009773b46a78bf247b21dbc9d5353582418be90f0e'


def export(source):
    glb = source.read_bytes()
    if hashlib.sha256(glb).hexdigest() != SOURCE_SHA256:
        raise SystemExit('Expected the lighthouse.glb revision documented in exhibits/README.md')
    json_size, = struct.unpack_from('<I', glb, 12)
    scene = json.loads(glb[20:20 + json_size])
    data = memoryview(glb)[28 + json_size:]

    def unpack(accessor_id, fmt):
        a = scene['accessors'][accessor_id]
        view = scene['bufferViews'][a['bufferView']]
        offset = view.get('byteOffset', 0) + a.get('byteOffset', 0)
        stride = view.get('byteStride', struct.calcsize(fmt))
        return [struct.unpack_from(fmt, data, offset + i * stride) for i in range(a['count'])]

    facets = bytearray()
    for mesh in scene['meshes']:
        for part in mesh['primitives']:
            # An opaque STL light cone or glass cylinder would hide the lantern.
            if scene['materials'][part['material']]['name'] in {'beam', 'beamcore', 'glass'}:
                continue
            # glTF Y-up to STL Z-up, preserving winding. Set the plinth on z=0.
            points = [(100*x, -100*z, 100*(y + 0.81))
                      for x, y, z in unpack(part['attributes']['POSITION'], '<fff')]
            indices = [index for index, in unpack(part['indices'], '<H')]
            for i in range(0, len(indices), 3):
                a, b, c = (points[j] for j in indices[i:i + 3])
                u = [q - p for p, q in zip(a, b)]
                v = [q - p for p, q in zip(a, c)]
                n = (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])
                length = hypot(*n)
                if length > 1e-8:
                    facets.extend(struct.pack('<12fH', *(x/length for x in n), *a, *b, *c, 0))

    count = len(facets) // 50
    header = struct.pack('<80sI', b'overbaffe1 | MyWorkAiBrain | Lighthouse | bind pose', count)
    path = ROOT / 'exhibits/lighthouse.stl'
    path.write_bytes(header + facets)
    print(f'{path.name}: {count:,} facets, {path.stat().st_size:,} bytes')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 tools/export_lighthouse.py path/to/lighthouse.glb')
    export(Path(sys.argv[1]))
