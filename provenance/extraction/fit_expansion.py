# Excerpt of the original analysis code for the dataset "fit_expansion" in data/.
# Fig 3 (a): the extra 1/3 peak position at 0.75 T (the Lorentzian fit that fills `expans`),
# and the expanded goodness-of-fit calculation that uses it. The peak-fit figure that these cells
# also draw is not part of the paper or SI.
#
# Verbatim copy apart from the omitted part marked below, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original SI_figures.py, cell "peak fits", lines 235-489 ---
with open(base_path + f'jar/SI_peaks.pkl', 'rb') as f:
    peaks_data = pickle.load(f)

with open(base_path + f'jar/SI_peaks_data.pkl', 'rb') as f:
    peaks_full_data = pickle.load(f)

with open(base_path + f'jar/SI_peaks_data_steep.pkl', 'rb') as f:
    peaks_full_data_steep = pickle.load(f)
plt.close()

expans = Data()

fig = plt.figure(figsize=(fig_width_cm, 36))
gs = plt.GridSpec(100, 100, figure=fig)

ax1_lim1 = (0, 12)
ax1_lim2 = (17, 29)
ax1_1 = fig.add_subplot(gs[ax1_lim1[0]:ax1_lim1[1], :17])
ax1_2 = fig.add_subplot(gs[ax1_lim1[0]:ax1_lim1[1], 21:38])
ax1_3 = fig.add_subplot(gs[ax1_lim1[0]:ax1_lim1[1], 43:59])
ax1_4 = fig.add_subplot(gs[ax1_lim1[0]:ax1_lim1[1], 64:80])
ax1_5 = fig.add_subplot(gs[ax1_lim1[0]:ax1_lim1[1], 85:])
ax1_6 = fig.add_subplot(gs[ax1_lim2[0]:ax1_lim2[1], :17])
ax1_7 = fig.add_subplot(gs[ax1_lim2[0]:ax1_lim2[1], 21:38])
ax1_8 = fig.add_subplot(gs[ax1_lim2[0]:ax1_lim2[1], 43:60])
ax1_9 = fig.add_subplot(gs[ax1_lim2[0]:ax1_lim2[1], 64:80])
fitless_axes1 = [ax1_1, ax1_2, ax1_3, ax1_4]
axes1 = [ax1_5, ax1_6, ax1_7, ax1_8, ax1_9]

ax2_lim1 = (35, 47)
ax2_lim2 = (52, 64)
ax2_1 = fig.add_subplot(gs[ax2_lim1[0]:ax2_lim1[1], :17])
ax2_2 = fig.add_subplot(gs[ax2_lim1[0]:ax2_lim1[1], 21:38])
ax2_3 = fig.add_subplot(gs[ax2_lim1[0]:ax2_lim1[1], 43:59])
ax2_4 = fig.add_subplot(gs[ax2_lim1[0]:ax2_lim1[1], 64:80])
ax2_5 = fig.add_subplot(gs[ax2_lim1[0]:ax2_lim1[1], 85:])
ax2_6 = fig.add_subplot(gs[ax2_lim2[0]:ax2_lim2[1], :17])
ax2_7 = fig.add_subplot(gs[ax2_lim2[0]:ax2_lim2[1], 21:38])
ax2_8 = fig.add_subplot(gs[ax2_lim2[0]:ax2_lim2[1], 43:60])
ax2_9 = fig.add_subplot(gs[ax2_lim2[0]:ax2_lim2[1], 64:80])
axes2 = [ax2_1, ax2_2, ax2_3, ax2_4, ax2_5, ax2_6, ax2_7, ax2_8, ax2_9]

ax3_lim1 = (71, 83)
ax3_lim2 = (88, 100)
ax3_1 = fig.add_subplot(gs[ax3_lim1[0]:ax3_lim1[1], :17])
ax3_2 = fig.add_subplot(gs[ax3_lim1[0]:ax3_lim1[1], 21:38])
ax3_3 = fig.add_subplot(gs[ax3_lim1[0]:ax3_lim1[1], 43:59])
ax3_4 = fig.add_subplot(gs[ax3_lim1[0]:ax3_lim1[1], 64:80])
ax3_5 = fig.add_subplot(gs[ax3_lim1[0]:ax3_lim1[1], 85:])
ax3_6 = fig.add_subplot(gs[ax3_lim2[0]:ax3_lim2[1], :17])
ax3_7 = fig.add_subplot(gs[ax3_lim2[0]:ax3_lim2[1], 21:38])
ax3_8 = fig.add_subplot(gs[ax3_lim2[0]:ax3_lim2[1], 43:60])
ax3_9 = fig.add_subplot(gs[ax3_lim2[0]:ax3_lim2[1], 64:80])
fitless_axes3 = [ax3_6, ax3_7, ax3_8, ax3_9]
axes3 = [ax3_1, ax3_2, ax3_3, ax3_4, ax3_5]

