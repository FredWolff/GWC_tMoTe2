"""Fig. 3: magnetic-field (a), displacement-field (b) and probe (c) dependence of the peak positions.

Called "Fig. 4" in the original analysis code.

(a) Peak position (relative to zero field) versus field at the three fillings,
    with fits and, in the inset, the n-B map they sit on.
(b) The 1/2 peak versus density at three displacement fields, with fits.
(c) Resistance at 1/2 filling versus displacement field for three probe pairs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.optimize import curve_fit

from tmote2 import io, physics, style
from tmote2.fitting import model_from_name

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'

PROBE = '11_06'
RASTERIZED = True
IN_OUT_STYLE = {'in': 'solid', 'out': 'dashed'}
SHAPES = ['o', 'o', 'o']
FILLING_COLORS = [style.color_1_3, style.color_1_2, style.color_2_3]
PROBE_COLORS = ['darkmagenta', 'royalblue', 'DarkBlue']  # 20-06, 06-11, 19-20
LINESTYLES = ['-', '-', '-']

# Markers: capthick=0 etc. are the settings of the original errorbar plots
ERRORBAR_STYLE = dict(capthick=0, capsize=0, elinewidth=2, markeredgecolor='black',
                      markeredgewidth=0, markersize=9)


# ------------------------------------------------------------------- panel (a)
class PeakFit:
    """Peak positions versus field for one filling and the model fitted to them."""

    def __init__(self, data, B_array, fit_array, peak_loc_err, y_0, fit_params):
        self.model = model_from_name(data.model_function)
        self.n_post_correction = data.n_post_correction
        self.B_array = B_array
        self.fit_array = fit_array
        self.peak_loc_err = peak_loc_err
        self.y_0 = y_0
        # Parameters of the model in the density coordinates that are plotted
        # (the stored parameters are shifted by -n_post_correction)
        self.params = np.asarray(fit_params, dtype=float) + np.array([0, self.n_post_correction])


def _fit_peaks(model, B_array, fit_array, peak_loc_err, p0):
    popt, _ = curve_fit(model, B_array, fit_array, sigma=peak_loc_err, p0=p0, absolute_sigma=True)
    return popt


def load_peak_fits():
    """The three PeakFit objects, with the extra 1/3 point at 0.75 T and the refits of the 1/3 and 2/3 constants."""
    expans = io.load('fit_expansion').expans

    # ---- 1/3: one extra point at 0.75 T, constant refitted
    d = io.load('B_dependence_one_third')
    B = np.concatenate(([0.75], d.B_array))
    fit = np.concatenate(([expans.one_third_75[0]], d.fit_array))
    err = np.concatenate(([expans.one_third_75[1]], d.peak_loc_err))
    y_0 = fit[0]
    constant = model_from_name(d.model_function)
    (c,) = _fit_peaks(lambda x, c: constant(x, 0, c), B, fit, err, p0=[y_0])
    params = np.array(d.fit_params, dtype=float)
    params[1] = c - d.n_post_correction
    one_third = PeakFit(d, B, fit, err, y_0, params)

    # ---- 1/2: as stored
    d = io.load('B_dependence_half')
    half = PeakFit(d, d.B_array, d.fit_array, d.peak_loc_err, d.y_0, d.fit_params)

    # ---- 2/3: only the points up to 1 T, constant refitted
    d = io.load('B_dependence_two_thirds')
    constant = model_from_name(d.model_function)
    (c,) = _fit_peaks(lambda x, c: constant(x, 0, c), d.B_array, d.fit_array, d.peak_loc_err, p0=[d.y_0])
    params = np.array(d.fit_params, dtype=float)
    params[1] = c - d.n_post_correction
    two_thirds = PeakFit(d, d.B_array, d.fit_array, d.peak_loc_err, d.y_0, params)

    return one_third, half, two_thirds


def _gen_B_in_out(B_lim, B_sample):
    B_in = np.linspace(np.min(B_sample), np.max(B_sample), 151)
    B_out = np.linspace(np.min(B_lim), np.max(B_lim), 151)
    return B_in, B_out


def peak_position_panel(ax, fits):
    """Panel (a): density shift of the peaks versus field."""
    for fit, shape, color, label in zip(fits, SHAPES, FILLING_COLORS, ['1/3', '1/2', '2/3']):
        ax.errorbar(fit.fit_array - fit.y_0, fit.B_array, fmt=shape, xerr=fit.peak_loc_err,
                    label=label, color=color, **ERRORBAR_STYLE)

    B_lim = np.array([-0.1, 4.1])
    for fit, color in zip(fits, FILLING_COLORS):
        B_in, B_out = _gen_B_in_out(B_lim, fit.B_array)
        ax.plot(fit.model(B_out, *fit.params) - fit.y_0, B_out, linestyle=IN_OUT_STYLE['out'], color=color)
        ax.plot(fit.model(B_in, *fit.params) - fit.y_0, B_in, linestyle=IN_OUT_STYLE['in'], color=color)

    ax.get_xaxis().get_offset_text().set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(1e11))
    ax.xaxis.set_minor_locator(MultipleLocator(.5e11))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(.5))

    leg = ax.legend(loc='center left', title=r'$\nu$', bbox_to_anchor=(0, 0.65))
    leg.get_frame().set_alpha(0)

    ax.set_xlabel(r'$\delta n$ ($\times 10^{11}$ cm$^{-2}$)')
    ax.set_ylabel(r'$\mu_0 H$ (T)')
    ax.set_ylim(-0.1, 4.1)


def inset_panel(ax_ins, B_n_data, corr_vec, fits, rasterized):
    """Inset of (a): the n-B map with the fitted peak positions on top."""
    nn = B_n_data.nn + corr_vec[0]
    BB = B_n_data.Bperp
    R_array = B_n_data.Rxx_11_06 / physics.R_Q
    n_to_12_v = physics.get_v_conversion(PROBE)

    ax_ins.pcolormesh(nn, BB, R_array, norm=mcolors.LogNorm(vmin=0.01, vmax=200),
                      cmap=style.Rxx_cmap, rasterized=rasterized)

    B_lim = np.array([-0.05, 2.5])
    for fit, color in zip(fits, FILLING_COLORS):
        B_in, B_out = _gen_B_in_out(B_lim, fit.B_array)
        ax_ins.plot(fit.model(B_out, *fit.params), B_out, linestyle=IN_OUT_STYLE['out'],
                    color=color, linewidth=1.5)
        ax_ins.plot(fit.model(B_in, *fit.params), B_in, linestyle=IN_OUT_STYLE['in'],
                    color=color, linewidth=1.5)

    ax_ins.set_xticks([n_to_12_v / 3, n_to_12_v / 2, 2 * n_to_12_v / 3])
    ax_ins.set_xticklabels(['-1/3', '-1/2', '-2/3'])
    ax_ins.yaxis.set_major_locator(MultipleLocator(2))
    ax_ins.yaxis.set_minor_locator(MultipleLocator(1))
    ax_ins.set_xlim((-3.2e12, -1e12))
    ax_ins.set_ylim(np.min(BB), np.max(BB))
    ax_ins.set_xlabel(r'$\nu$')
    ax_ins.set_ylabel(r'$\mu_0 H$ (T)')


# ------------------------------------------------------------------- panel (b)
def displacement_field_panel(ax, D_dependence_data):
    """Panel (b): the 1/2 peak at three displacement fields."""
    D_list = D_dependence_data['D_list']
    model_list = D_dependence_data['model_list']
    B_list_gen = D_dependence_data['B_list_gen']
    color_list = style.generate_con_color(style.color_1_2, len(D_list))
    x_data = D_dependence_data['fit_array_list']
    y_data = D_dependence_data['B_array_list']
    x_err = D_dependence_data['peak_fit_loc_err']

    D_index_corr = -15
    line_handles = []
    for i in [15, len(D_list) // 2 + 2, -11]:
        line, = ax.plot(model_list[i], B_list_gen, color=color_list[i])
        line_handles.append(line)
        ax.errorbar(x_data[i], y_data[i], fmt=SHAPES[0], xerr=x_err[i], label='1/3',
                    color=color_list[i], **ERRORBAR_STYLE)

    leg = ax.legend(
        handles=[line_handles[0], line_handles[1], line_handles[-1]],
        labels=[f'{D_list[15 + D_index_corr]:.2f}',
                f'{D_list[len(D_list) // 2 + 2 + D_index_corr]:.2f}',
                f'{D_list[-11 + D_index_corr]:.2f}'],
        title=r'$D/\epsilon_{0}$ (V/nm)',
    )
    leg.get_frame().set_alpha(0)

    ax.get_xaxis().get_offset_text().set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(2e11))
    ax.xaxis.set_minor_locator(MultipleLocator(1e11))
    ax.yaxis.set_minor_locator(MultipleLocator(.5))
    ax.set_ylim(0, 4.21)
    ax.set_xlim(-2.65e12, -2.05e12)
    ax.set_ylabel(r'$\mu_0 H$ (T)')
    ax.set_xlabel(r'$n$ ($\times 10^{12}$ cm$^{-2}$)')


# ------------------------------------------------------------------- panel (c)
def probe_panel(ax, probe_dependence_data):
    """Panel (c): resistance at 1/2 filling versus displacement field for three probe pairs."""
    d = probe_dependence_data
    uni_D_corr = d['D_correction']
    for key, label, color, linestyle in (('06_11', '06-11', PROBE_COLORS[1], LINESTYLES[1]),
                                         ('19_20', '19-20', PROBE_COLORS[2], LINESTYLES[2]),
                                         ('20_06', '20-06', PROBE_COLORS[0], LINESTYLES[0])):
        ax.plot(d[f'D_array_{key}'] - uni_D_corr, d[f'R_array_{key}'] / physics.R_Q,
                label=label, color=color, linestyle=linestyle, linewidth=2)

    ax.xaxis.set_minor_locator(MultipleLocator(.05))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.set_ylabel(r'$R$ (h/e$^2$)')
    ax.set_xlabel(r'$D/\epsilon_0$ (V/nm)')
    ax.set_xlim(-0.13, 0.13)
    ax.set_ylim(0, 10.5)


# ---------------------------------------------------------------------- figure
def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    corr_vec = physics.get_corrections(PROBE)

    fig = plt.figure(figsize=(style.FIG_WIDTH, 8), dpi=300)
    gs = plt.GridSpec(100, 100, figure=fig)
    ax1 = fig.add_subplot(gs[:, :58])
    ax1_ins = inset_axes(ax1, width="53%", height="32%", loc=3, borderpad=2.6)
    ax3 = fig.add_subplot(gs[:44, 66:])
    ax4 = fig.add_subplot(gs[57:, 66:])

    fits = load_peak_fits()
    peak_position_panel(ax1, fits)
    inset_panel(ax1_ins, io.load('n_B_map'), corr_vec, fits, RASTERIZED)
    displacement_field_panel(ax3, io.load('D_dependence'))
    probe_panel(ax4, io.load('probe_dependence_half'))

    for ax, label in zip([ax1, ax3, ax4], ['(a)', '(b)', '(c)']):
        ax.text(0.02, 0.95, label, transform=ax.transAxes, va='top', ha='left')
    return {'fig3': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory, bbox_inches=None)


if __name__ == '__main__':
    save(build())
