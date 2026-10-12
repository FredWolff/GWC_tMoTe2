# Excerpt of the original analysis code for the dataset "B_dependence" in data/.
# Fig 3 (a): peak position versus field at the three fillings, 11_06, D=0.12 V/nm.
# The shared data was made with a variant ("small err") of this cell, which is not in the repository:
# it differs only in the stored fit_params of the fits (see data/MANIFEST.md).
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original discrete_v_B_dependence.py, lines 331-462 ---
#%% combine fits from all filling fractions
probe = '11_06'
step_size = 0.001
filling_half = 'half'
filling_one_third = 'one_third'
filling_two_thirds = 'two_thirds'
D_lims_one_third, n_lims_one_third = input_dict[probe][filling_one_third].values()
D_lims_half, n_lims_half = input_dict[probe][filling_half].values()
D_lims_two_thirds, n_lims_two_thirds = input_dict[probe][filling_two_thirds].values()

D_lims_one_third = D_lims_one_third
D_lims_half = D_lims_half
D_lims_two_thirds = D_lims_two_thirds

save_figs = False
run_bootstrap = False
asymptote_args = (True, True) # (show_asymptote_plot, allow_offset)

null_model = lambda x, c: c
alt_model_1 = lambda x, b, c: b * x + c
alt_model_2 = lambda x, a, c: a * x**2 + c
models_to_compare = (null_model, alt_model_1, alt_model_2)

results_one_third = run_study(data_class, 
                        D_lims_one_third, 
                        probe, 
                        step=step_size,
                        n_lims=n_lims_one_third, 
                        filling=filling_one_third, 
                        models_to_compare=models_to_compare,
                        run_bootstrap=run_bootstrap,)

results_half = run_study(data_class, 
                        D_lims_half, 
                        probe, 
                        step=step_size,
                        n_lims=n_lims_half, 
                        filling=filling_half, 
                        models_to_compare=models_to_compare,
                        run_bootstrap=run_bootstrap,)

results_two_thirds = run_study(data_class, 
                        D_lims_two_thirds, 
                        probe, 
                        step=step_size,
                        n_lims=n_lims_two_thirds, 
                        filling=filling_two_thirds, 
                        models_to_compare=models_to_compare,
                        run_bootstrap=run_bootstrap,)
# %%
D_cut = 0.12 - set_D_correction(probe)

fig = plt.figure()
ax = fig.add_subplot(111)

n_post_correction = get_n_correction(probe) - n_correction

filling_list = [filling_one_third, filling_half, filling_two_thirds]
results_list = [results_one_third, results_half, results_two_thirds]

color_dict = {filling_one_third: 'steelblue',
              filling_half: 'crimson',
              filling_two_thirds: 'forestgreen'}

filling_dict = {filling_one_third: r'$\nu$ = 1/3',
                filling_half: r'$\nu$ = 1/2',
                filling_two_thirds: r'$\nu$ = 2/3'}

line_handle_dict = {}

for filling, result_dict in zip(filling_list, results_list):

    model_function = get_model(filling)

    fit_succes = np.array(result_dict[D_cut].fit_succes)
    succesful_fits = np.where(fit_succes == 1)[0]
    failed_fits = np.where(fit_succes == 0)[0]

    filter_flag = np.array(result_dict[D_cut].filter_flag)
    filtered_fits = np.where(filter_flag == 1)[0]

    B_array = np.array(result_dict[D_cut].B_set_list)
    data_array = np.array(result_dict[D_cut].x_max_coords_data)
    fit_array = np.array(result_dict[D_cut].x_max_coords)
    gamma_array = np.array(result_dict[D_cut].fit_gamma)
    peak_fit_loc_err = np.array(result_dict[D_cut].fit_errors)

    y_0 = fit_array[0] + n_post_correction
    
    line_1 = ax.errorbar(B_array[succesful_fits], 
                        fit_array[succesful_fits] + n_post_correction - y_0, 
                        yerr=gamma_array[succesful_fits], 
                        fmt='o', 
                        label=filling_dict[filling] + ', peak with FWHM', 
                        color=color_dict[filling]
    )

    xs = np.linspace(0, 4, 301)
    model_list = model_function(xs, *result_dict[D_cut].MLE_params)
    line_2 = ax.plot(xs, 
                    model_list + n_post_correction - y_0, 
                    label=filling_dict[filling], 
                    color=color_dict[filling]
    )
    line_handle_dict[filling] = line_1

    #extract data for paper plot - filling comparison

    plot_data = {
        'B_array': B_array[succesful_fits],
        'fit_array': fit_array[succesful_fits] + n_post_correction,
        'peak_loc_err': peak_fit_loc_err[succesful_fits][:, 2],
        'y_0': y_0,
        'gamma_array': gamma_array[succesful_fits],
        'fit_params': result_dict[D_cut].MLE_params,
        'model_function': model_function,
        'n_post_correction': n_post_correction,
    }

    if os.getcwd() != plot_path:
        os.chdir(plot_path)

    with open(f'jar/B_dependence_{filling}_paper_plot.pickle', 'wb') as f:
        pickle.dump(plot_data, f)

    os.chdir(base_path)

ax.set_xlabel('B [T]')
ax.set_ylabel(r'$\delta$n [$cm^{-2}$]')
ax.minorticks_on()
ax.legend(handles=line_handle_dict.values())

