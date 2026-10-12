# Excerpt of the original analysis code for the dataset "s6_topology" in data/.
# S6: topology data (panel (d) uses the Fig 1 gate-gate map).
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



# %% --- original SI_figures.py, cell "Topology: save data", lines 2092-2250 ---

def n_sweep_complete(id):

    def V_to_n_and_D(Vt, Vb, cbg, ctg):
        nn = np.array([n(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        DD = np.array([D(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        return nn, DD

    def R(I_array, V_arrays):
        R_arrays = V_arrays / I_array
        return R_arrays
  
    data = load_by_id(id).get_parameter_data()
    Vb_list = data['Vb']['Vb']
    Vt_list = data['Vt']['Vt']
    I = data['Ixx']['Ixx']
    I_phase = data['Ixx_phase']['Ixx_phase']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']

    R_arrays = R(I, np.array([Vxx_11_06, Vxy_11_19, Vxx_19_20, Vxy_06_20, Vxx_20_24, Vxy_05_24, Vxx_06_05]))
    nn, DD = V_to_n_and_D(Vt_list, Vb_list, cbg, ctg)
    return nn, DD, I_phase, R_arrays

def landau_polyprobe(id, dim):

    if id == 242:
        def reshape_(R_arrays, dim):
            reshaped_arrays = []
            for R_array in R_arrays:
                reshaped_arrays.append(np.reshape(R_array[:-100], dim))
            return reshaped_arrays
    else:
        def reshape_(R_arrays, dim):
            reshaped_arrays = []
            for R_array in R_arrays:
                reshaped_arrays.append(np.reshape(R_array, dim))
            return reshaped_arrays

    def V_to_n_and_D(Vt, Vb, cbg, ctg):
        nn = np.array([n(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        DD = np.array([D(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        return nn, DD

    def R(I_array, V_arrays):
        R_arrays = V_arrays / I_array
        return R_arrays

    data = load_by_id(id).get_parameter_data()
    Vb_list = data['Vb']['Vb']
    Vt_list = data['Vt']['Vt']
    B_list = data['Ixx']['B_perp']
    I = data['Ixx']['Ixx']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']

    R_arrays = R(I, np.array([Vxx_11_06, Vxy_11_19, Vxx_19_20, Vxy_06_20, Vxx_20_24, Vxy_05_24, Vxx_06_05]))
    nn, DD = V_to_n_and_D(Vt_list, Vb_list, cbg, ctg)
    reshape_arrays = [B_list, nn, DD, *R_arrays]
    [B_list, nn, DD, Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05] = reshape_(reshape_arrays, dim)

    return B_list, nn, DD, Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05

topology_11_06_20 = Data()
topology_19_20_11 = Data()

######### (a) #########

id = 329
dim = (81, 181)
Bperp, nn, DD, Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05 = landau_polyprobe(id, dim)

Rxx_11_06_sym = (Rxx_11_06 + np.flip(Rxx_11_06, axis=0)) / 2
Rxy_06_20_anti = (Rxy_06_20 - np.flip(Rxy_06_20, axis=0)) / 2

setattr(topology_11_06_20, f'Rxx_11_06_sym_landau_full_n', Rxx_11_06_sym)
setattr(topology_11_06_20, f'Rxy_06_20_anti_landau_full_n', Rxy_06_20_anti)
setattr(topology_11_06_20, f'nn_sym_landau_full_n', nn)
setattr(topology_11_06_20, f'Bperp_sym_landau_full_n', Bperp)
setattr(topology_11_06_20, f'DD_sym_landau_full_n', DD)

######### (c) #########

ids = [372, 368]

for i in range(len(ids)):
    nn, DD, I_phase, [Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05] = n_sweep_complete(ids[i])
    if i == 0:
        Rxx_arrays = np.array([Rxx_11_06, Rxx_19_20, Rxx_20_24, Rxx_06_05])
        Rxy_arrays = np.array([Rxy_11_19, Rxy_06_20, Rxy_05_24])
    else:
        Rxx_arrays += np.array([Rxx_11_06, Rxx_19_20, Rxx_20_24, Rxx_06_05])
        Rxy_arrays -= np.array([Rxy_11_19, Rxy_06_20, Rxy_05_24])

[Rxx_11_06, Rxx_19_20, Rxx_20_24, Rxx_06_05] = Rxx_arrays/2
[Rxy_11_19, Rxy_06_20, Rxy_05_24] = Rxy_arrays/2

setattr(topology_11_06_20, f'Rxx_11_06', Rxx_11_06)
setattr(topology_11_06_20, f'Rxy_06_20', Rxy_06_20)
setattr(topology_19_20_11, f'Rxx_19_20', Rxx_19_20)
setattr(topology_19_20_11, f'Rxy_11_19', Rxy_11_19)
setattr(topology_11_06_20, f'nn', nn)
setattr(topology_19_20_11, f'nn', nn)

######## (b) & (d) ########

id1 = 241
id2 = 242
id3 = 243
id4 = 244
ids = [id1, id2, id3, id4]
dim1 = (35, 8, 151)
dim2 = (76, 8, 151)
dim3 = (5, 8, 151)
dim4 = (35, 8, 151)
Bperp1, nn1, DD1, Rxx_11_06_1, Rxy_11_19_1, Rxx_19_20_1, Rxy_06_20_1, Rxx_20_24_1, Rxy_05_24_1, Rxx_06_05_1 = landau_polyprobe(id1, dim1)
Bperp2, nn2, DD2, Rxx_11_06_2, Rxy_11_19_2, Rxx_19_20_2, Rxy_06_20_2, Rxx_20_24_2, Rxy_05_24_2, Rxx_06_05_2 = landau_polyprobe(id2, dim2)
Bperp3, nn3, DD3, Rxx_11_06_3, Rxy_11_19_3, Rxx_19_20_3, Rxy_06_20_3, Rxx_20_24_3, Rxy_05_24_3, Rxx_06_05_3 = landau_polyprobe(id3, dim3)
Bperp4, nn4, DD4, Rxx_11_06_4, Rxy_11_19_4, Rxx_19_20_4, Rxy_06_20_4, Rxx_20_24_4, Rxy_05_24_4, Rxx_06_05_4 = landau_polyprobe(id4, dim4)

nn = np.concatenate((nn1, nn2, nn3, nn4))
Bperp = np.concatenate((Bperp1, Bperp2, Bperp3, Bperp4))
DD = np.concatenate((DD1, DD2, DD3, DD4))
Rxx_11_06 = np.concatenate((Rxx_11_06_1, Rxx_11_06_2, Rxx_11_06_3, Rxx_11_06_4))
Rxx_19_20 = np.concatenate((Rxx_19_20_1, Rxx_19_20_2, Rxx_19_20_3, Rxx_19_20_4))
Rxx_20_24 = np.concatenate((Rxx_20_24_1, Rxx_20_24_2, Rxx_20_24_3, Rxx_20_24_4))
Rxx_06_05 = np.concatenate((Rxx_06_05_1, Rxx_06_05_2, Rxx_06_05_3, Rxx_06_05_4))
Rxy_11_19 = np.concatenate((Rxy_11_19_1, Rxy_11_19_2, Rxy_11_19_3, Rxy_11_19_4))
Rxy_06_20 = np.concatenate((Rxy_06_20_1, Rxy_06_20_2, Rxy_06_20_3, Rxy_06_20_4))
Rxy_05_24 = np.concatenate((Rxy_05_24_1, Rxy_05_24_2, Rxy_05_24_3, Rxy_05_24_4))

Rxx_11_06_sym = (Rxx_11_06 + np.flip(Rxx_11_06, axis=0)) / 2
Rxy_06_20_anti = (Rxy_06_20 - np.flip(Rxy_06_20, axis=0)) / 2

setattr(topology_11_06_20, f'Rxx_11_06_sym_B_finite_D', Rxx_11_06_sym)
setattr(topology_11_06_20, f'Rxy_06_20_anti_B_finite_D', Rxy_06_20_anti)
setattr(topology_11_06_20, f'nn_B_finite_D', nn)
setattr(topology_11_06_20, f'Bperp_B_finite_D', Bperp)
setattr(topology_11_06_20, f'DD_B_finite_D', DD)

######## dump ########

with open(base_path + 'jar//SI_topology.pkl', 'wb') as f:
    pickle.dump({
        'topology_11_06_20': topology_11_06_20,
        'topology_19_20_11': topology_19_20_11
    }, f)

