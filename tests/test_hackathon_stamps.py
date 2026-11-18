"""The seven repo links must work as a gallery even when motion is disabled."""

import unittest
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from tools.print_hackathons import OUT, ROOT, STAMPS, render


class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a':
            self.cards.append({'href': a['href']})
        elif tag in ('img', 'source'):
            self.cards[-1].update(a)


def frame(element):
    """XML artwork without the animation instructions; ignore indentation."""
    return (element.tag, element.attrib, (element.text or '').strip(),
            [frame(child) for child in element if not child.tag.split('}')[-1].startswith('animate')])


class StampTests(unittest.TestCase):
    def test_gallery_has_a_static_default_for_each_repo(self):
        markup = (ROOT/'README.md').read_text(encoding='utf-8').split('## Участие в хакатонах\n')[1].split('\n## ')[0]
        gallery = Gallery()
        gallery.feed(markup)
        self.assertEqual(len(gallery.cards), len(STAMPS))
        for stamp, card in zip(STAMPS, gallery.cards):
            with self.subTest(stamp=stamp.name):
                self.assertEqual(card['href'], 'https://github.com/overbaffe1/' + stamp.name)
                self.assertIn(stamp.name, card['alt'])
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
