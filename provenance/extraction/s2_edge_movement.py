# Excerpt of the original analysis code for the dataset "s2_edge_movement" in data/.
# S2: magnetic-field response of the resistance edge.
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



# %% --- original SI_figures.py, cell "D-B competition: save data", lines 2251-2275 ---

two_d_map = Data()
cuts = Data()

n_index = 0
data_2d = load_by_id(569).get_parameter_data()
two_d_map.d_at_fixed_n = data_2d['Ixx']['D_at_fixed_n'][:, n_index, :]
two_d_map.b_perp = data_2d['Ixx']['B_perp'][:, n_index, :]
res_2d = data_2d['Vxx_11_06']['Vxx_11_06'][:, n_index, :] / data_2d['Ixx']['Ixx'][:, n_index, :]
two_d_map.res_2d_sym = (res_2d + np.flip(res_2d, axis=0)) / 2

j = 0
for i in [10, 12, 14, 16, 18, 20]:
    setattr(cuts, f'cut_{j}_b_perp', two_d_map.b_perp[i][0])
    setattr(cuts, f'cut_{j}_d_at_fixed_n', two_d_map.d_at_fixed_n[i])
    setattr(cuts, f'cut_{j}_res_sym', two_d_map.res_2d_sym[i])
    j += 1

with open(base_path + 'jar//SI_edge_movement.pkl', 'wb') as f:
    pickle.dump({
        'two_d_map': two_d_map,
        'cuts': cuts
    }, f)

