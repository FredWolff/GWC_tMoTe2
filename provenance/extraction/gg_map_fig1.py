# Excerpt of the original analysis code for the dataset "gg_map_fig1" in data/.
# Fig 1, S1, S6(d): gate-gate map at 0.02 T (used fields: nn, DD, Rxx_11_06_sym_200, Rxy_11_19_sym_200).
# The 1D "g_scan" part of the cell is not used by any shared figure.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original discrete_v_B_dependence.py, cell "fig 1 data extract", lines 670-741 ---
    
if os.getcwd() != base_path:
    os.chdir(base_path)

path = 'Volumes/STORE N GO/TD5/database/'

database = 'Database_CD2_3'
qc.config['core']['db_location'] = path + database + '.db'
qc.initialise_database()

fig1_gg_map = Data()

# B=0.02T map

id1 = 532
dim = [121, 91]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_1, Rxx_19_20_1, Rxx_20_24_1, Rxx_06_05_1, Rxy_11_19_1, Rxy_06_20_1, Rxy_05_24_1] = V_top_bottom_multiprobe(id1, dim)
id2 = 535
dim = [121, 91]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_2, Rxx_19_20_2, Rxx_20_24_2, Rxx_06_05_2, Rxy_11_19_2, Rxy_06_20_2, Rxy_05_24_2] = V_top_bottom_multiprobe(id2, dim)
fig1_gg_map.Rxx_19_20_sym_200= (Rxx_19_20_1+Rxx_19_20_2)/2
fig1_gg_map.Rxx_11_06_sym_200= (Rxx_11_06_1+Rxx_11_06_2)/2
fig1_gg_map.Rxx_20_24_sym_200= (Rxx_20_24_1+Rxx_20_24_2)/2
fig1_gg_map.Rxx_06_05_sym_200= (Rxx_06_05_1+Rxx_06_05_2)/2
fig1_gg_map.Rxy_11_19_sym_200= (Rxy_11_19_1-Rxy_11_19_2)/2
fig1_gg_map.Rxy_06_20_sym_200= (Rxy_06_20_1-Rxy_06_20_2)/2
fig1_gg_map.Rxy_05_24_sym_200= (Rxy_05_24_1-Rxy_05_24_2)/2

fig1_gg_map.Vb_list = Vb_list
fig1_gg_map.Vt_list = Vt_list
fig1_gg_map.nn = nn
fig1_gg_map.DD = DD

# 1D scans

fig1_g_scan = Data()

ids = [372, 368]
Rxy_arrays = []
Rxx_arrays = []
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

fig1_g_scan.Rxx_11_06 = Rxx_11_06
fig1_g_scan.Rxx_19_20 = Rxx_19_20
fig1_g_scan.Rxx_20_24 = Rxx_20_24
fig1_g_scan.Rxx_06_05 = Rxx_06_05
fig1_g_scan.Rxy_11_19 = Rxy_11_19
fig1_g_scan.Rxy_06_20 = Rxy_06_20
fig1_g_scan.Rxy_05_24 = Rxy_05_24
fig1_g_scan.nn = nn
fig1_g_scan.DD = DD

os.chdir(plot_path)

with open('jar/fig1_gg_map.pickle', 'wb') as f:
    pickle.dump(fig1_gg_map, f)

with open('jar/fig1_g_scan.pickle', 'wb') as f:
    pickle.dump(fig1_g_scan, f)

os.chdir(base_path)
