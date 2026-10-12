# Excerpt of the original analysis code for the dataset "s4_parallel_field" in data/.
# S4: parallel-field response.
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



# %% --- original SI_figures.py, cell "Bpar: save data", lines 2276-2327 ---

one_half_data = Data()
two_thirds_data = Data()

# v=-1/2
data_par_negative = load_by_id(263).get_parameter_data()
data_par_positive = load_by_id(279).get_parameter_data()

r_par_negative = data_par_negative['Vxx_11_06']['Vxx_11_06'] / data_par_negative['Ixx']['Ixx']
r_par_positive = data_par_positive['Vxx_11_06']['Vxx_11_06'] / data_par_positive['Ixx']['Ixx']
r_par_sym = (r_par_negative + r_par_positive) / 2

data_zero_negative = load_by_id(115).get_parameter_data()
data_zero_positive = load_by_id(85).get_parameter_data()

r_zero_negative = data_zero_negative['Vxx_11_06']['Vxx_11_06'] / data_zero_negative['Ixx']['Ixx']
r_zero_positive = data_zero_positive['Vxx_11_06']['Vxx_11_06'] / data_zero_positive['Ixx']['Ixx']
r_zero_sym = (r_zero_negative + r_zero_positive) / 2

one_half_data.par_d_at_fixed_n = data_par_negative['Ixx']['D_at_fixed_n']
one_half_data.r_par_sym = r_par_sym
one_half_data.zero_d_at_fixed_n = data_zero_negative['Ixx']['D_at_fixed_n']
one_half_data.r_zero_sym = r_zero_sym

# v=-2/3
data_par_negative = load_by_id(260).get_parameter_data()
data_par_positive = load_by_id(276).get_parameter_data()

r_par_negative = data_par_negative['Vxx_11_06']['Vxx_11_06'] / data_par_negative['Ixx']['Ixx']
r_par_positive = data_par_positive['Vxx_11_06']['Vxx_11_06'] / data_par_positive['Ixx']['Ixx']
r_par_sym = (r_par_negative + r_par_positive) / 2

data_zero_negative = load_by_id(104).get_parameter_data()
data_zero_positive = load_by_id(74).get_parameter_data()

r_zero_negative = data_zero_negative['Vxx_11_06']['Vxx_11_06'] / data_zero_negative['Ixx']['Ixx']
r_zero_positive = data_zero_positive['Vxx_11_06']['Vxx_11_06'] / data_zero_positive['Ixx']['Ixx']
r_zero_sym = (r_zero_negative + r_zero_positive) / 2

two_thirds_data.par_d_at_fixed_n = data_par_negative['Ixx']['D_at_fixed_n']
two_thirds_data.r_par_sym = r_par_sym
two_thirds_data.zero_d_at_fixed_n = data_zero_negative['Ixx']['D_at_fixed_n']
two_thirds_data.r_zero_sym = r_zero_sym

cwd = os.getcwd()
with open(base_path + 'jar//SI_B_par.pkl', 'wb') as f:
    pickle.dump({
        'one_half_data': one_half_data,
        'two_thirds_data': two_thirds_data
    }, f)

