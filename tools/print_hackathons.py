"""Print the kinetic stamps and their matching stills. No network or packages."""

import json
import math
from collections.abc import Callable
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from xml.sax.saxutils import escape

if __package__:
    from .print_relief import sample
else:  # python3 tools/print_hackathons.py
    from print_relief import sample

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'hackathons'
MONO = "Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Arial,'DejaVu Sans',sans-serif"


def num(x):
    return f'{x:.2f}'.rstrip('0').rstrip('.') if abs(x) >= .005 else '0'


def xy(x, y):
    return f'{num(x)} {num(y)}'


class Exposure:
    """All base attributes are a complete frame. Stills simply omit SMIL."""

    def __init__(self, moving):
        self.moving = moving

    def tween(self, attr, poses, seconds, *, transform=False, times=None, eased=False):
        if not self.moving or len(set(poses)) < 2:
            return ''
        tag = 'animateTransform' if transform else 'animate'
        target = f'attributeName="transform" type="{attr}"' if transform else f'attributeName="{attr}"'
        timing = ''
        if eased and times is None:
            times = [i / (len(poses) - 1) for i in range(len(poses))]
        if times is not None:
            timing += ' keyTimes="' + ';'.join(f'{t:.5f}' for t in times) + '"'
        if eased:
            timing += ' calcMode="spline" keySplines="' + ';'.join(['.42 0 .58 1'] * (len(poses)-1)) + '"'
        return (f'<{tag} {target} values="{";".join(map(str, poses))}" dur="{seconds}s"'
                f'{timing} repeatCount="indefinite"/>')

    def turn(self, start, end, seconds):
        return self.tween('rotate', [start, end], seconds, transform=True)


def polar(r, a):
    return xy(r*math.cos(a), r*math.sin(a))


def guardian(m):
    # The iris moves *behind* the almond aperture. Closing the traced outline
    # and the clipping path together makes the blink a shutter, not a flash.
    def aperture(h):
        return f'M-96 0C-48 {-h} 46 {-h} 96 0C48 {h} -48 {h} -96 0Z'

    blink = m.tween('d', [aperture(h) for h in [44, 44, 3, 44, 44]], 7.2,
                    times=[0, .66, .70, .77, 1], eased=True)
    spokes = ''.join(f'<path d="M{polar(16, a)} Q{polar(23, a+.20)} {polar(29, a+.43)}"/>'
                     for a in (i*math.tau/32 for i in range(32)))
    look = m.tween('translate', ['-10 1', '14 -2', '14 -2', '-10 1'], 7.2,
                   transform=True, times=[0, .44, .7, 1], eased=True)
    blades = ''.join(f'<path transform="rotate({i*60})" d="m-9-18 18 0 6 8-15-4-12 8z"/>' for i in range(6))
    return f'''<defs>
  <path id="aperture" d="{aperture(44)}">{blink}</path>
  <clipPath id="eye"><use href="#aperture"/></clipPath>
</defs>
<g transform="translate(160 60)">
  <g fill="none" stroke="#bdae95" opacity=".65" stroke-width=".8">
    <ellipse rx="119" ry="43" stroke-dasharray="1 5"/><path d="M-137 0h27m220 0h27M-68-32q68-39 137 0m-122 64q53 27 104 0"/>
    <path d="m-103-26-9 3-4 8m219-11 9 3 4 8m-219 41-9-3-4-8m219 11 9-3 4-8"/>
  </g>
  <path d="{aperture(49)}" fill="#1c2934" stroke="#f0c490" stroke-width="1.4"/>
  <use href="#aperture" fill="#ecdbb8"/>
  <g clip-path="url(#eye)"><g transform="translate(-10 1)">{look}
    <circle r="31" fill="#1c3a44"/><circle r="28.8" fill="#87b5a8"/>
    <g fill="none" stroke="#315963" stroke-width="1.45">{m.turn(0, 360, 32)}{spokes}</g>
    <circle r="18.5" fill="#c9956c"/><g fill="#6e6761">{m.turn(0, -360, 24)}{blades}</g>
    <circle r="9.7" fill="#1b3440">{m.tween('r', [9.7, 6.7, 9.7], 7.2, eased=True)}</circle>
    <circle cx="-5" cy="-6" r="2.9" fill="#fff2d9"/>
  </g></g>
  <use href="#aperture" fill="none" stroke="#26333a" stroke-width="1.5"/>
  <path d="m-130 0 5-3v6zm260 0-5-3v6z" fill="#ed9e79"/>
</g>'''


