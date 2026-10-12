"""Fig. S6: topology of the states: the Hall resistance in the n-B plane (a, b), cuts in n (c) and the Rxy map (d).

The slopes of the transitions in (a) and (b), in units of the slope expected for the
corresponding filling factor, are printed when the figure is built.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style
from tmote2.fitting import fit_transition_line, linear_model

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'

PROBE = '11_06'
# slope of the density-field line of a state at filling nu = -1: e/h per tesla, in cm^-2
SLOPE_NU_1 = physics.elementary_q * 1e-4 / physics.h_Planck


def _print_slope(label, params, errors):
    print(f'slope for {label} = {params[0] / SLOPE_NU_1}+/-{errors[0] / SLOPE_NU_1}')


def _filling_axis(ax, n_to_12_v, ticks, labels):
    ax_extra = ax.twiny()
    ax_extra.set_xlabel(r'$\nu$')
    ax_extra.set_xlim(ax.get_xlim() / np.abs(n_to_12_v))
    ax_extra.set_xticks(1e-12 * np.array(ticks))
    ax_extra.set_xticklabels(labels)


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    n_correction, D_correction = physics.get_corrections(PROBE)
    n_to_12_v = physics.get_v_conversion(PROBE)
    R_Q = physics.R_Q
    topo = io.load('topology').topology_11_06_20

    fig, gs = style.new_figure(style.FIG_WIDTH, 10)
    ax1 = fig.add_subplot(gs[:41, :40])
    cax1 = fig.add_subplot(gs[:41, 41:42])
    ax2 = fig.add_subplot(gs[:41, 55:95])
    cax2 = fig.add_subplot(gs[:41, 96:97])
    ax3 = fig.add_subplot(gs[59:, :56])
    ax4 = fig.add_subplot(gs[59:, 68:95])
    cax4 = fig.add_subplot(gs[59:, 96:97])

    ######### (a) #########
    Rxy = topo.Rxy_06_20_anti_landau_full_n
    Bperp = topo.Bperp_sym_landau_full_n
    nn = topo.nn_sym_landau_full_n + n_correction
    n_index = [0, -1]

    im1 = ax1.pcolormesh(
        1e-12 * nn[:, n_index[0]:n_index[1]],
        -Bperp[:, n_index[0]:n_index[1]],
        -Rxy[:, n_index[0]:n_index[1]] / R_Q,
        vmin=-1.5, vmax=1.5,
        cmap=style.Rxy_cmap,
        rasterized=True,
    )

    # line through the sigmoid transitions of the first 40 field values
    params, errors = fit_transition_line(Rxy[:40, 90:150], nn[0, 90:150], Bperp[:40, 0], x0_guess=-4e12)
    ax1.plot(linear_model(Bperp[:40, 0], *params) * 1e-12, Bperp[:40, 0], color='black')
    _print_slope(r'$\nu = -1$', params, errors)

    ax1_extra = ax1.twiny()
    ax1.set_ylabel(r'$\mu_0 H$ (T)')
    ax1.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax1.set_xlim(-4.6, -3.6)
    fig.colorbar(im1, cax=cax1, label=r'$R_{xy}$ (h/e$^2$)')

    ax1.xaxis.set_major_locator(MultipleLocator(0.5))
    ax1.xaxis.set_minor_locator(MultipleLocator(0.25))
    ax1.set_yticks([-4, -2, 0, 2, 4])
    ax1.yaxis.set_minor_locator(MultipleLocator(1))

    ax1_extra.set_xlabel(r'$\nu$')
    ax1_extra.set_xlim(ax1.get_xlim() / np.abs(n_to_12_v))
    ax1_extra.set_xticks(1e-12 * np.array([-1]))
    ax1_extra.set_xticklabels(['-1'])

    ######### (b) #########
    # The stored arrays are the slice at the first displacement field
    Rxy = topo.Rxy_06_20_anti_B_finite_D
    Bperp = topo.Bperp_B_finite_D
    nn = topo.nn_B_finite_D + n_correction

    im2 = ax2.pcolormesh(
        1e-12 * nn, Bperp, Rxy / R_Q,
        vmin=-1.5, vmax=1.5,
        cmap=style.Rxy_cmap,
        rasterized=True,
    )

    fields = Bperp[:75, 0]
    params, errors = fit_transition_line(-Rxy[:75], nn[0], fields, x0_guess=-2.5e12)
    ax2.plot(linear_model(fields, *params) * 1e-12, fields, color='black')
    _print_slope(r'$\nu = -2/3$', params, errors)

    ax2.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax2.set_ylabel(r'$\mu_0 H $ (T)')
    ax2.set_ylim(-4, 4)
    ax2.set_xlim(-3.5, -2.6)
    fig.colorbar(im2, cax=cax2, label=r'$R_{xy}$ (h/e$^2$)')

    ax2.xaxis.set_major_locator(MultipleLocator(0.5))
    ax2.xaxis.set_minor_locator(MultipleLocator(0.25))
    ax1.set_yticks([-4, -2, 0, 2, 4])
    ax1.yaxis.set_minor_locator(MultipleLocator(1))

    _filling_axis(ax2, n_to_12_v, [-2/3], ['-2/3'])

    ######### (c) #########
    nn = topo.nn + n_correction

    ax3.plot(1e-12 * nn, topo.Rxx_11_06 / R_Q, color='slateblue')
    ax3.set_xlabel(r'$n$ (10$^{12}$ cm$^{-2}$)')
    ax3.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
    ax3.spines['left'].set_color('slateblue')
    ax3.set_xlim(-4.5, -1.85)
    ax3.set_ylim(-0.14, 3.5)

    ax3.xaxis.set_major_locator(MultipleLocator(1))
    ax3.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax3.yaxis.set_minor_locator(MultipleLocator(.5))

    ax3_extra_x = ax3.twinx()
    ax3_extra = ax3_extra_x.twiny()
    ax3_extra.set_xlim(ax3.get_xlim())
    ax3_extra.plot(1e-12 * nn, -topo.Rxy_06_20 / R_Q, color='coral')
    ax3_extra_x.set_ylabel(r'$R_{xy}$ (h/e$^2$)')
    ax3_extra.set_xlabel(r'$\nu$')
    ax3_extra.set_ylim(-0.1, 2.5)
    ax3_extra.yaxis.set_minor_locator(MultipleLocator(.5))

    ax3_extra.set_xticks(1e-12 * np.array([-1, -2/3, -1/2]) * np.abs(n_to_12_v))
    ax3_extra.set_xticklabels(['-1', '-2/3', '-1/2'])
    ax3_extra.hlines(1, -5, -1, colors='black', linestyles='--')

    ########## (d) ##########
    gg_map = io.load('gg_map_fig1')
    Rxy_200 = gg_map.Rxy_11_19_sym_200 / R_Q
    nn = gg_map.nn + n_correction
    DD = gg_map.DD - D_correction

    mesh4 = ax4.pcolormesh(
        1e-12 * nn, DD, Rxy_200,
        vmin=-2, vmax=2,
        cmap=style.Rxy_cmap,
        rasterized=True,
    )
    ax4.hlines(0.035, -4.5, -3.6, colors='blue', linestyles='--')
    ax4.hlines(0.005, -3.5, -2.6, colors='red', linestyles='--')
    ax4.set_xlim(-4.5, -2)
    ax4.set_ylim(-0.1, 0.2)

    ax4_extra = ax4.twiny()

    cbar = fig.colorbar(mesh4, cax=cax4)
    cbar.set_label(r'$R_{xy}$ (h/e$^2$)')
    ax4.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax4.set_ylabel(r'$D/\epsilon_0$ (V/nm)')
    ax4.xaxis.set_major_locator(MultipleLocator(2))
    ax4.xaxis.set_minor_locator(MultipleLocator(1))
    ax4.yaxis.set_major_locator(MultipleLocator(0.2))
    ax4.yaxis.set_minor_locator(MultipleLocator(0.1))

    ax4_extra.set_xlabel(r'$\nu$')
    ax4_extra.set_xlim(ax4.get_xlim() / np.abs(n_to_12_v))
    ax4_extra.set_xticks(1e-12 * np.array([-1, -2/3, -1/2]))
    ax4_extra.set_xticklabels(['-1', '-2/3', '-1/2'])

    for ax, label in zip([ax1, ax2, ax3, ax4], ['(a)', '(b)', '(c)', '(d)']):
        ax.text(-0.11, 1.09, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')
    return {'figS6_topology': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
