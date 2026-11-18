"""Typeset two self-contained layouts, with and without the moving light. Inputs: art/lighthouse.svg and this file."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK = '#173c42'
VERMILION = '#b94932'
COLLECTION = 'КОЛЛЕКЦИЯ 01—11'
MONO = "'SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"
SERIF = "Georgia,'DejaVu Serif','Times New Roman',serif"
SANS = "'Segoe UI',Arial,'DejaVu Sans',sans-serif"


def cut_edge(width, height, pitch=16, radius=3.5):
    """Clockwise paper outline. Counterclockwise half circles are the perforations."""
    d = ['M0 0']
    for side, length, direction in [('h', width, 1), ('v', height, 1),
                                    ('h', width, -1), ('v', height, -1)]:
        n = round(length / pitch)
        shoulder = (length / n / 2 - radius) * direction
        dx = 2 * radius * direction if side == 'h' else 0
        dy = 2 * radius * direction if side == 'v' else 0
        d.extend([f'{side}{shoulder:.3f}a{radius} {radius} 0 0 0 {dx} {dy}{side}{shoulder:.3f}'] * n)
    return ''.join(d) + 'Z'


def imprint():
    landscape = (ROOT / 'art/lighthouse.svg').read_text(encoding='utf-8').strip()
    return f'''
      <path id="paper-edge" d="{cut_edge(310, 320)}"/>
      <g id="stamp">
        <use href="#paper-edge" fill="#fff5da" stroke="#bfb29a" stroke-width=".9"/>
        <rect x="12" y="12" width="286" height="296" fill="none" stroke="#817f6c" stroke-width=".7"/>
        <g transform="translate(16 16) scale(.926667)">{landscape}</g>
        <path d="M16 248.5h278v55H16z" fill="#e7debf"/>
        <path d="M16 248.5h278M26 296h258" stroke="#647369" stroke-width=".8"/>
        <text x="27" y="284" font-family="{SERIF}" font-size="32" font-style="italic" fill="{INK}">Маяк</text>
        <text x="269" y="271" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.4" fill="{INK}">MYWORKAIBRAIN</text>
        <text x="269" y="287" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="#8a4636">МАРКА № 01</text>
      </g>'''


def postmark():
    return f'''
      <g id="postmark" fill="none" stroke="#345d5c">
        <circle r="52" stroke-width="1.7" stroke-dasharray="206 2 63 1 53 2"/>
        <circle r="46.8" stroke-width=".85"/><circle r="32" stroke-width=".8" stroke-dasharray="85 5 106 5"/>
        <path id="type-arc" d="M-38 1a38 38 0 0 1 76 0" stroke="none"/>
        <text fill="#345d5c" stroke="none" text-anchor="middle" font-family="{MONO}" font-size="8.3" letter-spacing="1.5"><textPath href="#type-arc" startOffset="50%">ОТКРЫТЫЙ КОД</textPath></text>
        <path d="M-22-14h44m-42 30h40" stroke-width="1"/>
        <text y="9" text-anchor="middle" font-family="{SERIF}" font-size="24" font-style="italic" fill="#345d5c" stroke="none">ob.</text>
        <text y="42" text-anchor="middle" font-family="{MONO}" font-size="8.5" letter-spacing="1.8" fill="#345d5c" stroke="none">№ 001</text>
        <g stroke-width="1.45" stroke-linecap="round">
          <path d="M52-16c18 2 23 11 42 7s30-12 46-8m-88 9c18 2 24 11 42 7s30-12 46-8m-87 9c18 2 23 11 41 7s30-12 46-8m-88 9c18 2 24 11 42 7s30-12 46-8"/>
        </g>
      </g>'''


def heading(mark_x, mark_y, scale=1):
    return f'''<g transform="translate({mark_x} {mark_y}) scale({scale})">
      <path d="M0 0h31v29H0z" fill="{VERMILION}"/>
      <g stroke="#fff4db" fill="none" stroke-linecap="round" stroke-width="1.65">
        <path d="M5 19q5-3 10 0t11 0M5 23q5-3 10 0t11 0"/>
        <path d="m8 15 8-10v10zm10-8 6 8h-6z" fill="#fff4db" stroke="none"/>
      </g>
      <text x="45" y="21" fill="{INK}" font-family="{SANS}" font-size="21" font-weight="700" letter-spacing="-.6">overbaffe1</text>
      <path d="m184 5-6 20" stroke="#9b977f"/>
      <text x="199" y="20" fill="{INK}" font-family="{MONO}" font-size="14" letter-spacing="2">ПОРТФОЛИО</text>
    </g>'''


def postcard(compact, motion):
    # Select motion in the surrounding <picture>, not only inside the SVG. Some
    # image renderers do not pass the reader's media preferences to subdocuments.
    beam_style = """<style>
    @media (prefers-reduced-motion: no-preference) {
      .beam { transform-origin: 145px 72px; animation: lantern 4.6s ease-in-out 1; }
      @keyframes lantern { 0%, 100% { transform: rotate(0deg) } 46% { transform: rotate(-7deg) } }
    }
  </style>""" if motion else ''
    width, height = (480, 466) if compact else (1120, 418)
    if compact:
        content = f'''
        {heading(25, 24, .95)}
        <text x="24" y="101" font-family="{SERIF}" font-size="35" letter-spacing="-1.6" fill="{INK}">Альбом открытого кода.</text>
        <path d="M26 119h428" stroke="#bcb7a0"/>
        <text transform="translate(38 355) rotate(-90)" font-family="{MONO}" font-size="13" letter-spacing="2" fill="#48635f">{COLLECTION}</text>
        <g transform="translate(168 142) rotate(5 145 142) scale(.827)"><use href="#paper-edge" x="2.8" y="3" fill="#a9997f" opacity=".4"/><use href="#stamp"/></g>
        <use href="#postmark" transform="translate(112 317) rotate(-12) scale(.86)" opacity=".79"/>
        <path d="M26 426h428" stroke="#bcb7a0"/>
        <text x="26" y="449" font-family="{MONO}" font-size="13" letter-spacing="1.2" fill="{VERMILION}">МАРКА 01</text>
        <text x="450" y="449" text-anchor="end" font-family="{SANS}" font-size="16" fill="{INK}">Открыть маяк в 3D ↗</text>'''
    else:
        content = f'''
        {heading(53, 37)}
        <text x="49" y="168" font-family="{SERIF}" font-size="97" letter-spacing="-5" fill="{INK}">Альбом</text>
        <text x="50" y="248" font-family="{SERIF}" font-style="italic" font-size="81" letter-spacing="-4.4" fill="{INK}">открытого кода<tspan fill="{VERMILION}">.</tspan></text>
        <path d="M54 290h32" stroke="{VERMILION}" stroke-width="2.2"/>
        <text x="100" y="297" font-family="{SANS}" font-size="21" fill="#415a55">Маяк, кристалл и девять марок с хакатонов.</text>
        <path d="M54 345h600" stroke="#a8a793" stroke-width="1"/>
        <g font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="#3c5955">
          <text x="54" y="376">{COLLECTION}</text>
          <text x="654" y="376" text-anchor="end">ОТКРЫТЬ МАЯК В 3D ↗</text>
        </g>
        <g transform="translate(736 38) rotate(6 155 160) scale(1.04)"><use href="#paper-edge" x="3" y="4" fill="#998972" opacity=".3"/><use href="#stamp"/></g>
        <use href="#postmark" transform="translate(721 279) rotate(-13)" opacity=".78"/>
        <text x="1094" y="381" transform="rotate(-90 1094 381)" font-family="{MONO}" font-size="10.5" letter-spacing="1.9" fill="#526560">ЭКЗЕМПЛЯР № 01</text>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">overbaffe1 · Портфолио — Альбом открытого кода</title>
  <desc id="desc">Почтовая карточка на кремовой бумаге. На марке полосатый маяк освещает море; за ним медный диск солнца.</desc>
  <!-- Generated by tools/print_album.py. The original engraving is art/lighthouse.svg. -->
{beam_style}
  <defs>
    <linearGradient id="stock" x2="1" y2="1"><stop stop-color="#f6eedc"/><stop offset=".7" stop-color="#f1e8d5"/><stop offset="1" stop-color="#e8ddc5"/></linearGradient>
    <pattern id="grain" width="29" height="23" patternUnits="userSpaceOnUse">
      <path d="M2 3h1m10 4h.7m9 9h1M7 18h1m17-16h1m-12 18h1.2" stroke="#807f6c" stroke-width=".8" opacity=".21"/>
      <path d="M8 9h1.1m10 3h.8m6 7h1.4" stroke="white" opacity=".65"/>
    </pattern>
    <pattern id="airmail" width="57" height="8" patternUnits="userSpaceOnUse"><path d="m0 8 8-8h15l-8 8Z" fill="#c45e46"/><path d="m28 8 8-8h15l-8 8Z" fill="#45666a"/></pattern>
{imprint()}
{postmark()}
  </defs>
  <path d="M0 0h{width}v{height}H0z" fill="url(#stock)"/>
  <path d="M0 0h{width}v{height}H0z" fill="url(#grain)"/>
  <path d="M0 0h{width}v5H0z" fill="url(#airmail)"/>
  <rect x=".5" y=".5" width="{width-1}" height="{height-1}" fill="none" stroke="#a8a18b" stroke-opacity=".65"/>
{content}
</svg>\n'''


if __name__ == '__main__':
    for compact in (False, True):
        for motion in (False, True):
            name = 'postcard' + ('-compact' if compact else '') + ('-beam' if motion else '')
            (ROOT / 'assets' / f'{name}.svg').write_bytes(postcard(compact, motion).encode('utf-8'))