def gear(teeth, pitch, spokes, color, dark, angle, seconds, direction, m):
    # Cut actual slots out of the wheel (even-odd), so the stationary paper
    # shows through. Pitch radii and periods have the same tooth-count ratio.
    root, tip = pitch-2.3, pitch+2.2
    points = [polar(r, (k+f)*math.tau/teeth) for k in range(teeth)
              for f, r in [(0, root), (.17, root), (.31, tip), (.65, tip), (.81, root)]]
    outline = 'M' + ' '.join(points) + 'Z'
    for i in range(spokes):
        a, b = (i+.11)*math.tau/spokes, (i+.88)*math.tau/spokes
        r, h = pitch-8, 9
        outline += f'M{polar(r,a)}A{r} {r} 0 0 1 {polar(r,b)}L{polar(h,b)}A{h} {h} 0 0 0 {polar(h,a)}Z'
    return f'''<g transform="rotate({angle})">{m.turn(angle, angle+direction*360, seconds)}
    <path d="{outline}" fill="{color}" fill-rule="evenodd" stroke="{dark}" stroke-width="1.15" stroke-linejoin="round"/>
    <circle r="{pitch-4}" fill="none" stroke="{dark}" stroke-width=".8"/><circle cx="{pitch-5.4}" r="2.1" fill="#bb6147"/>
  </g><circle r="6.4" fill="{dark}" stroke="{color}" stroke-width="1.3"/><circle r="2" fill="#eddabd"/>'''


def coordination(m):
    return f'''<g fill="none" stroke="#a7ba9f" opacity=".7" stroke-width=".9">
  <path d="M12 74h52l26-18h39m64 0h40l19-15h54M16 78h49l26-18m142-1 20-15h47"/>
  <circle cx="129" cy="60" r="46" stroke-dasharray="2 5"/><circle cx="197" cy="60" r="34" stroke-dasharray="2 5"/>
  <path d="M43 24v9m-4-4h9m219 52v9m-4-5h9"/>
</g>
<g fill="#c48164" stroke="#e3cbb0"><circle cx="50" cy="74" r="3.2"/><circle cx="272" cy="41" r="3.2"/></g>
<g transform="translate(129 60)">{gear(20, 40, 5, '#e1ad79', '#3d4647', 0, 18, 1, m)}</g>
<g transform="translate(197 60)">{gear(14, 28, 4, '#a1c6b4', '#32484c', 13, 12.6, -1, m)}</g>'''


def film(m):
    # Four exposures of the same paper swallow, with different wing folds.
    poses = [(24, 3, 39, 13), (19, 13, 42, 9), (21, 35, 46, 24), (24, 24, 41, 15)]
    frames = []
    for i, (lx, ly, rx, ry) in enumerate(poses):
        frames.append(f'''<g transform="translate({i*66} 0)">
        <path d="M0 0h61v48H0z" fill="#486b73"/><circle cx="47" cy="12" r="6" fill="#d99b70"/>
        <path d="M0 39q17-8 29-5t32-6v20H0Z" fill="#31545e"/>
        <path d="M6 39 27 21 49 17 40 24 26 29Z" fill="#f5dfb7"/>
        <path d="M25 26 {rx} {ry} 39 24Z" fill="#cca47a"/><path d="M26 27 {lx} {ly} 36 23Z" fill="#f3cd98" stroke="#334e55" stroke-width=".65"/>
        <path d="m9 38 17-13 7-1-7 6Z" fill="#b7c6b0"/></g>''')
    shift = m.tween('translate', ['0 0','0 0','-66 0','-66 0','-132 0','-132 0','-198 0','-198 0','-264 0'], 7.2,
                    transform=True, times=[0,.17,.25,.42,.50,.67,.75,.92,1], eased=True)
    return f'''<defs><g id="four-frames">{''.join(frames)}</g>
    <pattern id="sprockets" width="11" height="6" patternUnits="userSpaceOnUse"><rect x="2" y="1" width="5" height="4" rx="1" fill="#ddcaa9"/></pattern></defs>
<path d="M16 11h96m92 98h100" stroke="#936d5d" stroke-width=".8"/>
<g transform="rotate(-5 160 60)"><g transform="translate(0 0)">{shift}
  <path d="M-265 22h925v77h-925z" fill="#866b5f"/><path d="M-265 19h925v77h-925z" fill="#283f46"/>
  <path d="M-265 23h925v6h-925zm0 60h925v6h-925z" fill="url(#sprockets)"/>
  <use href="#four-frames" x="-233" y="33"/><use href="#four-frames" x="31" y="33"/>
  <use href="#four-frames" x="295" y="33"/><use href="#four-frames" x="559" y="33"/>
</g></g>
<g fill="none" stroke="#fff1d2" stroke-width="2"><path d="M121 39v-8h9m58 0h9v8m0 38v8h-9m-58 0h-9v-8"/></g>
<path d="m155 14 5 6 5-6Zm0 90 5-6 5 6Z" fill="#614d47"/>'''


