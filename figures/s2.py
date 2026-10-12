"""Fig. S2: magnetic-field response of the resistance edge at fixed density."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'

CUT_COLOR = '#00C55B'  # colour of the highest-field cut in panel (b)


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    D_correction = physics.get_corrections()[1]
    data = io.load('edge_movement')

    fig, gs = style.new_figure(style.FIG_WIDTH, 7)
    ax1 = fig.add_subplot(gs[:, :42])
    cax1 = fig.add_subplot(gs[:, 43:44])
    ax2 = fig.add_subplot(gs[:, 57:])

    ########## (a) #########
    DD = data.two_d_map.d_at_fixed_n - D_correction
    mesh = ax1.pcolormesh(
        DD, data.two_d_map.b_perp, data.two_d_map.res_2d_sym / physics.R_Q,
        norm=mcolors.LogNorm(vmin=1e-1, vmax=2),
        cmap=style.Rxx_cmap,
        rasterized=True,
    )
    fig.colorbar(mesh, cax=cax1, label=r'$R_{xx}$ (h/e$^2$)')

    ########## (b) #########
    n_cuts = 0
    while f'cut_{n_cuts}_res_sym' in data.cuts:  # one line per field value stored
        n_cuts += 1
    # from black at the lowest field to green at the highest
    colors = style.generate_con_color(CUT_COLOR, n_cuts)[::-1]
    for i in range(n_cuts):
        ax2.plot(
            data.cuts[f'cut_{i}_d_at_fixed_n'] - D_correction,
            data.cuts[f'cut_{i}_res_sym'] / physics.R_Q,
            label=str(round(float(data.cuts[f'cut_{i}_b_perp']), 2)),
            color=colors[i],
        )

    for ax in (ax1, ax2):
        ax.set_xlabel(r'$D/\epsilon_0$ (V/nm)')
        ax.set_xlim(np.min(DD), 0.14)
        ax.xaxis.set_major_locator(MultipleLocator(0.1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.05))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax1.set_ylabel(r'$\mu_0 H$ (T)')
    ax2.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
    ax2.set_ylim(0, 2)

    leg = ax2.legend(loc='center left', title=r'$\mu_0 H$ (T)', bbox_to_anchor=(0.25, 0.65))
    leg.get_frame().set_alpha(0)

    for ax, label in zip([ax1, ax2], ['(a)', '(b)']):
        ax.text(-0.11, 1.03, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')
    return {'figS2_edge_movement': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
