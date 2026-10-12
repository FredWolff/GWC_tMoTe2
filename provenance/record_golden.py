"""Record what the ORIGINAL plotting code draws, as the reference for ``tests/``.

This runs the figure cells of the original ``paper_figures.py`` and
``SI_figures.py`` unchanged, against the original data, with
``Figure.savefig`` disabled (so none of the original exports are
overwritten), and stores a summary of every figure in ``tests/golden/``.

It needs the original repository and the folder the main-text figures were run
in, which are not part of this folder::

    python record_golden.py --original-repo <repo> --working-folder <folder> [--runs 2] [--only s1 fig3]

The original cells depend on variables left behind by earlier cells (for
example ``n_to_12_v``). With ``--runs 2`` each cell is executed twice and the
second run is recorded; a warning is printed when the two runs differ.
"""
import argparse
import sys

sys.dont_write_bytecode = True  # never write .pyc files next to the original code
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

HERE = Path(__file__).resolve().parent
SHARE = HERE.parent
sys.path.insert(0, str(SHARE / 'tests'))

from summarize import compare, summarize_figure  # noqa: E402

# module -> (original file, cell title, {output file name: variable holding the figure},
#            variables that the cell expects earlier cells to have defined)
# The presets are the values every earlier cell of the original file assigns.
FIGURES = {
    'fig1': ('paper_figures.py', 'fig 1 2d maps export',
             {'fig1_Rxx_map': 'fig_xx', 'fig1_Rxy_map': 'fig_yy'}, {}),
    'fig2': ('paper_figures.py', 'fig 2', {'fig2': 'fig2'}, {}),
    'fig3': ('paper_figures.py', 'fig 4', {'fig3': 'fig4'}, {}),  # "Fig 4" in the original code
    's2': ('SI_figures.py', 'd-b competition', {'figS2_edge_movement': 'fig'}, {}),
    's3': ('SI_figures.py', 'probe 2', {'figS3_probes': 'fig'}, {}),
    's4': ('SI_figures.py', 'bpar', {'figS4_parallel_field': 'fig'}, {}),
    's5': ('SI_figures.py', 'temperature', {'figS5_temperature': 'fig'}, {'xx_z_lims': (0.01, 50)}),
    's6': ('SI_figures.py', 'topology', {'figS6_topology': 'fig'}, {}),
    's1': ('SI_figures.py', 'mapping', {'figS1_mapping': 'fig'}, {'xx_z_lims': (0.01, 50)}),
}

# The original code in the repository no longer reproduces some of the final figures. These
# amendments replace the text between two markers of an original cell (the markers are kept)
# so that the recorded figure is the final one. {figure: [(start, end, replacement) or function]};
# a function takes the whole cell source and returns the amended source.
def _move_s3_panels(source):
    """Fig. S3: (b) goes to the top right, (c) to the bottom right and the fourth panel, labelled
    "(d)" instead of "(e)", to the bottom left (the original has them at the bottom left, top right
    and bottom right). The colour-bar labels read "R_<probe pair>" instead of "|Z_<probe pair>|"."""
    for old, token in (('ax[1,0]', '@A'), ('ax[0,1]', '@B'), ('ax[1,1]', '@C')):
        source = source.replace(old, token)
    for token, new in (('@A', 'ax[0,1]'), ('@B', 'ax[1,1]'), ('@C', 'ax[1,0]')):
        source = source.replace(token, new)
    source = re.sub(r"\$\\left\| Z_\{([0-9-]+)\} \\right\|\$", lambda m: f"$R_{{{m.group(1)}}}$", source)
    return source.replace("'(e)'", "'(d)'")


def _color_s2_cuts(source):
    """Fig. S2(b): the six cuts run from black (0 T) to green (1 T), RGB (0, 197, 91), in equal steps."""
    old = "label=str(round(getattr(bpar_data['cuts'], f'cut_{i}_b_perp'), 2))"
    assert old in source
    return source.replace(old, old + ",\n                color=tuple(i / 5 * np.array([0, 197, 91]) / 255)")


_FIG2_CUTS = r"""
# panel (d) and the markers of its cuts in panel (c) (not in the original cell)
_nn = B_n_data.nn + corr_vec[0]
_B = B_n_data.Bperp[:, 0]
_R = B_n_data.Rxx_11_06 / R_Q
_cuts = {}
for _f, _nu, _row in (('two_thirds', -2/3, np.argmin(np.abs(_B))), ('one_third', -1/3, np.argmax(_B))):
    _w = np.where(np.abs(_nn[0] - _nu * np.abs(get_v_conversion('11_06'))) < 0.35e12)[0]
    _cuts[_f] = _w[np.argmax(_R[_row, _w])]
_colors = {'two_thirds': '#DB5F00', 'one_third': '#7F00A4'}
for _f, _c in _cuts.items():
    ax3.vlines(_nn[0, _c] * 1e-12, 1.98, 2.4, color=_colors[_f], linewidth=5, zorder=3)
ax3.set_ylim(-np.max(_B), np.max(_B))
_o = np.argsort(_B)
for _f, _l in (('one_third', '-1/3'), ('two_thirds', '-2/3')):
    ax4.plot(_B[_o], _R[_o, _cuts[_f]], color=_colors[_f], linewidth=2, label=_l)
ax4.set_yscale('log')
ax4.set_xlim(0, 2.25)
ax4.set_ylim(0.03, 500)
ax4.set_xticks([0, 1, 2])
ax4.xaxis.set_minor_locator(MultipleLocator(0.5))
ax4.set_xlabel(r'$\mu_0 H$ (T)')
ax4.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax4.legend(loc='lower right', title=r'$\nu$', frameon=False)

"""