def manipulator(m):
    # Wrist, jaw opening and cargo centre at the timed stops. Recompute the
    # elbow by two-link inverse kinematics between stops instead of scaling rods.
    stops = [
        (0,    137,74,11,137,91), (.07,137,74,7,137,91), (.18,142,43,7,142,60),
        (.36,  206,43,7,206,60), (.45,213,74,7,213,91), (.50,213,74,11,213,91),
        (.56,  210,61,11,213,91), (.62,213,74,11,213,91), (.66,213,74,7,213,91),
        (.75,  206,43,7,206,60), (.88,142,43,7,142,60), (.96,137,74,7,137,91),
        (1,    137,74,11,137,91)]
    times, states = [], []
    for a, b in zip(stops, stops[1:]):
        for step in range(4):
            u = step/4
            times.append(a[0] + (b[0]-a[0])*u)
            t = u*u*(3-2*u)
            states.append([v + (w-v)*t for v,w in zip(a[1:],b[1:])])
    times.append(1); states.append(stops[-1][1:])
    shoulder = (68,99)
    elbows, wrists, boxes, jaws = [], [], [], []
    for x, y, half, bx, by in states:
        dx, dy = x-shoulder[0], y-shoulder[1]
        a = math.atan2(dy, dx) - math.acos(math.hypot(dx,dy)/(2*78))
        elbows.append(xy(shoulder[0]+78*math.cos(a), shoulder[1]+78*math.sin(a)))
        wrists.append(xy(x,y)); boxes.append(xy(bx,by))
        jaws.append(f'M{-half:g} 3v14l3 2M{half:g} 3v14l-3 2')

    def d_path(name, poses):
        return f'<path id="{name}" d="{poses[0]}">{m.tween("d",poses,9.6,times=times)}</path>'

    def location(poses, contents):
        return f'<g transform="translate({poses[0]})">{m.tween("translate",poses,9.6,transform=True,times=times)}{contents}</g>'

    upper = ['M68 99L'+e for e in elbows]; lower = ['M'+e+'L'+w for e,w in zip(elbows,wrists)]
    linkage = ''.join(f'<use href="#{rod}" stroke="{color}" stroke-width="{w}"/>'
                      for rod in ['upper','lower'] for color,w in [('#2e514e',14),('#dfb986',10),('#f2d6a6',2)])
    pivot = '<circle r="7.3" fill="#42605a" stroke="#edd2a7" stroke-width="1.9"/><circle r="3" fill="#d08361"/>'
    crate = '<path d="m-7-5 7-4 7 4v12l-7 3-7-4z" fill="#d1764d" stroke="#594c3f"/><path d="m-7-5 7 3 7-3-7-4z" fill="#f0c490"/><path d="M0-1v10" stroke="#a3573e"/>'
    grip = '<path d="M-10-1H10v5h-20z" fill="#36544e"/><use href="#jaw" stroke="#324f49" stroke-width="3" fill="none"/><circle r="4.4" fill="#c97955" stroke="#e4cfad"/>'
    return f'''<defs>{d_path('upper',upper)}{d_path('lower',lower)}{d_path('jaw',jaws)}</defs>
<g fill="none" stroke="#637e72" stroke-width=".8"><path d="M19 102h279m-265 5h253M24 48h16m-8-8v16m223-28h18m-9-9v18"/><path d="M68 21a78 78 0 0 1 78 78m77 0a155 155 0 0 0-24-84" stroke-dasharray="2 4"/></g>
<path d="m41 103 4-9h45l4 9zm81-2h31v4h-31zm75 0h32v4h-32z" fill="#426158"/>
{location(boxes,crate)}<g fill="none" stroke-linecap="round">{linkage}</g>
<g transform="translate(68 99)">{pivot}</g>{location(elbows,pivot)}{location(wrists,grip)}'''


