# Excerpt of the original analysis code for the dataset "s5_temperature" in data/.
# S5: temperature dependence.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original SI_figures.py, cell "save data setup", lines 1927-1943 ---
import qcodes as qc
from qcodes.dataset import load_by_id


qc.config['user']['mainfolder'] = 'D://TD5'
scfg = qc.Station(config_file='D://TD5//config//Topo2DEG_config_T8.yaml')

database = 'Database_CD2_3'
qc.config['core']['db_location'] = 'D://TD5//database//' + database + '.db'
qc.initialise_database()
#qc.new_experiment("2023-10-10_tMoTe2.TD5-CD2", sample_name="TD5")

class Data:
    pass



# %% --- original SI_figures.py, cell "Temperature: save data", lines 1944-2091 ---

def n_to_T_multiprobe_Ru(id, dim):

    def R(I_array, V_arrays, dim):
        R_arrays = V_arrays / I_array
        # R_arrays = reshape_(R_arrays, dim)
        return R_arrays

    data = load_by_id(id).get_parameter_data()
    # Vb_list = data['Vb']['Vb']
    # Vt_list = data['Vt']['Vt']
    n_list = data['Ixx']['n_at_fixed_D']
    I = data['Ixx']['Ixx']
    T_set = data['Ixx']['temperature_ch8']
    T_meas = data['T_mc']['T_mc']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']

    # nn, DD = V_to_n_and_D(Vt_list, Vb_list, cbg, ctg, dim)
    V_arrays = np.array([Vxx_11_06, Vxx_19_20, Vxx_20_24, Vxx_06_05, Vxy_11_19, Vxy_06_20, Vxy_05_24])
    R_arrays = R(I, V_arrays, dim)
    
    return n_list, T_set, R_arrays, T_meas

def n_to_T_multiprobe(id, dim):

    def V_to_n_and_D(Vt, Vb, cbg, ctg, dim):
        nn = np.reshape(np.array([n(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)]), dim)
        DD = np.reshape(np.array([D(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)]), dim)
        return nn, DD

    def reshape_(R_arrays, dim):
        reshaped_arrays = []
        for R_array in R_arrays:
            reshaped_arrays.append(np.reshape(R_array, dim))
        return reshaped_arrays

    def R(I_array, V_arrays, dim):
        R_arrays = V_arrays / I_array
        # R_arrays = reshape_(R_arrays, dim)
        return R_arrays

    data = load_by_id(id).get_parameter_data()
    # Vb_list = data['Vb']['Vb']
    # Vt_list = data['Vt']['Vt']
    n_list = data['Ixx']['n_at_fixed_D']
    I = data['Ixx']['Ixx']
    # T_set = data['Ixx']['temperature_ch8']
    T_set = data['Ixx']['temperature_ch5']
    T_meas = data['T_mc']['T_mc']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']

    # nn, DD = V_to_n_and_D(Vt_list, Vb_list, cbg, ctg, dim)
    V_arrays = np.array([Vxx_11_06, Vxx_19_20, Vxx_20_24, Vxx_06_05, Vxy_11_19, Vxy_06_20, Vxy_05_24])
    R_arrays = R(I, V_arrays, dim)
    # T_arrays = reshape_([T_set, T_meas], dim)
    # n_arrays = reshape_([n_list], dim)
    
    return n_list, T_set, R_arrays, T_meas

# B-
ids = [405, 427, 482, 479, 503, 510] #[405, 422, 427, 482, 479, 503, 510]
dim = [[74, 201], [11, 201], [25, 201], [40, 201], [151, 201], [100, 201]] #[[74, 201], [21, 201], [11, 201], [25, 201], [40, 201], [151, 201], [100, 201]]

nn_0, T_set_list_0, R_list_0, T_meas_list_0 = n_to_T_multiprobe_Ru(ids[0], dim[0])
nn_1, T_set_list_1, R_list_1, T_meas_list_1 = n_to_T_multiprobe(ids[1], dim[1])
nn_2, T_set_list_2, R_list_2, T_meas_list_2 = n_to_T_multiprobe(ids[2], dim[2])
nn_3, T_set_list_3, R_list_3, T_meas_list_3 = n_to_T_multiprobe(ids[3], dim[3])
nn_4, T_set_list_4, R_list_4, T_meas_list_4 = n_to_T_multiprobe(ids[4], dim[4])
nn_5, T_set_list_5, R_list_5, T_meas_list_5 = n_to_T_multiprobe(ids[5], dim[5])

