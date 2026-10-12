# Excerpt of the original analysis code for the dataset "D_dependence" in data/.
# Fig 3 (b): 1/2 peak versus field at many displacement fields. Run with probe = "11_06" and
# filling = "half". The cell below does not write the keys fit_array_list, B_array_list and
# peak_fit_loc_err that the shared data holds, see README.md.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original discrete_v_B_dependence.py, lines 70-149 ---
#%%
data_class = load_multiple_datasets('D:/TD5/database/')
#%% 0.11
probe = '11_06'
step_size = 0.001
# filling = 'half'
# filling = 'one_third'
filling = 'two_thirds'
D_lims, n_lims = input_dict[probe][filling].values()

save_figs = False
run_bootstrap = False
asymptote_args = (False, False)#(True, True) # (show_asymptote_plot, allow_offset)

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
inspect_study_quality(results, probe, filling=filling, save_figs=save_figs)
plot_study_results(results,
                   probe,
                   filling=filling,
                   save_figs=save_figs,
                   asymptote_args=asymptote_args)

#%% extract data for paper plot - 1/2 coefficients D-dependence

if os.getcwd() != plot_path:
    os.chdir(plot_path)

n_post_correction = get_n_correction(probe) - n_correction
model_function = get_model(filling)

(D_list, 
a1_list, 
a2_list, 
a1_err_list, 
a2_err_list, 
model_list,
) = [], [], [], [], [], []

B_list_gen = np.linspace(0, results[next(iter(results.keys()))].B_set_list[-1])

for D_cut in results.keys():
    D_list.append(D_cut)
    a1_list.append(results[D_cut].MLE_params[0])
    a2_list.append(results[D_cut].MLE_params[1])
    a1_err_list.append(results[D_cut].MLE_error_autograd[0])
    a2_err_list.append(results[D_cut].MLE_error_autograd[1])
    model_list.append(model_function(B_list_gen, *results[D_cut].MLE_params) + n_post_correction)

color_list = generate_black_to_red(len(results.keys()))

plot_data = {
    'D_list': D_list, 
    'a1': a1_list, 
    'a2': a2_list, 
    'a1_err': a1_err_list, 
    'a2_err': a2_err_list,
    'B_list_gen': B_list_gen,
    'model_list': model_list,
    'color_list': color_list,
    'n_post_correction': n_post_correction,
}

with open('jar/D_dependence_paper_plot.pickle', 'wb') as f:
    pickle.dump(plot_data, f)

if os.getcwd() != base_path:
    os.chdir(base_path)