def terrain(m):
    rows = sample(json.loads((ROOT / 'exhibits/qaoa-case-0.json').read_text(encoding='utf-8')))
    end = len(rows)-1
    grid = list(range(0, end+1, 2))
    peak = max(map(max,rows))
    angles = [math.radians(x) for x in (29, 56, 29)]

    def point(x, y, p, a):
        u, v = x/end-.5, y/end-.5
        return xy(160 + 160*(u*math.cos(a)-v*math.sin(a)),
                  78 + 43*(u*math.sin(a)+v*math.cos(a)) - 57*p/peak)

    def surface(path_at, style):
        poses = [path_at(a) for a in angles]
        return f'<path {style} d="{poses[0]}">{m.tween("d",poses,7.8,eased=True)}</path>'

    edge = [(x,end) for x in grid] + [(end,y) for y in grid[-2::-1]]
    def wall(a):
        return ('M'+' '.join(point(x,y,rows[y][x],a) for x,y in edge)+'L'+
                ' '.join(point(x,y,-.05*peak,a) for x,y in reversed(edge))+'Z')

    mesh = [surface(wall, 'fill="#799b98" stroke="#243c48" stroke-width="1"')]
    for y0, y1 in zip(grid,grid[1:]):
        def ribbon(a):
            back = [point(x,y0,rows[y0][x],a) for x in grid]
            face = [point(x,y1,rows[y1][x],a) for x in reversed(grid)]
            return 'M'+' '.join(back+face)+'Z'

        def lines(a):
            front = 'M'+' '.join(point(x,y1,rows[y1][x],a) for x in grid)
            return front + ''.join('M'+point(x,y0,rows[y0][x],a)+'L'+point(x,y1,rows[y1][x],a) for x in grid[::2])

        mesh.append(surface(ribbon,'fill="#305362" stroke="#345564" stroke-width=".55"'))
        mesh.append(surface(lines,'fill="none" stroke="#e5c79b" stroke-width=".95"'))
    return f'''<g fill="none" stroke="#8bada6" stroke-width=".8" opacity=".65"><path d="M20 88q-1 20 61 19m158-83q46 2 61 19" stroke-dasharray="2 4"/>
<path d="M21 65h11m-6-5v10m262-3h11m-5.5-5v10"/></g>
{''.join(mesh)}<circle cx="160" cy="21" r="2.8" fill="#ff986d" stroke="#304856"/>'''