def transfer(ax_source, ax_target):
    # Transfer lines (from plot)
    for line in ax_source.get_lines():
        ax_target.plot(
            1e-12 * line.get_xdata(),
            line.get_ydata(),
            color=line.get_color(),
            linestyle=line.get_linestyle(),
            marker=line.get_marker(),
            label=line.get_label(),
            linewidth=line.get_linewidth(),
            markersize=line.get_markersize()
        )

    # Optionally, copy axis labels, limits, and title
    ax_target.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    # ax_target.set_ylabel(ax_source.get_ylabel())
    title = (ax_source.get_title().split(',')[0]).split('=')[1]
    ax_target.set_title(r'$\mu_0 H = $' + title)
    ax_target.set_xlim(1e-12 * ax_source.get_xlim()[0], 1e-12 * ax_source.get_xlim()[1])
    ax_target.set_ylim(ax_source.get_ylim())

def transfer_style(ax_source, ax_target, xdata, ydata, title, ylim=None, xlim=None):

    line = ax_source.get_lines()[0]
    ax_target.plot(
        1e-12 * xdata,
        ydata / R_Q,
        color=line.get_color(),
        linestyle=line.get_linestyle(),
        marker=line.get_marker(),
        label=line.get_label(),
        linewidth=line.get_linewidth(),
        markersize=line.get_markersize()
    )

    ax_target.set_xlabel(r'$n$ ($\times10^{12}$ cm$^{-2}$)')
    ax_target.set_title(r'$\mu_0 H = $' + title)
    
    if xlim == None:
        ax_target.set_xlim(1e-12 * ax_source.get_xlim()[0], 1e-12 * ax_source.get_xlim()[1])
    else:
        ax_target.set_xlim(*xlim)

    if ylim == None:
        ax_target.set_ylim(ax_source.get_ylim())
    else:
        ax_target.set_ylim(*ylim)
        #ax_target.set_xlim(1e-12 * ax_source.get_xlim()[0]-0.4, 1e-12 * ax_source.get_xlim()[1])
    
axes_1_3 = sorted([attr for attr in dir(peaks_data['one_third']) if 'ax_' in attr])
axes_1_2 = sorted([attr for attr in dir(peaks_data['half']) if 'ax_' in attr])
axes_2_3 = sorted([attr for attr in dir(peaks_data['two_thirds']) if 'ax_' in attr])

fillings = ['one_third', 'half', 'two_thirds']
for src_axes, tar_axes in zip([axes_1_3, axes_1_2, axes_2_3], [axes1, axes2, axes3]):
    filling = fillings.pop(0)
    i = 0
    while len(src_axes) > 0:
        src_ax = getattr(peaks_data[filling], src_axes[0])
        tar_ax = tar_axes[i]
        transfer(src_ax, tar_ax)
        src_axes.pop(0)
        i += 1

ax_style = getattr(peaks_data['one_third'], 'ax_4')
gen1 = [
    fitless_axes1, 
    ['0.02T', '0.2T', '0.5T', '0.75T'],
    peaks_full_data['full_n_list'][:4],
    peaks_full_data['full_data_list'][:4]
]
for ax, title, xdata, ydata in zip(*gen1):
    if title == '0.75T':
        xarray = np.array(xdata) + corr_vec[0] - n_correction
        indices = np.where((xarray > -1.5e12) & (xarray < -1.2e12))[0]
        p0=[1e14, -1.35e12, 1e9, 0.1*R_Q, 0.1*R_Q/(5e11)]
        popt, pcov = curve_fit(
            lorentzian, 
            xarray[indices], 
            np.array(ydata)[indices], 
            p0=p0,
        )
        ns = np.linspace(
            4 * min(xarray[indices]), 
            0.1 * max(xarray[indices]), 
            301
        )
        ax.plot(ns*1e-12, 
            lorentzian(ns, *popt)/R_Q, 
            color='steelblue', 
            label='fit'
        )
        setattr(
            expans, 
            'one_third_75', 
            [popt[1], np.sqrt(np.diag(pcov)[1])]
        )

    transfer_style(
        ax_style, 
        ax, 
        np.array(xdata) + corr_vec[0] - n_correction, 
        np.array(ydata), 
        title
    )

# (part of the original cell omitted: it concerns fits that are not used in the shared figures)

ax1_1.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax1_6.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax2_1.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax2_6.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax3_1.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
ax3_6.set_ylabel(r'$R_{xx}$ (h/e$^2$)')

labels = ['(a)', '(b)', '(c)']

for ax, label in zip([ax1_1, ax2_1, ax3_1], labels):
    ax.text(
        -0.25, 
        1.15, 
        label, 
        transform=ax.transAxes, 
        fontsize=30, 
        va='top', 
        ha='left'
    )

