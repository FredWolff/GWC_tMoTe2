"""Build the figures of the paper and write them to ``output/``.

    python make_figures.py              # all figures
    python make_figures.py fig3 s6      # selected figures
"""
import importlib
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ALL = ['fig1', 'fig2', 'fig3', 's1', 's2', 's3', 's4', 's5', 's6']


def main(names):
    unknown = [name for name in names if name not in ALL]
    if unknown:
        sys.exit(f'unknown figure(s) {unknown}; choose from {ALL}')
    (HERE / 'output').mkdir(exist_ok=True)
    for name in names or ALL:
        module = importlib.import_module(f'figures.{name}')
        figures = module.build()
        module.save(figures)
        for stem in figures:
            print(f'wrote output/{stem}.pdf')
        plt.close('all')


if __name__ == '__main__':
    main(sys.argv[1:])