def distillation(m):
    # An exploded axonometric assembly: each set of nine tiles first separates
    # in Z, then fans out horizontally. Foreground voxels paint last.
    palettes = [('#9abbb0','#597b7b','#395b67'),('#f1dcb7','#c09482','#8e777e'),('#e4a57f','#b7766b','#875a6b')]
    dies = []
    for k,(top,left,right) in enumerate(palettes):
        dies.append(f'''<g id="die-{k}" stroke="#514855" stroke-width=".85" stroke-linejoin="round">
        <path d="m-16 0 16-7 16 7-16 7Z" fill="{top}"/><path d="m-16 0 16 7v13l-16-7Z" fill="{left}"/>
        <path d="m0 7 16-7v13l-16 7Z" fill="{right}"/><path d="m5 8 6-2.6m-6 6 6-2.6" stroke="{top}" opacity=".45"/></g>''')
    lattice = sorted(((i,j,k) for i in range(3) for j in range(3) for k in range(3)),key=lambda v:(sum(v), v[2], v[1]))
    cells = []
    for i,j,k in lattice:
        def pos(gap, lift, shear):
            return xy(160 + (i-j)*16*gap + (k-1)*shear, 51 + (i+j-2)*7*gap - (k-1)*13*lift)
        poses = [pos(*phase) for phase in [(1.06,1.18,2),(1.06,1.18,2),(1.06,1.9,12),(1.52,1.9,16),(1.52,1.9,16),(1.06,1.18,2)]]
        anim = m.tween('translate', poses, 7.4, transform=True, times=[0,.12,.35,.55,.7,1], eased=True)
        cells.append(f'<g transform="translate({poses[0]})">{anim}<use href="#die-{k}"/></g>')
    return f'''<defs>{''.join(dies)}</defs>
<g fill="none" stroke="#947a80" stroke-width=".8"><path d="m42 91 116 19 118-27M48 96l107 19 115-25" stroke-dasharray="2 4"/>
<path d="m40 42 27-11 26 11-26 11Zm27 11v12m-27-23v12l27 11 26-11V42m166 39 14-6 15 6-15 6Z" opacity=".7"/></g>
{''.join(cells)}'''


def orbit(m):
    # Back and front impressions share the very same animated carrier. Only
    # the near half of the orbit overprints the planet, so the craft is occulted.
    coords = [xy(110*math.cos(a), 22*math.sin(a)) for a in
              (math.tau*(i/40+.07) for i in range(41))]
    track = m.tween('translate',coords,10.8,transform=True)
    stars = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in
                    [(27,29,1),(64,92,1),(93,16,1.1),(212,13,.7),(278,96,1.1),(294,39,.8),(217,105,.8)])
    return f'''<defs>
  <pattern id="cells" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#446e79"/><path d="M0 5V0h5" stroke="#c3ccb4" stroke-width=".65" fill="none"/></pattern>
  <g id="flight" transform="translate({coords[0]})">{track}<g transform="rotate(-9)" stroke="#1c3743" stroke-width=".9">
    <path d="M-21-1h42v2h-42z" fill="#e4b482"/><path d="M-26-6h15v13h-15zm37 0h15v13H11z" fill="url(#cells)" stroke="#c4c9b4"/>
    <path d="m-7-6 4-4h7l4 4v12l-4 3h-7l-4-3z" fill="#e3c4a1"/><path d="M-3-9V8m6-17V8" stroke="#b76e52" stroke-width="2.3"/>
    <path d="M0-9v-5m-4-2q3 5 7 0Z" fill="#f0d5a5" stroke="#d3bd9a"/></g></g>
  <clipPath id="near"><path d="M-150 0h300v90h-300z"/></clipPath><clipPath id="planet"><circle r="36"/></clipPath>
</defs>
<g fill="#ece4c9">{stars}<path d="m55 32 1.2 4 4 1.2-4 1.2-1.2 4-1.2-4-4-1.2 4-1.2Z"/></g>
<g transform="translate(160 61) rotate(-14)">
  <ellipse rx="116" ry="26" fill="none" stroke="#739797" stroke-width=".75" stroke-dasharray="1 5"/>
  <ellipse rx="110" ry="22" fill="none" stroke="#b1c4ad" stroke-width="1"/><use href="#flight"/>
  <circle r="37.2" fill="#142e40"/><circle r="36" fill="#edb47e"/>
  <g clip-path="url(#planet)"><path d="M-5-38q-26 19-14 45 10 25 42 25L7 45l-50-11-5-53Z" fill="#bd876b"/>
    <g fill="none" stroke="#a17663" stroke-width=".95"><path d="M-39 6q32-17 77-12M-34 13q34-16 74-13M-36 18q42-17 78-13m-62 18q20-11 48-11"/>
    <ellipse cx="11" cy="-15" rx="6" ry="3"/><path d="M0-21q7-6 14-5m-1 44q7-4 13-3"/></g>
  </g>
  <path d="M110 0a110 22 0 0 1-220 0" fill="none" stroke="#f3d5a3" stroke-width="1.6"/>
  <g clip-path="url(#near)"><use href="#flight"/></g>
</g>'''


