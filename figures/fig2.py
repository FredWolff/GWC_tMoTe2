"""Fig. 2: Rxx gate-gate maps at 0.2 T and 2 T (a, b) and the n-B map at fixed D (c)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'

RASTERIZED = True
PROBE = '11_06'
Z_LIMS = (0.03, 200)
CUT_COLORS = {'two_thirds': '#DB5F00', 'one_third': '#7F00A4'}  # the cuts of panel (c) shown in (d)


def map_negative_Rxx(R_array, index_devisor):
    """Replace negative Rxx values: by a very large value above ``index_devisor``
    and by a very small one from there on (i.e. on the two sides of the map)."""
    R_array = np.copy(R_array)
    R_array[:index_devisor][R_array[:index_devisor] < 0] = 1e10
    R_array[index_devisor:][R_array[index_devisor:] < 0] = 1e-2
    return R_array


def _filling_axis(ax_top, v_ticks):
    ax_top.set_xlabel(r'$\nu$')
    ax_top.set_xticks(v_ticks)
    ax_top.set_xticklabels(['-1', '-2/3', '-1/2', '-1/3'])


def gate_gate_panels(ax1, ax2, cax2, gg_map, corr_vec, rasterized):
    """Panels (a) and (b): Rxx versus n and D at low and high field."""
    R_200 = map_negative_Rxx(gg_map.Rxx_11_06_sym_200 / physics.R_Q, 75)
    R_2 = map_negative_Rxx(gg_map.Rxx_11_06_sym_2 / physics.R_Q, 75)

    nn = gg_map.nn + corr_vec[0]
    DD = gg_map.DD - corr_vec[1]
    n_to_12_v = physics.get_v_conversion(PROBE)

    y_lims = (-0.22, 0.32)
    x_lims = (-4.95, -0.85)
    v_lims = (x_lims[0] / np.abs(n_to_12_v), x_lims[1] / np.abs(n_to_12_v))
    norm = mcolors.LogNorm(vmin=Z_LIMS[0], vmax=Z_LIMS[1])

    ax1.pcolormesh(nn * 1e-12, DD, R_200, norm=norm, cmap=style.Rxx_cmap, rasterized=rasterized)
    mesh2 = ax2.pcolormesh(nn * 1e-12, DD, R_2, norm=norm, cmap=style.Rxx_cmap, rasterized=rasterized)

    ax1_top = ax1.twiny()
    ax2_top = ax2.twiny()

    cbar2 = ax2.figure.colorbar(mesh2, cax=cax2)
    cbar2.set_label(r'$R_{xx}$ (h/e$^2$)')

    for ax in (ax1, ax2):
        ax.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
        ax.set_ylabel(r'$D/\epsilon_0$ (V/nm)')
        ax.set_ylim(*y_lims)

    for ax in (ax1, ax2):
        ticks = list(ax.get_xticks())
        ax.set_xticks(ticks[2:])
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.5))
        ax.set_yticks([-0.2, 0, 0.2])
        ax.yaxis.set_minor_locator(MultipleLocator(0.1))

    v_ticks = 1e-12 * np.array([-1, -0.67, -1/2, -0.33])
    for ax_top in (ax1_top, ax2_top):
        _filling_axis(ax_top, v_ticks)

    ax1_top.hlines(0.12, -1.5e-12, -1.12e-12, color='limegreen', linewidth=5)
    ax2_top.hlines(0.12, -1.5e-12, -1.12e-12, color='dodgerblue', linewidth=5)

    for ax in (ax1, ax2):
        ax.set_xlim(x_lims[0], x_lims[1])
    for ax_top in (ax1_top, ax2_top):
        ax_top.set_xlim(v_lims[0], v_lims[1])
    return ax1_top, ax2_top


def peak_cuts(B_n_data, corr_vec, half_window=0.35e12):
    """Densities of the two cuts of panel (c) that are shown in panel (d).

    The 2/3 cut is at the density where the 2/3 peak is highest at 0 T, the 1/3 cut at the
    density where the 1/3 peak is highest at the largest field. Each peak is searched within
    ``half_window`` (cm^-2) of its filling factor. Returns ``{filling: column index}``.
    """
    nn = B_n_data.nn[0] + corr_vec[0]
    B = B_n_data.Bperp[:, 0]
    R_array = B_n_data.Rxx_11_06 / physics.R_Q
    n_per_filling = np.abs(physics.get_v_conversion(PROBE))

    cuts = {}
    for filling, nu, row in (('two_thirds', -2/3, np.argmin(np.abs(B))),
                             ('one_third', -1/3, np.argmax(B))):
        window = np.where(np.abs(nn - nu * n_per_filling) < half_window)[0]
        cuts[filling] = window[np.argmax(R_array[row, window])]
    return cuts


def n_B_panel(ax3, B_n_data, corr_vec, rasterized):
    """Panel (c): Rxx versus n and out-of-plane field, mirrored to negative fields."""
    nn = B_n_data.nn + corr_vec[0]
    BB = B_n_data.Bperp
    R_array = B_n_data.Rxx_11_06 / physics.R_Q

    nn_double = np.concatenate((nn, nn), axis=0)
    BB_double = np.concatenate((BB, np.flip(-BB, axis=0)), axis=0)
    R_double = np.concatenate((R_array, np.flip(R_array, axis=0)), axis=0)

    n_to_12_v = physics.get_v_conversion(PROBE)
    x_lims = (-4.93, -0.85)
    v_lims = (x_lims[0] / np.abs(n_to_12_v), x_lims[1] / np.abs(n_to_12_v))

    ax3.pcolormesh(
        nn_double * 1e-12, BB_double, R_double,
        norm=mcolors.LogNorm(vmin=Z_LIMS[0], vmax=Z_LIMS[1]),
        cmap=style.Rxx_cmap, rasterized=rasterized, zorder=2,
    )
    ax3_top = ax3.twiny()

    ax3.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax3.set_ylabel(r'$\mu_0 H$ (T)')
    ax3.set_xticks([-4, -3, -2, -1])
    ax3.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax3.yaxis.set_major_locator(MultipleLocator(1))
    ax3.yaxis.set_minor_locator(MultipleLocator(0.5))

    _filling_axis(ax3_top, 1e-12 * np.array([-1, -0.67, -1/2, -0.33]))
    ax3_top.hlines(0.2, -1.5e-12, -1.16e-12, color='limegreen', linewidth=5, zorder=3)
    ax3_top.hlines(2, -1.5e-12, -1.16e-12, color='dodgerblue', linewidth=5, zorder=3)

    # markers at the top edge for the cuts that are shown in panel (d)
    for filling, column in peak_cuts(B_n_data, corr_vec).items():
        ax3.vlines(nn[0, column] * 1e-12, 1.98, 2.4, color=CUT_COLORS[filling], linewidth=5, zorder=3)

    ax3.set_xlim(x_lims)
    ax3.set_ylim(np.min(BB_double), np.max(BB_double))  # the markers must not extend the field range
    ax3_top.set_xlim(v_lims)
    return ax3_top


def cuts_panel(ax4, B_n_data, corr_vec):
    """Panel (d): Rxx versus field along the two cuts of panel (c)."""
    B = B_n_data.Bperp[:, 0]
    R_array = B_n_data.Rxx_11_06 / physics.R_Q
    order = np.argsort(B)  # the stored fields run from high to low

    cuts = peak_cuts(B_n_data, corr_vec)
    for filling, label in (('one_third', '-1/3'), ('two_thirds', '-2/3')):
        ax4.plot(B[order], R_array[order, cuts[filling]], color=CUT_COLORS[filling], linewidth=2, label=label)

    ax4.set_yscale('log')
    ax4.set_xlim(0, 2.25)
    ax4.set_ylim(0.03, 500)
    ax4.set_xticks([0, 1, 2])
    ax4.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax4.set_xlabel(r'$\mu_0 H$ (T)')
    ax4.set_ylabel(r'$R_{xx}$ (h/e$^2$)')

    leg = ax4.legend(loc='lower right', title=r'$\nu$', frameon=False)
    style.add_legend_rule(ax4, leg)


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    corr_vec = physics.get_corrections(PROBE)

    fig2 = plt.figure(figsize=(style.FIG_WIDTH, 14))
    hspace = 4
    gs = plt.GridSpec(100, 100, figure=fig2)
    ax1 = fig2.add_subplot(gs[:46 - hspace, :39])
    ax2 = fig2.add_subplot(gs[:46 - hspace, 48:87])
    # colour bar: same column as before, spanning 10.5% to 89.5% of the height of the upper row
    # of panels, i.e. centred on it
    upper_row = gs[:46 - hspace, 88:89].get_position(fig2)
    cax2 = fig2.add_axes([upper_row.x0, upper_row.y0 + 0.105 * upper_row.height,
                          upper_row.width, 0.79 * upper_row.height])
    ax3 = fig2.add_subplot(gs[50 + hspace:, :54])
    ax4 = fig2.add_subplot(gs[50 + hspace:, 65:87])

    B_n_data = io.load('n_B_map')
    ax1_top, ax2_top = gate_gate_panels(ax1, ax2, cax2, io.load('gg_map_fig2'), corr_vec, RASTERIZED)
    ax3_top = n_B_panel(ax3, B_n_data, corr_vec, RASTERIZED)
    cuts_panel(ax4, B_n_data, corr_vec)

    for ax, label in zip([ax1, ax2, ax4], ['(a)', '(b)', '(d)']):
        ax.text(0.03, 0.98, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')

    ax1_top.text(0.02, 0.02, r'$\mu_0 H$ = 0.2T', color='black', transform=ax1_top.transAxes,
                 fontsize=20, va='bottom', ha='left')
    ax2_top.text(0.02, 0.02, r'$\mu_0 H$ = 2T', color='black', transform=ax2_top.transAxes,
                 fontsize=20, va='bottom', ha='left')
    ax3_top.text(0.03, 0.98, '(c)', color='white', transform=ax3_top.transAxes,
                 fontsize=20, va='top', ha='left')
    return {'fig2': fig2}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
