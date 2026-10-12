"""Fig. S5: temperature dependence of Rxx and Rxy, and a cut at fixed density."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'

PROBE = '11_06'


def _filling_axis(ax, n_to_12_v):
    ax_extra = ax.twiny()
    ax_extra.set_xlabel(r'$\nu$')
    ax_extra.set_xlim(ax.get_xlim() / np.abs(n_to_12_v))
    ax_extra.set_xticks(1e-12 * np.array([-1, -2/3, -1/2]))
    ax_extra.set_xticklabels(['-1', '-2/3', '-1/2'])


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    n_correction = physics.get_corrections(PROBE)[0]
    temp_data = io.load('temperature').temp_data

    fig, gs = style.new_figure(style.FIG_WIDTH, 13)
    ax1 = fig.add_subplot(gs[:52, :38])
    cax1 = fig.add_subplot(gs[:52, 39:40])
    ax2 = fig.add_subplot(gs[:52, 57:95])
    cax2 = fig.add_subplot(gs[:52, 96:97])
    ax3 = fig.add_subplot(gs[63:, :])

    nn = temp_data.nn_list_comb_p + n_correction
    T_set = temp_data.T_set_list_comb_p
    Rxx = temp_data.Rxx_11_06_sym
    Rxy = temp_data.Rxy_06_20_anti
    n_to_12_v = physics.get_v_conversion(PROBE)

    ######## (a) ########
    mesh0 = ax1.pcolormesh(
        1e-12 * nn, T_set, Rxx / physics.R_Q,
        norm=mcolors.LogNorm(vmin=0.01, vmax=2),
        cmap=style.Rxx_cmap,
        rasterized=True,
    )
    ax1.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax1.set_ylabel(r'$T$ (K)')
    ax1.set_ylim(ax1.get_ylim()[0], 20)
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax1.yaxis.set_major_locator(MultipleLocator(5))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    _filling_axis(ax1, n_to_12_v)
    fig.colorbar(mesh0, cax=cax1).set_label(r'$R_{xx}$ (h/e$^2$)')

    ######## (b) ########
    mesh1 = ax2.pcolormesh(
        1e-12 * nn, T_set, Rxy / physics.R_Q,
        vmin=-1.1, vmax=1.1,
        cmap=style.Rxy_cmap,
        rasterized=True,
    )
    ax2.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax2.set_ylabel(r'$T$ (K)')
    ax2.set_ylim(ax2.get_ylim()[0], 20)
    ax2.xaxis.set_major_locator(MultipleLocator(1))
    ax2.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax2.yaxis.set_major_locator(MultipleLocator(5))
    ax2.yaxis.set_minor_locator(MultipleLocator(1))
    _filling_axis(ax2, n_to_12_v)
    cbar1 = fig.colorbar(mesh1, cax=cax2)
    cbar1.set_label(r'$R_{xy}$ (h/e$^2$)')
    cbar1.ax.yaxis.set_major_locator(MultipleLocator(1))
    cbar1.ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    ######## (c) ########
    cut_index = -41
    ax3.plot(T_set[:, cut_index], Rxx[:, cut_index] / physics.R_Q, color='slateblue')
    ax3.set_ylabel(r'R$_{xx}$ (h/e$^2$)')
    ax3.set_xlabel(r'$T$ (K)')
    ax3.set_xlim(0.03, 20)

    ax3_extra = ax3.twinx()
    ax3_extra.plot(T_set[:, cut_index], Rxy[:, cut_index] / physics.R_Q, color='coral')
    ax3_extra.set_ylabel(r'R$_{xy}$ (h/e$^2$)')
    ax3_extra.set_ylim(-1.1, .1)
    ax3_extra.set_xlim(0.03, 20)
    ax3.xaxis.set_major_locator(MultipleLocator(5))
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    ax3.yaxis.set_major_locator(MultipleLocator(0.1))
    ax3.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax3_extra.yaxis.set_major_locator(MultipleLocator(1))
    ax3_extra.yaxis.set_minor_locator(MultipleLocator(.5))

    # mark the density of the cut in (a) and (b)
    ax1.vlines(1e-12 * nn[0, cut_index], 0.03, 2, color='slateblue', linewidth=5)
    ax2.vlines(1e-12 * nn[0, cut_index], 0.03, 2, color='coral', linewidth=5)

    for ax, label in zip([ax1, ax2, ax3], ['(a)', '(b)', '(c)']):
        ax.text(-0.07, 1.09, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')
    return {'figS5_temperature': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