def contact_sheet(m):
    """A radio dish and seven downlink tracks on the same clock."""
    # First 12 ticks of P01_intro, rows S01/S02/S03/S04/S12/S13/S16.
    slots = (4, 3, 2, 0, 10, 9, 5)
    start, pitch = 153, 11
    rows = []
    for i, slot in enumerate(slots):
        y = 29 + 9 * i
        rows.append(f'<path d="M{start} {y}h132" stroke="#6f938b" stroke-width=".75"/>'
                    f'<use href="#window" x="{start + pitch * slot + 1}" y="{y - 2.7}"/>')
    ticks = ''.join(f'M{start + i * pitch} 23v65' for i in range(13))
    stops = [0, .38, .77, 1]
    cursor = [f'{start + pitch * i} 0' for i in (4.5, 11.5, .5, 4.5)]
    scan = m.tween('translate', cursor, 9.6, transform=True, times=stops, eased=True)
    tilt = m.tween('rotate', [14, 36, -16, 14], 9.6, transform=True, times=stops, eased=True)
    return f'''<defs>
  <g id="window"><rect width="9" height="5.4" rx=".8" fill="#e8b77d"/><path d="M2 1.4h4.8" stroke="#fff0be" stroke-width=".7"/></g>
</defs>
<g fill="none" stroke="#6c7b72" stroke-width=".9"><path d="M-9 72Q44 2 126 11m-132 69q71-83 141-63" stroke-dasharray="2 4"/>
  <path d="M-6 96q23-16 47-9t47 0 49 4m-142 14q44-16 87-4t59-2"/></g>
<path d="M25 104h87m-81 3h74" fill="none" stroke="#726d5b"/>
<g transform="translate(71 67)" stroke="#324d50" stroke-linejoin="round">
  <path d="m-24 35 18-34h10l21 34h-7L0 9l-17 26Z" fill="#65817a" stroke-width="1.8"/>
  <path d="m-18 32 29-13m-24 4 29 9m-42 2h53v4h-53z" fill="#ae8d69"/>
  <g transform="rotate(14)">{tilt}
    <path d="M-32-14Q-13 23 9 13q14-5 23-27Z" fill="#628d87" stroke-width="1.7"/>
    <path d="M-32-14Q0-25 32-14Q3 17-32-14Z" fill="#ebd8ae" stroke-width="1.5"/>
    <g fill="none" stroke="#8b947f" stroke-width=".8"><path d="M-26-14q26 19 50 1m-43-3q18 12 37 1m-27-2q10 5 21 0M-14-17l7 13m6-14 2 15m12-15-5 13"/></g>
    <path d="m-29-14 29-19 29 19M0-31v28" fill="none" stroke-width="1.5"/>
    <ellipse cy="-33" rx="3.6" ry="2.3" fill="#cc845e"/>
    <path d="M-7-40q7-5 14 0m-18-5q11-7 22 0" fill="none" stroke="#567a77" stroke-width="1.35"/>
  </g><circle r="4.1" fill="#d7956c"/><circle r="1.4" fill="#e9d4a6"/>
</g>
<path d="M142 14h145l7 7v71l-6 6H143l-7-7V21Z" fill="#24434a" stroke="#645f50" stroke-width="1.8"/>
<path d="M145 18h140l5 5v67l-4 4H145l-5-5V23Z" fill="none" stroke="#b4b89a" stroke-width=".8"/>
<path d="{ticks}" fill="none" stroke="#71918d" stroke-width=".65" stroke-dasharray="1.2 2.7"/>
{''.join(rows)}
<g transform="translate({cursor[0]})">{scan}<path d="M-3 22h6v67h-6Z" fill="#f4d59d" opacity=".16"/>
  <path d="M0 22v67" stroke="#f6dbb1" stroke-width="1.15"/><path d="m-3 19 3 5 3-5zm0 73 3-5 3 5z" fill="#db9570"/></g>'''


