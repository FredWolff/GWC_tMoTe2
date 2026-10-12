"""Fig. 1: gate-gate maps of Rxx (log scale) and Rxy (linear scale) in (n, D) with a filling-factor axis."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'


def _finish_axes(ax, ax_top, n_to_12_v, x_lims, v_lims, y_lims):
    ax.set_xlabel(r'$n$ ($10^{12}$ cm$^{-2}$)')
    ax.set_ylabel(r'$D/\epsilon_0$ (V/nm)')
    ax_top.set_xlabel(r'$\nu$')

    ax.xaxis.set_major_locator(MultipleLocator(base=2, offset=1))
    ax.xaxis.set_minor_locator(MultipleLocator(base=1, offset=1))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))

    ax_top.set_xlim(ax.get_xlim() / np.abs(n_to_12_v))
    ax_top.set_xticks(np.array([-1, -2/3, -1/2, -1/3, 0]))
    ax_top.set_xticklabels(['-1', '-2/3', '-1/2', '-1/3', '0'])

    ax.set_xlim(x_lims[0], x_lims[1])
    ax_top.set_xlim(v_lims[0], v_lims[1])
    ax.set_ylim(*y_lims)


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    probe = '11_06'
    n_correction, D_correction = physics.get_corrections(probe)
    gg_map = io.load('gg_map_fig1')

    fig_xx = plt.figure(figsize=(6, 6))
    fig_yy = plt.figure(figsize=(6, 6))
    ax_xx = fig_xx.add_subplot(111)
    ax_yy = fig_yy.add_subplot(111)

    n_to_12_v = physics.get_v_conversion(probe)
    x_lims = (-5.1, -0.9)
    v_lims = (-5.1e12 / np.abs(n_to_12_v), -0.9e12 / np.abs(n_to_12_v))
    y_lims = (-0.21, 0.28)
    xx_z_lims = (0.03, 200)
    xy_z_lims = (-2, 2)

    pos = ax_xx.get_position()  # [x0, y0, width, height] in figure fractions
    cax_xx = fig_xx.add_axes([pos.x1 + 0.01, pos.y0, 0.02, pos.height])
    cax_yy = fig_yy.add_axes([pos.x1 + 0.01, pos.y0, 0.02, pos.height])

    Rxx = gg_map.Rxx_11_06_sym_200 / physics.R_Q
    Rxy = gg_map.Rxy_11_19_sym_200 / physics.R_Q
    nn = gg_map.nn + n_correction
    DD = gg_map.DD - D_correction
    vv = nn / np.abs(n_to_12_v)

    xx_norm = mcolors.LogNorm(vmin=xx_z_lims[0], vmax=xx_z_lims[1])

    mesh_xx = ax_xx.pcolormesh(1e-12 * nn, DD, Rxx, norm=xx_norm, cmap=style.Rxx_cmap, rasterized=True)
    mesh_yy = ax_yy.pcolormesh(1e-12 * nn, DD, Rxy, vmin=xy_z_lims[0], vmax=xy_z_lims[1],
                               cmap=style.Rxy_cmap, rasterized=True)

    # the same maps again against the filling factor, on the twin x axes
    ax_xx_top = ax_xx.twiny()
    ax_xx_top.pcolormesh(vv, DD, Rxx, norm=xx_norm, cmap=style.Rxx_cmap, rasterized=True)
    ax_yy_top = ax_yy.twiny()
    ax_yy_top.pcolormesh(vv, DD, Rxy, vmin=xy_z_lims[0], vmax=xy_z_lims[1],
                         cmap=style.Rxy_cmap, rasterized=True)

    cbar_xx = fig_xx.colorbar(mesh_xx, cax=cax_xx)
    cbar_yy = fig_yy.colorbar(mesh_yy, cax=cax_yy)
    cbar_xx.set_label(r'$R_{xx}$ (h/e$^2$)', rotation=270, labelpad=17)
    cbar_yy.set_label(r'$R_{xy}$ (h/e$^2$)', rotation=270, labelpad=17)
    cbar_yy.ax.yaxis.set_major_locator(MultipleLocator(2))
    cbar_yy.ax.yaxis.set_minor_locator(MultipleLocator(1))

    for ax, ax_top in ((ax_xx, ax_xx_top), (ax_yy, ax_yy_top)):
        _finish_axes(ax, ax_top, n_to_12_v, x_lims, v_lims, y_lims)

    return {'fig1_Rxx_map': fig_xx, 'fig1_Rxy_map': fig_yy}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
