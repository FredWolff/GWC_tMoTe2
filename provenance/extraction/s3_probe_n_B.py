# Excerpt of the original analysis code for the dataset "s3_probe_n_B" in data/.
# S3: n-B data of the other probe pairs.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original SI_figures.py, cell "save data setup", lines 1614-1630 ---
sys.path.append('C:/Users/frede/Documents/tMoTe2-analysis')
from functions import *
import pickle

plot_path = 'C:/Users/frede/Documents/tMoTe2-analysis/'

qc.config['user']['mainfolder'] = 'D:/TD5'

database = 'Database_CD2_'
qc.config['core']['db_location'] = 'D:/TD5/database/' + database + '.db'
qc.initialise_database()
qc.new_experiment("2023-10-10_tMoTe2.TD5-CD2", sample_name="TD5")

class Data:
    pass


# %% --- original SI_figures.py, cell "Probe: n-B: save data", lines 1861-1926 ---

def landau_polyprobe_R(id):

    def V_to_n_and_D(Vt, Vb, cbg, ctg):
        nn = np.array([n(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        DD = np.array([D(Vt_val, Vb_val, cbg, ctg) for Vt_val, Vb_val in zip(Vt, Vb)])
        return nn, DD

    def R(I_array, V_arrays):
        R_arrays = V_arrays / I_array
        return R_arrays

    data = load_by_id(id).get_parameter_data()
    # Vb_list = data['Vb']['Vb']
    # Vt_list = data['Vt']['Vt']
    nn = data['Ixx']['n_at_fixed_D']
    B_list = data['Ixx']['B_perp']
    I = data['Ixx']['Ixx']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']
    I_phase = data['Ixx_phase']['Ixx_phase']
    Vxx_11_06_phase = data['Vxx_11_06_phase']['Vxx_11_06_phase']
    Vxx_19_20_phase = data['Vxx_19_20_phase']['Vxx_19_20_phase']
    Vxx_20_24_phase = data['Vxx_20_24_phase']['Vxx_20_24_phase']
    Vxx_06_05_phase = data['Vxx_06_05_phase']['Vxx_06_05_phase']

    I_R = I / np.cos(I_phase * np.pi / 180)
    V_R_11_06 = Vxx_11_06 / np.cos(Vxx_11_06_phase * np.pi / 180)
    V_R_19_20 = Vxx_19_20 / np.cos(Vxx_19_20_phase * np.pi / 180)
    V_R_20_24 = Vxx_20_24 / np.cos(Vxx_20_24_phase * np.pi / 180)
    V_R_06_05 = Vxx_06_05 / np.cos(Vxx_06_05_phase * np.pi / 180)
 
    #R_arrays = R(I_R, np.array([Vxx_11_06, Vxy_11_19, Vxx_19_20, Vxy_06_20, Vxx_20_24, Vxy_05_24, Vxx_06_05]))
    #nn, DD = V_to_n_and_D(Vt_list, Vb_list, cbg, ctg)
    #reshape_arrays = [B_list, nn, DD, *R_arrays]
    # [B_list, nn, DD, Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05] = reshape_(reshape_arrays, dim)

    Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05 = V_R_11_06 / I_R, Vxy_11_19 / I, V_R_19_20 / I_R, Vxy_06_20 / I, V_R_20_24 / I_R, Vxy_05_24 / I, V_R_06_05 / I_R

    return B_list, nn, Rxx_11_06, Rxy_11_19, Rxx_19_20, Rxy_06_20, Rxx_20_24, Rxy_05_24, Rxx_06_05

B_list, nn, R_11_06, R_11_19, R_19_20, R_06_20, R_20_24, R_05_24, R_06_05 = landau_polyprobe_R(141)

probe_data = Data()

setattr(probe_data, 'B_perp', B_list)
setattr(probe_data, 'nn', nn)
setattr(probe_data, 'R_11_06_long', R_11_06)
setattr(probe_data, 'R_11_19_trans', R_11_19)
setattr(probe_data, 'R_19_20_long', R_19_20)
setattr(probe_data, 'R_06_20_trans', R_06_20)
setattr(probe_data, 'R_20_24_long', R_20_24)
setattr(probe_data, 'R_05_24_trans', R_05_24)
setattr(probe_data, 'R_06_05_long', R_06_05)

with open(base_path + 'jar//SI_probe_n_B.pkl', 'wb') as f:
    pickle.dump({
        'probe_data': probe_data,
    }, f)