def swatch_print(rows, colors):
    """Print runs of equal ink as horizontal cuts rather than hundreds of rects."""
    cuts = [[] for _ in colors]
    for y, row in enumerate(rows):
        x = 0
        for color, run in groupby(row):
            n = sum(1 for _ in run)
            if color != '0':
                cuts[int(color)].append(f'M{x} {y}h{n}v1h-{n}z')
            x += n
    base = f'<rect width="{len(rows[0])}" height="{len(rows)}" fill="{colors[0]}"/>'
    return base + ''.join(f'<path d="{"".join(paths)}" fill="{ink}"/>'
                          for ink, paths in zip(colors, cuts) if paths)


def burn_atlas(m):
    """Two leaves of one atlas: spectral print and registered severity overlay."""
    chip = json.loads((ROOT / 'exhibits/omlp-chip-95.json').read_text(encoding='utf-8'))
    tones = swatch_print(chip['dnbr_tones'], ('#294b50', '#47706b', '#769381', '#aab997', '#e6d5a6'))
    burn = swatch_print(chip['severity'], ('#354b47', '#c4b276', '#dca273', '#af644f'))
    widths = [17, 27, 2, 17]
    travel = m.tween('width', widths, 8.4, eased=True)
    positions = [f'{w} 0' for w in widths]
    slide = m.tween('translate', positions, 8.4, transform=True, eased=True)
    return f'''<defs>
  <g id="tones" shape-rendering="crispEdges">{tones}</g><g id="severity" shape-rendering="crispEdges">{burn}</g>
  <clipPath id="shutter"><rect width="17" height="28">{travel}</rect></clipPath>
  <g id="leaf"><rect width="100" height="100" fill="#e5d5ad" stroke="#6f6b55"/>
    <path d="M4 15V4h11m70 0h11v11m0 70v11H85m-70 0H4V85" fill="none" stroke="#ad9072"/>
    <use href="#tones" transform="translate(8 8) scale(3)"/>
    <path d="M7.5 7.5h85v85h-85Z" fill="none" stroke="#526e64" stroke-width=".75"/></g>
  <g id="reader" transform="translate(17 0)">{slide}<path d="M0 0v28" stroke="#f4e2c4" stroke-width=".34"/>
    <path d="m-1-1.2 1 1.8 1-1.8Zm0 30.4 1-1.8 1 1.8Z" fill="#bd7453" stroke="#614f42" stroke-width=".16"/></g>
</defs>
<g fill="none" stroke="#a8b298" stroke-width=".7" opacity=".65"><path d="M-9 94Q36 96 34 65T54 4m-63 83q39 2 37-28t24-59m-61 80q31 0 31-29T42 0M270 126q32-25 21-60t36-51m-64 111q32-28 22-60t40-58"/>
  <path d="M16 23h12m-6-6v12m267 63h12m-6-6v12"/></g>
<path d="m43 16 8-3 109 13 111-13 6 3v83l-117 14L43 100Z" fill="#203f3c" stroke="#c0b394" stroke-width="1.35"/>
<path d="m47 95 113 13 113-13m-223 4 110 12 111-13" fill="none" stroke="#b19e7e" stroke-width=".9"/>
<g transform="matrix(1.12 .12 0 .8 48 12)"><use href="#leaf"/>
  <g transform="translate(8 8) scale(3)"><use href="#reader"/></g></g>
<g transform="matrix(1.12 -.12 0 .8 160 24)"><use href="#leaf"/>
  <g transform="translate(8 8) scale(3)"><g clip-path="url(#shutter)"><use href="#severity"/></g><use href="#reader"/></g></g>
<path d="M157 24v80m6-80v80" stroke="#72684f" stroke-width=".85" opacity=".7"/>'''


@dataclass(frozen=True)
class Stamp:
    number: str
    slug: str
    name: str
    colors: tuple[str, str]
    desc: str
    scene: Callable[[Exposure], str]
    font_size: int = 23

    def filename(self, moving):
        return f'{self.number}-{self.slug}{"" if moving else "-still"}.svg'


