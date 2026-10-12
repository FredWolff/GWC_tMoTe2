# Excerpt of the original analysis code for the dataset "probe_dependence_half" in data/.
# Fig 3 (c): resistance at 1/2 filling versus D for three probe pairs.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original Landau_fan_model_comparison.py, lines 1234-1300 ---
# %% extract data for paper plot - directionality of half

# n = 2.51e12
#V_20_06 - #2545: (I+; B+). 2547: (I-; B+). #2593: (I+; B-). #2595: (I-; B-)
#V_06_11 - #2363: (I+, B+). 2365: (I-, B+). #2411: (I+, B-). #2413: (I-, B-)
#V_19_20 - #2181: (I+, B+). 2183: (I-, B+). #2229: (I+, B-). #2231: (I-, B-)

V_20_06_indices = [2545, 2547, 2593, 2595]
V_06_11_indices = [2363, 2365, 2411, 2413]
V_19_20_indices = [2181, 2183, 2229, 2231]

def cal_long_R(
        V_lists: list[NDArray[np.float64]],
        I_lists: list[NDArray[np.float64]]
) -> NDArray[np.float64]:
    
    V_1, V_2, V_3, V_4 = V_lists
    I_1, I_2, I_3, I_4 = I_lists

    return (V_1 - V_2 + V_3 - V_4) / (I_1 - I_2 + I_3 - I_4)

def get_vdp_data(id_list: list[int]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:

    V_lists = []
    I_lists = []
    for id in id_list:
        data = load_by_id(id).get_parameter_data()
        D_array = data['dmm_dc']['D_at_fixed_n']
        V_lists.append(data['dmm_dc']['dmm_dc'])
        I_lists.append(data['dmm3_dc']['dmm3_dc'])

    R_array = cal_long_R(V_lists, I_lists)

    return D_array, R_array

D_array_20_06, R_array_20_06 = get_vdp_data(V_20_06_indices)
D_array_06_11, R_array_06_11 = get_vdp_data(V_06_11_indices)
D_array_19_20, R_array_19_20 = get_vdp_data(V_19_20_indices)

plot_path = '/Volumes/STORE N GO/analysis_folder/peak_movement/tMoTe2-analysis/'
if os.getcwd() != plot_path:
    os.chdir(plot_path)

D_correction = -0.015

plot_data = {
    'D_correction': D_correction,
    'D_array_20_06': D_array_20_06,
    'R_array_20_06': R_array_20_06,
    'D_array_06_11': D_array_06_11,
    'R_array_06_11': R_array_06_11,
    'D_array_19_20': D_array_19_20,
    'R_array_19_20': R_array_19_20,
}

with open(f'jar/probe_dependence_half_paper_plot.pickle', 'wb') as f:
    pickle.dump(plot_data, f)

plt.title('1/2, n_uncorr = -2.51e12')
plt.plot(D_array_20_06 - D_correction, R_array_20_06 / R_Q, label='20_06')
plt.plot(D_array_06_11 - D_correction, R_array_06_11 / R_Q, label='06_11')
plt.plot(D_array_19_20 - D_correction, R_array_19_20 / R_Q, label='19_20')
plt.xlabel('D/$\epsilon_{0}$ [V/nm]')
plt.ylabel('R$_{xx}$ [h/e$^2$]')
plt.legend()

# plt.xlim(-0.13, 0.13)
