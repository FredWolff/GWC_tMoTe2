"""Each figure builds from ``data/`` alone and plots what the original code plotted.

Run from the ``share`` folder with ``python -m unittest discover tests`` (or pytest).
"""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

SHARE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SHARE))
sys.path.insert(0, str(SHARE / 'tests'))

from summarize import compare, summarize_figure  # noqa: E402

FIGURES = ['fig1', 'fig2', 'fig3', 's1', 's2', 's3', 's4', 's5', 's6']


class FigureTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def check(self, name):
        module = importlib.import_module(f'figures.{name}')
        figures = module.build()

        with self.subTest('plots what the original code plotted'):
            golden = json.loads((SHARE / 'tests' / 'golden' / f'{name}.json').read_text())
            self.assertEqual(set(golden), set(figures))
            for stem, fig in figures.items():
                self.assertEqual(compare(golden[stem], summarize_figure(fig), where=stem), [])

        with self.subTest('saves a non-empty PDF per figure'):
            with tempfile.TemporaryDirectory() as tmp:
                module.save(figures, tmp)
                for stem in figures:
                    self.assertGreater((Path(tmp) / f'{stem}.pdf').stat().st_size, 1000)

        with self.subTest('needs no original code'):
            for module_name in ('functions', 'qcodes'):
                self.assertNotIn(module_name, sys.modules)


def _add(name):
    setattr(FigureTests, f'test_{name}', lambda self: self.check(name))


for _name in FIGURES:
    _add(_name)


class DataTests(unittest.TestCase):
    def test_no_pickles_in_data(self):
        suffixes = {p.suffix for p in (SHARE / 'data').iterdir()}
        self.assertTrue(suffixes <= {'.npz', '.json', '.md'}, suffixes)


if __name__ == '__main__':
    unittest.main()