nn2 = nn_2[1:]
T_set_list2 = T_set_list_2[1:]
R_list2 = R_list_2[:, 1:]
T_meas_list2 = T_meas_list_2[1:]

nn4 = nn_4[1:]
T_set_list4 = T_set_list_4[1:]
R_list4 = R_list_4[:, 1:]
T_meas_list4 = T_meas_list_4[1:]

nn_list_comb_m = np.concatenate((nn_0, nn_1, nn2, nn_3, nn4, nn_5))
T_set_list_comb_m = np.concatenate((T_set_list_0, T_set_list_1, T_set_list2, T_set_list_3, T_set_list4, T_set_list_5))
R_list_comb_m = np.concatenate((R_list_0, R_list_1, R_list2, R_list_3, R_list4, R_list_5), axis=1)
T_meas_list_comb_m = np.concatenate((T_meas_list_0, T_meas_list_1, T_meas_list2, T_meas_list_3, T_meas_list4, T_meas_list_5))

[Rxx_11_06_m, Rxx_19_20_m, Rxx_20_24_m, Rxx_06_05_m, Rxy_11_19_m, Rxy_06_20_m, Rxy_05_24_m] = R_list_comb_m

# B+ 
ids = [416, 431, 472, 475, 523] #[416, 419, 431, 472, 475, 523]
dim = [[74, 201], [11, 201], [25, 201], [40, 201], [251, 201]] #[[74, 201], [25, 201], [11, 201], [25, 201], [40, 201], [251, 201]]

nn_0, T_set_list_0, R_list_0, T_meas_list_0 = n_to_T_multiprobe_Ru(ids[0], dim[0])
nn_1, T_set_list_1, R_list_1, T_meas_list_1 = n_to_T_multiprobe(ids[1], dim[1])
nn_2, T_set_list_2, R_list_2, T_meas_list_2 = n_to_T_multiprobe(ids[2], dim[2])
nn_3, T_set_list_3, R_list_3, T_meas_list_3 = n_to_T_multiprobe(ids[3], dim[3])
nn_4, T_set_list_4, R_list_4, T_meas_list_4 = n_to_T_multiprobe(ids[4], dim[4])

nn2 = nn_2[1:]
T_set_list2 = T_set_list_2[1:]
R_list2 = R_list_2[:, 1:]
T_meas_list2 = T_meas_list_2[1:]

nn4 = nn_4[1:]
T_set_list4 = T_set_list_4[1:]
R_list4 = R_list_4[:, 1:]
T_meas_list4 = T_meas_list_4[1:]

nn_list_comb_p = np.concatenate((nn_0, nn_1, nn2, nn_3, nn4))
T_set_list_comb_p = np.concatenate((T_set_list_0, T_set_list_1, T_set_list2, T_set_list_3, T_set_list4))
R_list_comb_p = np.concatenate((R_list_0, R_list_1, R_list2, R_list_3, R_list4), axis=1)
T_meas_list_comb_p = np.concatenate((T_meas_list_0, T_meas_list_1, T_meas_list2, T_meas_list_3, T_meas_list4))

[Rxx_11_06_p, Rxx_19_20_p, Rxx_20_24_p, Rxx_06_05_p, Rxy_11_19_p, Rxy_06_20_p, Rxy_05_24_p] = R_list_comb_p

Rxx_11_06_sym = (Rxx_11_06_p + Rxx_11_06_m) / 2
Rxy_06_20_anti = (Rxy_06_20_p - Rxy_06_20_m) / 2

temp_data = Data()

setattr(temp_data, f'nn_list_comb_p', nn_list_comb_p)
setattr(temp_data, f'T_set_list_comb_p', T_set_list_comb_p)
setattr(temp_data, f'R_list_comb_p', R_list_comb_p)
setattr(temp_data, f'T_meas_list_comb_p', T_meas_list_comb_p)
setattr(temp_data, f'nn_list_comb_m', nn_list_comb_m)
setattr(temp_data, f'T_set_list_comb_m', T_set_list_comb_m)
setattr(temp_data, f'R_list_comb_m', R_list_comb_m)
setattr(temp_data, f'T_meas_list_comb_m', T_meas_list_comb_m)
setattr(temp_data, f'Rxx_11_06_sym', Rxx_11_06_sym)
setattr(temp_data, f'Rxy_06_20_anti', Rxy_06_20_anti)

with open(base_path + 'jar//SI_temperature.pkl', 'wb') as f:
    pickle.dump({
        'temp_data': temp_data,
    }, f)