def _add_fig2_panel_d(source):
    """Fig. 2: panel (c) is narrower and followed by panel (d), the cuts of (c) against field,
    and carries markers at the cuts (the original cell has panels (a)-(c) only)."""
    old = "ax3 = fig2.add_subplot(gs[50+hspace:, :87])"
    assert old in source
    source = source.replace(old, "ax3 = fig2.add_subplot(gs[50+hspace:, :54])\nax4 = fig2.add_subplot(gs[50+hspace:, 65:87])")
    marker = "#### ax4 ####"
    assert marker in source
    source = source.replace(marker, _FIG2_CUTS + marker, 1)
    old = "labels = ['(a)', '(b)']\n\nfor ax, label in zip([ax1, ax2], labels):"
    assert old in source
    return source.replace(old, "labels = ['(a)', '(b)', '(d)']\n\nfor ax, label in zip([ax1, ax2, ax4], labels):")


AMENDMENTS = {
    'fig2': [_add_fig2_panel_d],
    's2': [_color_s2_cuts],
    's3': [_move_s3_panels],
    # Fig. 3(a): the 2/3 trace uses only the stored points (up to 1 T), fitted with a constant model
    'fig3': [(
        '######### two thirds ########',
        'color_fillings = ',
        """
popt, pcov = curve_fit(
    lambda x, c: fitted_B_two_thirds['model_function'](x, 0, c),
    fitted_B_two_thirds['B_array'],
    fitted_B_two_thirds['fit_array'],
    sigma=fitted_B_two_thirds['peak_loc_err'],
    p0=[fitted_B_two_thirds['y_0']],
    absolute_sigma=True
)
fit_params = fitted_B_two_thirds['fit_params']
fit_params[1] = popt[0] - fitted_B_two_thirds['n_post_correction']
fitted_B_two_thirds['fit_params'] = fit_params

""")],
}

CELL_MARK = re.compile(r'^\s*#\s?%%')


def split_cells(text):
    """``[(title line, source)]`` for each ``#%%`` cell; the first entry is the header."""
    cells, title, lines = [], '', []
    for line in text.splitlines():
        if CELL_MARK.match(line):
            cells.append((title, '\n'.join(lines)))
            title, lines = line, []
        else:
            lines.append(line)
    cells.append((title, '\n'.join(lines)))
    return cells


# The main-text figures were run with the ``functions.py`` of the working folder
# (the script changes into it), the SI figures with the repository's.
def functions_dir(filename, repo, working):
    return working if filename == 'paper_figures.py' else repo


def prelude(header, repo, working, code_dir):
    """The header cell with machine-specific paths replaced and IPython magics removed."""
    out = []
    for line in header.splitlines():
        if line.startswith('%'):
            continue
        for variable, value in (('base_path', str(repo) + '/'),
                                ('import_path', str(repo)),
                                ('plot_path', str(working) + '/')):
            if re.match(rf'{variable}\s*=', line):
                line = f'{variable} = {value!r}'
        out.append(line)
    return f'import sys; sys.path.insert(0, {str(code_dir)!r})\n' + '\n'.join(out)


def find_cell(cells, title):
    for cell_title, source in cells[1:]:
        # "#%% mapping" -> "mapping"
        if CELL_MARK.sub('', cell_title).strip().lower() == title.lower():
            return source
    raise KeyError(title)


def record(name, repo, working, runs, golden_dir):
    filename, title, variables, presets = FIGURES[name]
    cells = split_cells((Path(repo) / filename).read_text())
    header = find_cell(cells, '')  # the untitled cell right after the first "#%%"
    namespace = {'__name__': '__original__', **presets}
    # Figure.savefig is disabled so the original exports are never overwritten
    original_savefig = Figure.savefig
    Figure.savefig = lambda self, *a, **k: None
    try:
        sys.modules.pop('functions', None)  # make sure the right functions.py is imported
        exec(compile(prelude(header, repo, working, functions_dir(filename, repo, working)),
                     '<original header>', 'exec'), namespace)
        # Pickles written from a notebook refer to classes in ``__main__``
        import __main__
        for class_name in ('Data', 'Results'):
            if class_name in namespace:
                setattr(__main__, class_name, namespace[class_name])
        source = find_cell(cells, title)
        for amendment in AMENDMENTS.get(name, []):
            if callable(amendment):
                source = amendment(source)
            else:
                start, end, replacement = amendment
                a, b = source.index(start) + len(start), source.index(end)
                source = source[:a] + replacement + source[b:]
        run_summaries = []
        for _ in range(runs):
            plt.close('all')
            exec(compile(source, '<original cell>', 'exec'), namespace)
            run_summaries.append({stem: summarize_figure(namespace[var]) for stem, var in variables.items()})
    finally:
        Figure.savefig = original_savefig
    if runs > 1 and compare(run_summaries[0], run_summaries[-1]):
        print(f'WARNING {name}: first and last run differ (cell depends on leftover state):')
        for diff in compare(run_summaries[0], run_summaries[-1])[:10]:
            print('   ', diff)
    (Path(golden_dir) / f'{name}.json').write_text(json.dumps(run_summaries[-1], indent=1))
    print(f'recorded {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--original-repo', required=True, type=Path)
    parser.add_argument('--working-folder', required=True, type=Path)
    parser.add_argument('--runs', type=int, default=2)
    parser.add_argument('--only', nargs='*')
    args = parser.parse_args()
    golden_dir = SHARE / 'tests' / 'golden'
    golden_dir.mkdir(exist_ok=True)
    for name in FIGURES:
        if not args.only or name in args.only:
            record(name, args.original_repo, args.working_folder, args.runs, golden_dir)


if __name__ == '__main__':
    main()
