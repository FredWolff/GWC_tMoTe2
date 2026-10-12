"""Fig. S1: conversion between gate voltages and (n, D)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    probe = '11_06'
    n_correction, D_correction = physics.get_corrections(probe)
    gg_map = io.load('gg_map_fig1')

    fig, gs = style.new_figure(style.FIG_WIDTH, 7)
    ax1 = fig.add_subplot(gs[:, :38])
    cax1 = fig.add_subplot(gs[:, 39:40])
    ax2 = fig.add_subplot(gs[:, 57:95])
    cax2 = fig.add_subplot(gs[:, 96:97])

    nn_uncorr, DD_uncorr = gg_map.nn, gg_map.DD
    Rxx = gg_map.Rxx_11_06_sym_200 / physics.R_Q
    Vt, Vb = physics.n_D_to_Vt_Vb(nn_uncorr, DD_uncorr, physics.cbg, physics.ctg)
    xx_z_lims = (0.01, 50)

    ########## (a) #########
    mesh0 = ax1.pcolormesh(
        Vt, Vb, Rxx,
        norm=mcolors.LogNorm(vmin=xx_z_lims[0], vmax=xx_z_lims[1]),
        cmap=style.Rxx_cmap,
        rasterized=True,
    )
    ax1.set_xlabel(r'$V_t$ (V)')
    ax1.set_ylabel(r'$V_b$ (V)')
    cbar0 = fig.colorbar(mesh0, cax=cax1)
    cbar0.set_label(r'$R_{xx}$ (h/e$^2$)')

    ########## (b) #########
    nn = nn_uncorr + n_correction
    DD = DD_uncorr - D_correction
    n_to_12_v = physics.get_v_conversion(probe)

    mesh1 = ax2.pcolormesh(
        1e-12 * nn, DD, Rxx,
        norm=mcolors.LogNorm(vmin=xx_z_lims[0], vmax=xx_z_lims[1]),
        cmap=style.Rxx_cmap,
        rasterized=True,
    )
    ax2_extra = ax2.twiny()

    cbar1 = fig.colorbar(mesh1, cax=cax2)
    cbar1.set_label(r'$R_{xx}$ (h/e$^2$)')
    ax2.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax2.set_ylabel(r'$D/\epsilon_0$ (V/nm)')
    ax2.xaxis.set_major_locator(MultipleLocator(2))
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    ax2.yaxis.set_major_locator(MultipleLocator(0.2))
    ax2.yaxis.set_minor_locator(MultipleLocator(0.1))

    ax2_extra.set_xlabel(r'$\nu$')
    ax2_extra.set_xlim(ax2.get_xlim() / np.abs(n_to_12_v))
    ax2_extra.set_xticks(1e-12 * np.array([-1, -2/3, -1/2, -1/3, 0]))
    ax2_extra.set_xticklabels(['-1', '-2/3', '-1/2', '-1/3', '0'])

    for ax, label in zip([ax1, ax2], ['(a)', '(b)']):
        ax.text(-0.07, 1.08, label, transform=ax.transAxes,
                fontsize=20, va='top', ha='left')
    return {'figS1_mapping': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