# fig.savefig(
#     base_path + "SI_fig_exports/fig_peaks.pdf", 
#     dpi=300, 
#     bbox_inches="tight", 
#     transparent=True,
#     backend='pdf',
# )

# with open(base_path + f'jar/SI_peaks_expans.pkl', 'wb') as f:
#     pickle.dump({
#             'expans': expans,
#         }, f)

# plt.figure()
# plt.plot(np.array(gen1[3][1]), '.')
# plt.xlim([50, 90])
# plt.ylim(0*R_Q, 5*R_Q)


# %% --- original SI_figures.py, cell "expanded gof at D = 0.12", lines 127-234 ---

with open(base_path + f'jar/SI_peaks.pkl', 'rb') as f:
    peaks_data = pickle.load(f)

with open(base_path + f'jar/SI_peaks_expans.pkl', 'rb') as f:
    peaks_expans = pickle.load(f)['expans']

if 'data_class' not in globals():
    data_class = load_multiple_datasets('D:/TD5/database/')

probe = '11_06'
step_size = 0.001
for filling in ['half', 'one_third', 'two_thirds']:
    D_lims, n_lims = input_dict[probe][filling].values()

    save_figs = False
    run_bootstrap = False
    asymptote_args = (False, False)

    null_model = lambda x, c: c
    alt_model_1 = lambda x, b, c: b * x + c
    alt_model_2 = lambda x, a, c: a * x**2 + c
    models_to_compare = (null_model, alt_model_1, alt_model_2)

    results = run_study(data_class, 
                        D_lims, 
                        probe, 
                        step=step_size,
                        n_lims=n_lims, 
                        filling=filling, 
                        models_to_compare=models_to_compare,
                        run_bootstrap=run_bootstrap,)

    p1_list = []
    p2_list = []
    a_list = []
    a_unc = []
    model1_popt = []
    model2_popt = []
    alt1_rss = []
    alt2_rss = []

    keys = list(results.keys())
    cut = 0.12
    result = results[cut]

    unc = result.fit_errors[:, 1]
    if filling == 'one_third':
        x0, unc_x0 = getattr(peaks_expans, 'one_third_75')
        unc = np.concatenate((unc, np.array([unc_x0])))
        x_coords = np.concatenate((result.x_max_coords, np.array([x0])))
        B_set_list = np.concatenate((result.B_set_list, np.array([0.75])))
    else:
        x_coords = result.x_max_coords
        B_set_list = result.B_set_list

    c0 = result.x_max_coords[0]
    popt_null, pcov_null = curve_fit(models_to_compare[0], 
                            B_set_list, 
                            x_coords, 
                            p0=c0,
                            sigma=unc,
                            absolute_sigma=True,
                            maxfev=5000)

    b0 = (result.x_max_coords[-1] - result.x_max_coords[0]) / (result.B_set_list[-1] - result.B_set_list[0])
    b0 = -1e9
    popt_1, pcov_1 = curve_fit(models_to_compare[1], 
                            B_set_list, 
                            x_coords, 
                            p0=(b0, c0),
                            sigma=unc,
                            absolute_sigma=True,
                            maxfev=5000)

    a0 = np.sqrt(abs(result.x_max_coords[-1] - result.x_max_coords[0])) / (result.B_set_list[-1] - result.B_set_list[0])
    a0 = -1e10
    popt_2, pcov_2 = curve_fit(models_to_compare[2], 
                            B_set_list, 
                            x_coords, 
                            p0=(a0, c0),
                            sigma=unc,
                            absolute_sigma=True,
                            maxfev=5000)

    # After fitting:
    y_obs = result.x_max_coords
    y_null_fit = np.ones_like(result.B_set_list) * models_to_compare[0](np.array(result.B_set_list), *popt_null)
    y_alt1_fit = models_to_compare[1](np.array(result.B_set_list), *popt_1)
    y_alt2_fit = models_to_compare[2](np.array(result.B_set_list), *popt_2)

    F1, p1 = f_test(y_obs, y_null_fit, y_alt1_fit, 1, 2)  # null vs. alt1
    F2, p2 = f_test(y_obs, y_null_fit, y_alt2_fit, 1, 2)  # null vs. alt2
    p1_list.append(p1)
    p2_list.append(p2)

    a_list.append(popt_2[0])
    a_unc.append(np.sqrt(pcov_2[0,0]))
    model1_popt.append(popt_1)
    model2_popt.append(popt_2)

    alt1_rss.append(np.sum((y_obs - y_alt1_fit) ** 2))
    alt2_rss.append(np.sum((y_obs - y_alt2_fit) ** 2))

    print(f'{filling}: p1 = {p1:.2e}, p2 = {p2:.2e}')


