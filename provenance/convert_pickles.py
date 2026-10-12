"""Convert the original analysis pickles into the compressed data files in ``data/``.

The original pickles can only be loaded if the module they were written from
(``functions``, or a notebook's ``__main__``) is importable, and unpickling
executes code. This converter reads them with a *stand-in* unpickler that
never imports the original code: classes become plain containers and
function references become their names. Only the fields listed in
``CONVERSIONS`` (those that the shared figures actually read) are kept.

Usage (needs the original pickles, which are not part of this folder)::

    python convert_pickles.py --working-jar <dir with the main-text pickles> \
                              --repo-jar <dir with the SI pickles>

``--verify`` reloads every written file and checks it equals the pruned source
field by field. See ``data/MANIFEST.md`` for the result of the last run.
"""
import argparse
import json
import pickle
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / 'data'

# Names of classes defined in the original code. Every other global found in
# a pickle is a function reference.
ORIGINAL_CLASSES = {'Data', 'Results'}
ORIGINAL_MODULES = {'functions', '__main__'}


class FunctionRef:
    """Stand-in for a function the original pickle referred to by name."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'FunctionRef({self.name!r})'


class _StandInUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module in ORIGINAL_MODULES:
            if name in ORIGINAL_CLASSES:
                return type(name, (), {})
            return FunctionRef(name)
        return super().find_class(module, name)


def _is_plain_object(obj):
    return hasattr(obj, '__dict__') and not isinstance(obj, (np.ndarray, FunctionRef, type))


class PickleConverter:
    """Reads an original pickle and writes ``.npz`` / ``.json`` files."""

    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = Path(data_dir)

    # ------------------------------------------------------------------ reading
    def read(self, path):
        """Unpickle ``path`` with stand-in classes and return a nested dict."""
        with open(path, 'rb') as f:
            return self._normalise(_StandInUnpickler(f).load(), str(path))

    def _normalise(self, obj, where):
        """Turn dicts, original-class instances, lists and scalars into a tree
        of dicts, ndarrays and JSON-able scalars."""
        if isinstance(obj, dict):
            for key in obj:
                if not isinstance(key, str):
                    raise TypeError(f'{where}: non-string key {key!r}')
            return {k: self._normalise(v, f'{where}/{k}') for k, v in obj.items()}
        if _is_plain_object(obj):
            return {k: self._normalise(v, f'{where}/{k}') for k, v in vars(obj).items()}
        if isinstance(obj, FunctionRef):
            return f'function:{obj.name}'
        if isinstance(obj, np.ndarray):
            if obj.dtype == object:
                raise TypeError(f'{where}: object array')
            return obj
        if isinstance(obj, np.generic):
            return obj.item()
        if isinstance(obj, (list, tuple)):
            return self._normalise_sequence(obj, where)
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        raise TypeError(f'{where}: cannot convert {type(obj).__name__}')

    def _normalise_sequence(self, seq, where):
        items = [self._normalise(v, f'{where}[{i}]') for i, v in enumerate(seq)]
        if not items:
            return []
        numeric = all(isinstance(v, (int, float, np.ndarray)) and not isinstance(v, bool)
                      for v in items)
        if numeric and len({np.shape(v) for v in items}) == 1:
            return np.array(items)
        if all(isinstance(v, str) for v in items):
            return items
        if all(isinstance(v, np.ndarray) for v in items):
            # arrays of different lengths: stored under the keys "0", "1", ... and
            # turned back into a list by the loader
            return {str(i): v for i, v in enumerate(items)}
        raise TypeError(f'{where}: sequence of mixed items')

    # ----------------------------------------------------------------- pruning
    @staticmethod
    def select(tree, keep, slices=None):
        """Return a copy of ``tree`` holding only the ``/``-separated ``keep`` paths.

        ``slices`` optionally maps a path to an index (e.g. ``np.s_[:, 0]``) that is
        applied to that array before it is stored.
        """
        slices = slices or {}
        out = {}
        for path in keep:
            *parents, leaf = path.split('/')
            src, dst = tree, out
            for key in parents:
                src = src[key]
                dst = dst.setdefault(key, {})
            dst[leaf] = src[leaf][slices[path]] if path in slices else src[leaf]
        return out

    # ----------------------------------------------------------------- writing
    @staticmethod
    def _split(tree, prefix=''):
        arrays, scalars = {}, {}
        for key, value in tree.items():
            path = f'{prefix}{key}'
            if isinstance(value, dict):
                sub_arrays, sub_scalars = PickleConverter._split(value, f'{path}/')
                arrays.update(sub_arrays)
                if sub_scalars:
                    scalars[key] = sub_scalars
            elif isinstance(value, np.ndarray):
                arrays[path] = value
            else:
                scalars[key] = value
        return arrays, scalars

    def write(self, tree, name):
        """Write ``tree`` as ``<name>.npz`` and, if needed, ``<name>.json``."""
        arrays, scalars = self._split(tree)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if arrays:
            np.savez_compressed(self.data_dir / f'{name}.npz', **arrays)
        if scalars:
            with open(self.data_dir / f'{name}.json', 'w') as f:
                json.dump(scalars, f, indent=1)
        return sorted(arrays), scalars

    # --------------------------------------------------------------- verifying
    def verify(self, tree, name):
        """Reload ``<name>`` through the shared loader and compare to ``tree``."""
        import sys
        sys.path.insert(0, str(HERE.parent))
        from tmote2.io import load
        loaded = load(name, self.data_dir)
        self._compare(tree, loaded, name)

    def _compare(self, expected, got, where):
        if isinstance(expected, dict) and isinstance(got, list):
            expected = [expected[str(i)] for i in range(len(expected))]
        if isinstance(expected, dict):
            assert set(expected) == set(got), f'{where}: keys differ'
            for key in expected:
                self._compare(expected[key], got[key], f'{where}/{key}')
        elif isinstance(expected, list) and isinstance(got, list) and expected and isinstance(expected[0], np.ndarray):
            assert len(expected) == len(got), f'{where}: length differs'
            for i, (e, g) in enumerate(zip(expected, got)):
                self._compare(e, g, f'{where}/{i}')
        elif isinstance(expected, np.ndarray):
            assert expected.shape == got.shape and expected.dtype == got.dtype, where
            assert np.array_equal(expected, got, equal_nan=True), f'{where}: values differ'
        else:
            assert expected == got, f'{where}: {expected!r} != {got!r}'


# ----------------------------------------------------------------------------
# What to convert. ``root`` says which folder of original pickles the file is in:
#   'working' - the folder the main-text figures were run in (``--working-jar``)
#   'repo'    - the git repository's ``jar/`` (``--repo-jar``)
# ``keep`` lists the fields the shared figures read; everything else is left out.
# ``figures`` is only used to write the manifest.
# ----------------------------------------------------------------------------
CONVERSIONS = [
    dict(name='gate_corrections', root='working', source='probe_dependence_half_paper_plot.pickle',
         keep=['D_correction'],
         figures='all (shared gate correction)'),
    dict(name='gg_map_fig1', root='working', source='fig1_gg_map.pickle',
         keep=['nn', 'DD', 'Rxx_11_06_sym_200', 'Rxy_11_19_sym_200'],
         figures='Fig 1, S1, S6(d)'),
    dict(name='gg_map_fig2', root='working', source='fig2_gg_map.pickle',
         keep=['nn', 'DD', 'Rxx_11_06_sym_200', 'Rxx_11_06_sym_2'],
         figures='Fig 2 (a, b)'),
    dict(name='B_dependence_one_third', root='working', source='B_dependence_one_third_paper_plot_small_err.pickle',
         keep=['B_array', 'fit_array', 'peak_loc_err', 'y_0', 'fit_params', 'model_function', 'n_post_correction'],
         figures='Fig 3 (a)'),
    dict(name='B_dependence_half', root='working', source='B_dependence_half_paper_plot_small_err.pickle',
         keep=['B_array', 'fit_array', 'peak_loc_err', 'y_0', 'fit_params', 'model_function', 'n_post_correction'],
         figures='Fig 3 (a)'),
    dict(name='B_dependence_two_thirds', root='working', source='B_dependence_two_thirds_paper_plot_small_err.pickle',
         keep=['B_array', 'fit_array', 'peak_loc_err', 'y_0', 'fit_params', 'model_function', 'n_post_correction'],
         figures='Fig 3 (a)'),
    dict(name='fit_expansion', root='repo', source='SI_peaks_expans.pkl',
         keep=['expans/one_third_75'],
         figures='Fig 3 (a): extra fitted point at 0.75 T [peak position, uncertainty]'),
    dict(name='D_dependence', root='working', source='D_dependence_paper_plot.pickle',
         keep=['D_list', 'B_list_gen', 'model_list', 'fit_array_list', 'B_array_list', 'peak_fit_loc_err'],
         figures='Fig 3 (b)'),
    dict(name='probe_dependence_half', root='working', source='probe_dependence_half_paper_plot.pickle',
         keep=['D_correction', 'D_array_20_06', 'R_array_20_06', 'D_array_06_11', 'R_array_06_11',
               'D_array_19_20', 'R_array_19_20'],
         figures='Fig 3 (c)'),
    dict(name='edge_movement', root='repo', source='SI_edge_movement.pkl',
         keep=['two_d_map', 'cuts'],
         figures='S2'),
    dict(name='probe_n_B', root='repo', source='SI_probe_n_B.pkl',
         keep=['probe_data/B_perp', 'probe_data/nn', 'probe_data/R_11_06_long', 'probe_data/R_19_20_long',
               'probe_data/R_20_24_long', 'probe_data/R_06_05_long'],
         figures='S3'),
    dict(name='parallel_field', root='repo', source='SI_B_par.pkl',
         keep=['one_half_data', 'two_thirds_data'],
         figures='S4'),
    dict(name='temperature', root='repo', source='SI_temperature.pkl',
         keep=['temp_data/nn_list_comb_p', 'temp_data/T_set_list_comb_p', 'temp_data/Rxx_11_06_sym',
               'temp_data/Rxy_06_20_anti'],
         figures='S5'),
    dict(name='topology', root='repo', source='SI_topology.pkl',
         keep=['topology_11_06_20/Rxy_06_20_anti_landau_full_n', 'topology_11_06_20/nn_sym_landau_full_n',
               'topology_11_06_20/Bperp_sym_landau_full_n',
               'topology_11_06_20/nn_B_finite_D', 'topology_11_06_20/Bperp_B_finite_D',
               'topology_11_06_20/Rxy_06_20_anti_B_finite_D',
               'topology_11_06_20/nn', 'topology_11_06_20/Rxx_11_06', 'topology_11_06_20/Rxy_06_20'],
         slices={'topology_11_06_20/nn_B_finite_D': np.s_[:, 0],
                 'topology_11_06_20/Bperp_B_finite_D': np.s_[:, 0],
                 'topology_11_06_20/Rxy_06_20_anti_B_finite_D': np.s_[:, 0]},
         figures='S6 (a, b, c); panel (d) uses `gg_map_fig1`'),
    dict(name='n_B_map', root='working', source='B_n_data.pickle',
         keep=['nn', 'DD', 'Bperp', 'Rxx_11_06'],
         figures='Fig 2 (c, d), Fig 3 inset'),
]


def convert_all(roots, conversions=CONVERSIONS, data_dir=DATA_DIR, verify=True, only=None):
    converter = PickleConverter(data_dir)
    rows = []
    for spec in conversions:
        if only and spec['name'] not in only:
            continue
        tree = converter.select(converter.read(Path(roots[spec['root']]) / spec['source']),
                                spec['keep'], spec.get('slices'))
        converter.write(tree, spec['name'])
        if verify:
            converter.verify(tree, spec['name'])
        rows.append(spec)
    return rows


def write_manifest(conversions=CONVERSIONS, data_dir=DATA_DIR):
    lines = ['# Data manifest', '',
             'Written by `provenance/convert_pickles.py`. Each file was verified field by field',
             'against its source pickle after conversion.', '',
             '| Dataset | Original pickle | Fields kept | Used by |', '|---|---|---|---|']
    for spec in conversions:
        fields = ', '.join(f'`{k}`' + (' (first displacement-field slice)' if k in spec.get('slices', {}) else '')
                           for k in spec['keep'])
        lines.append(f"| `{spec['name']}` | `{spec['source']}` | {fields} | {spec['figures']} |")
    (Path(data_dir) / 'MANIFEST.md').write_text('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--working-jar', required=True, type=Path)
    parser.add_argument('--repo-jar', required=True, type=Path)
    parser.add_argument('--only', nargs='*', help='convert only these dataset names')
    parser.add_argument('--no-verify', action='store_true')
    args = parser.parse_args()
    roots = {'working': args.working_jar, 'repo': args.repo_jar}
    convert_all(roots, verify=not args.no_verify, only=args.only)
    write_manifest()


if __name__ == '__main__':
    main()