STAMPS = (
    Stamp('03','guardian','Guardian-of-Truth',('#29313e','#59495a'), 'Глаз с подвижной механической диафрагмой.',guardian),
    Stamp('04','referee','Coordination-Referee',('#30545b','#203944'), 'Два зубчатых колеса в зацеплении.',coordination,21),
    Stamp('05','film','Vision-Action-Data-Factory',('#edcfab','#d7a387'), 'Лента с фазами полёта бумажной птицы.',film,18),
    Stamp('06','arm','Green-Challenge',('#c4d4bf','#89a99c'), 'Шарнирная рука переносит медный кубик.',manipulator),
    Stamp('07','relief','QAOA',('#273e53','#173943'), 'Поворотная гравюра рельефа вероятности.',terrain),
    Stamp('08','voxels','3D-DIT-Distillation',('#e1cebd','#b89ca9'), 'Три слоя объёмного куба расходятся и собираются.',distillation,22),
    Stamp('09','orbit','CosmoH',('#1e2f44','#31545f'), 'Спутник проходит за планетой и возвращается на свет.',orbit),
    Stamp('10', 'contact', 'AUSG', ('#ded1ae', '#b09c7d'), 'Антенна поворачивается, пока указатель проходит окна связи.', contact_sheet),
    Stamp('11', 'atlas', 'OMLP', ('#3d5951', '#68775e'), 'В атласе гари шторка совмещает спектральный отпечаток с картой степеней повреждения.', burn_atlas),
)


def render(stamp, moving):
    # Everything in the image area can move; stock, serial, caption and the
    # link arrow stay registered. A no-SMIL viewer still gets this exact pose.
    scene = stamp.scene(Exposure(moving))
    c0,c1 = stamp.colors
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="352" height="180" viewBox="0 0 352 180" role="img" aria-labelledby="title desc">
<title id="title">{stamp.number} · {escape(stamp.name)}</title><desc id="desc">{stamp.desc}</desc>
<!-- Printed by tools/print_hackathons.py; all artwork is local. -->
<defs>
  <linearGradient id="ink" x2="1" y2="1"><stop stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>
  <pattern id="fleck" width="19" height="13" patternUnits="userSpaceOnUse"><path d="M2 5h1m7 5h.7m6-8h.8" stroke="#e8d5ad" stroke-width=".7" opacity=".39"/><circle cx="5" cy="11" r=".5" fill="#182e3b" opacity=".4"/></pattern>
  <clipPath id="gate"><path d="M0 0h320v120H0z"/></clipPath>
</defs>
<path d="M6 1h340q5 0 5 5v126a5 5 0 0 0 0 10v32q0 5-5 5H6q-5 0-5-5v-32a5 5 0 0 0 0-10V6q0-5 5-5Z" fill="#f3e9d2" stroke="#bbae94" stroke-width="1.3"/>
<rect x="12.5" y="8.5" width="327" height="127" fill="none" stroke="#9c9c85" stroke-width=".8"/>
<g transform="translate(16 12)"><g clip-path="url(#gate)"><path fill="url(#ink)" d="M0 0h320v120H0z"/>
{scene}
<path d="M0 0h320v120H0z" fill="url(#fleck)"/>
<path d="M5 14V5h9m292 0h9v9m0 92v9h-9m-292 0H5v-9" stroke="#d9c9a6" stroke-width=".8" opacity=".72" fill="none"/>
</g></g>
<path d="M15 142h322" stroke="#bcae91" stroke-width=".8" stroke-dasharray="2 3"/>
<text x="17" y="165" font-family="{MONO}" font-size="14" letter-spacing=".8" fill="#93533f">{stamp.number}</text>
<path d="M43 150v19" stroke="#b9af95"/>
<text x="54" y="166" font-family="{SANS}" font-weight="600" font-size="{stamp.font_size}" letter-spacing="-.6" fill="#1c4044">{escape(stamp.name)}</text>
<path d="m322 164 9-10m-8 0h8v8" fill="none" stroke="#776b55" stroke-width="1.4"/>
</svg>\n'''


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for stamp in STAMPS:
        for moving in (False, True):
            (OUT / stamp.filename(moving)).write_bytes(render(stamp, moving).encode('utf-8'))
