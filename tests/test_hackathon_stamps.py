"""Check each event's repo links, printed stamps and reduced-motion alternatives."""

import unittest
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from tools.print_hackathons import OUT, ROOT, STAMPS, render


class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.groups = []
        self.in_heading = False
        self.card = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h3':
            self.in_heading = True
            self.groups.append({'title': '', 'links': [], 'dividers': [], 'cards': []})
        elif self.in_heading and tag == 'a':
            self.groups[-1]['links'].append(a['href'])
        elif self.in_heading and tag == 'img':
            self.groups[-1]['dividers'].append(a)
        elif tag == 'a':
            self.card = {'href': a['href']}
            self.groups[-1]['cards'].append(self.card)
        elif self.card is not None and tag in ('img', 'source'):
            self.card.update(a)

    def handle_data(self, data):
        if self.in_heading:
            self.groups[-1]['title'] += data

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_heading = False
        elif tag == 'a':
            self.card = None


def frame(element):
    """XML artwork without the animation instructions; ignore indentation."""
    return (element.tag, element.attrib, (element.text or '').strip(),
            [frame(child) for child in element if not child.tag.split('}')[-1].startswith('animate')])


class StampTests(unittest.TestCase):
    def test_gallery_has_a_static_default_for_each_repo(self):
        markup = (ROOT/'README.md').read_text(encoding='utf-8').split('## Участие в хакатонах\n')[1].split('\n## ')[0]
        gallery = Gallery()
        gallery.feed(markup)
        events = [
            ('AI Journey Contest 2026', 'ai-journey.svg', ['https://dsworks.ru/group/aij2026'],
             ['Guardian-of-Truth', 'Coordination-Referee', 'Vision-Action-Data-Factory',
              'Green-Challenge', '3D-DIT-Distillation']),
            ('КосмоХакатон 2026', 'cosmohack.svg', [], ['CosmoH', 'AUSG', 'OMLP']),
            ('AI Challenge 2026', 'ai-challenge.svg', ['https://aiijc.com/ru/'], ['QAOA']),
        ]
        by_name = {stamp.name: stamp for stamp in STAMPS}
        self.assertCountEqual([name for *_, names in events for name in names], by_name.keys())
        self.assertEqual(len(gallery.groups), len(events))
        for group, (event, divider, links, names) in zip(gallery.groups, events):
            with self.subTest(event=event):
                self.assertEqual(group['title'].strip(), event)
                self.assertEqual(group['links'], links)
                self.assertEqual(len(group['dividers']), 1)
                art = group['dividers'][0]
                self.assertEqual(art['alt'], '')  # the actual heading is text
                path = ROOT / art['src']
                self.assertEqual(path.name, divider)
                self.assertEqual(ET.parse(path).getroot().tag, '{http://www.w3.org/2000/svg}svg')
                self.assertEqual(len(group['cards']), len(names))
            for name, card in zip(names, group['cards']):
                with self.subTest(stamp=name):
                    stamp = by_name[name]
                    self.assertEqual(card['href'], 'https://github.com/overbaffe1/' + name)
                    self.assertEqual(card['alt'], f'{stamp.number} · {name}')
                    self.assertEqual(card['media'], '(prefers-reduced-motion: no-preference)')
                    for attr, moving in [('src', False), ('srcset', True)]:
                        self.assertEqual(ROOT/card[attr], OUT/stamp.filename(moving))

    def test_prints_match_the_generator(self):
        for stamp in STAMPS:
            for moving in (True, False):
                with self.subTest(stamp=stamp.name, moving=moving):
                    self.assertEqual((OUT / stamp.filename(moving)).read_bytes(),
                                     render(stamp, moving).encode('utf-8'))

    def test_stills_are_the_same_print_without_the_motion(self):
        for stamp in STAMPS:
            with self.subTest(stamp=stamp.name):
                film, still = [ET.parse(OUT/stamp.filename(m)).getroot() for m in (True, False)]
                self.assertEqual(frame(film), frame(still))
                self.assertFalse(any(el.tag.split('}')[-1].startswith('animate') for el in still.iter()))
                animations = [el for el in film.iter() if el.tag.split('}')[-1].startswith('animate')]
                self.assertTrue(animations)
                for el in animations:
                    poses = el.attrib['values'].split(';')
                    self.assertGreater(len(set(poses)), 1)
                    if 'keyTimes' in el.attrib:
                        times = list(map(float, el.attrib['keyTimes'].split(';')))
                        self.assertEqual((times[0], times[-1]), (0, 1))
                        self.assertEqual(len(times), len(poses))
                        self.assertEqual(times, sorted(times))


if __name__ == '__main__':
    unittest.main()
