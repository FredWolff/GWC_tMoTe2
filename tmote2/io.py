"""Loading of the compressed data files in ``data/``.

Each dataset is stored as ``<name>.npz`` (all arrays) and, when it holds any
non-array content (numbers, strings, lists), ``<name>.json``. Nested
structures are flattened with ``/`` in the ``.npz`` keys and rebuilt here.
"""
import json
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


class Tree(dict):
    """A dict whose entries can also be read as attributes (``d.nn``)."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None


def _insert(tree, path, value):
    *parents, leaf = path.split('/')
    for key in parents:
        tree = tree.setdefault(key, Tree())
    tree[leaf] = value


def _treeify(obj):
    if isinstance(obj, dict):
        return Tree({key: _treeify(value) for key, value in obj.items()})
    return obj


def _listify(obj):
    """Groups whose keys are "0", "1", ... are lists of arrays of different lengths."""
    if isinstance(obj, dict):
        obj = Tree({key: _listify(value) for key, value in obj.items()})
        if obj and set(obj) == {str(i) for i in range(len(obj))}:
            return [obj[str(i)] for i in range(len(obj))]
    return obj


def load(name: str, data_dir: Path = DATA_DIR) -> Tree:
    """Load the dataset ``name`` from the data directory."""
    tree = Tree()
    json_path = Path(data_dir) / f'{name}.json'
    npz_path = Path(data_dir) / f'{name}.npz'
    if json_path.exists():
        with open(json_path) as f:
            tree.update(_treeify(json.load(f)))
    if npz_path.exists():
        with np.load(npz_path) as npz:
            for path in npz.files:
                _insert(tree, path, npz[path])
    if not tree:
        raise FileNotFoundError(f'no data found for {name!r} in {data_dir}')
    return _listify(tree)
