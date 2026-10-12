# Excerpt of the original analysis code for the dataset "gg_map_fig2" in data/.
# Fig 2 (a, b): gate-gate maps at 0.2 T and 2 T.
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original discrete_v_B_dependence.py, cell "fig 2 data extract", lines 604-669 ---

path = 'Volumes/STORE N GO/TD5/database/'

database = 'Database_CD2_3'
qc.config['core']['db_location'] = path + database + '.db'
qc.initialise_database()

fig2_gg_map = Data()

# B=0.2T map

id1 = 223
dim = [141, 121]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_1, Rxx_19_20_1, Rxx_20_24_1, Rxx_06_05_1, Rxy_11_19_1, Rxy_06_20_1, Rxy_05_24_1] = V_top_bottom_multiprobe(id1, dim)
id2 = 549
dim = [141, 121]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_2, Rxx_19_20_2, Rxx_20_24_2, Rxx_06_05_2, Rxy_11_19_2, Rxy_06_20_2, Rxy_05_24_2] = V_top_bottom_multiprobe(id2, dim)
fig2_gg_map.Rxx_19_20_sym_200= (Rxx_19_20_1+Rxx_19_20_2)/2
fig2_gg_map.Rxx_11_06_sym_200= (Rxx_11_06_1+Rxx_11_06_2)/2
fig2_gg_map.Rxx_20_24_sym_200= (Rxx_20_24_1+Rxx_20_24_2)/2
fig2_gg_map.Rxx_06_05_sym_200= (Rxx_06_05_1+Rxx_06_05_2)/2
fig2_gg_map.Rxy_11_19_sym_200= (Rxy_11_19_1-Rxy_11_19_2)/2
fig2_gg_map.Rxy_06_20_sym_200= (Rxy_06_20_1-Rxy_06_20_2)/2
fig2_gg_map.Rxy_05_24_sym_200= (Rxy_05_24_1-Rxy_05_24_2)/2

# B=2T map

id1 = 232
dim = [141, 121]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_1, Rxx_19_20_1, Rxx_20_24_1, Rxx_06_05_1, Rxy_11_19_1, Rxy_06_20_1, Rxy_05_24_1] = V_top_bottom_multiprobe(id1, dim)
id2 = 541
dim = [141, 121]
Vb_list, Vt_list, nn, DD, [Rxx_11_06_2, Rxx_19_20_2, Rxx_20_24_2, Rxx_06_05_2, Rxy_11_19_2, Rxy_06_20_2, Rxy_05_24_2] = V_top_bottom_multiprobe(id2, dim)
fig2_gg_map.Rxx_19_20_sym_2 = (Rxx_19_20_1+Rxx_19_20_2)/2
fig2_gg_map.Rxx_11_06_sym_2 = (Rxx_11_06_1+Rxx_11_06_2)/2
fig2_gg_map.Rxx_20_24_sym_2 = (Rxx_20_24_1+Rxx_20_24_2)/2
fig2_gg_map.Rxx_06_05_sym_2 = (Rxx_06_05_1+Rxx_06_05_2)/2
fig2_gg_map.Rxy_11_19_sym_2 = (Rxy_11_19_1-Rxy_11_19_2)/2
fig2_gg_map.Rxy_06_20_sym_2 = (Rxy_06_20_1-Rxy_06_20_2)/2
fig2_gg_map.Rxy_05_24_sym_2 = (Rxy_05_24_1-Rxy_05_24_2)/2

fig2_gg_map.Vb_list = Vb_list
fig2_gg_map.Vt_list = Vt_list
fig2_gg_map.nn = nn
fig2_gg_map.DD = DD

if os.getcwd() != plot_path:
    os.chdir(plot_path)

with open('jar/fig2_gg_map.pickle', 'wb') as f:
    pickle.dump(fig2_gg_map, f)

os.chdir(base_path)

##########

# path = 'Volumes/STORE N GO/TD5/database/'

# database = 'Database_CD2_'
# qc.config['core']['db_location'] = path + database + '.db'
# qc.initialise_database()

# n vs. B map


