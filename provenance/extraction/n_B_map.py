# Excerpt of the original analysis code for the dataset "n_B_map" in data/.
# Fig 2 (c) and Fig 3 inset: n-B map at fixed D (run 141).
#
# Verbatim copy, not meant to be run on its own: it needs the raw measurement database
# and the names defined by analysis_functions.py (the original code does
# `from functions import *`) as well as state from the cells before it in the original file.

# %% --- original Landau_fan_model_comparison.py, lines 184-266 ---
def landau_multiprobe(id, dim):

    def reshape_(R_arrays, dim):
        reshaped_arrays = []
        for R_array in R_arrays:
            reshaped_arrays.append(np.reshape(R_array, dim))
        return R_arrays

    def R(I_array, V_arrays, dim):
        R_arrays = V_arrays / I_array
        R_arrays = reshape_(R_arrays, dim)
        return R_arrays

    data = load_by_id(id).get_parameter_data()
    n_list = data['Ixx']['n_at_fixed_D']
    D_list = np.ones_like(n_list) * 0.12
    I = data['Ixx']['Ixx']
    B_array = data['Ixx']['B_perp']
    Vxx_11_06 = data['Vxx_11_06']['Vxx_11_06']
    Vxy_11_19 = data['Vxy_11_19']['Vxy_11_19']
    Vxx_19_20 = data['Vxx_19_20']['Vxx_19_20']
    Vxy_06_20 = data['Vxy_06_20']['Vxy_06_20']
    Vxx_20_24 = data['Vxx_20_24']['Vxx_20_24']
    Vxy_05_24 = data['Vxy_05_24']['Vxy_05_24']
    Vxx_06_05 = data['Vxx_06_05']['Vxx_06_05']

    V_arrays = np.array([Vxx_11_06, Vxx_19_20, Vxx_20_24, Vxx_06_05, Vxy_11_19, Vxy_06_20, Vxy_05_24])
    R_arrays = R(I, V_arrays, dim)
    B_array, n_list, D_list = reshape_([B_array, n_list, D_list], dim)
    
    return B_array, n_list, D_list, R_arrays

def anti_sym(array):
    N = len(array)
    if N % 2 == 0:
        return (array[:N//2]  - np.flipud(array[N//2:]))/2
    else:
        new_array = (array[:N//2] - np.flipud(array[N//2+1:]))/2
        return np.concatenate((new_array, np.array([array[N//2]])))
    
def sym(array):
    N = len(array)
    if N % 2 == 0:
        return (array[:N//2] + np.flipud(array[N//2:]))/2
    else:
        new_array = (array[:N//2] + np.flipud(array[N//2+1:]))/2
        return np.concatenate((new_array, np.array([array[N//2]])))

id = 141
dim = [91, 301]
Bperp, nn, DD, R_arrays = landau_multiprobe(id, dim)

Data_class = Data()

Data_class.Bperp = anti_sym(Bperp)
Data_class.nn = sym(nn)
Data_class.DD = sym(DD)

resistance_string = ['Rxx_11_06', 
                     'Rxx_19_20', 
                     'Rxx_20_24', 
                     'Rxx_06_05', 
                     'Rxy_11_19', 
                     'Rxy_06_20', 
                     'Rxy_05_24']

for resistance_list in range(len(resistance_string)):
    attr_name = resistance_string[resistance_list]
    if 'Rxx' in attr_name:
        attr_val = sym(R_arrays[resistance_list])
    else:
        attr_val = anti_sym(R_arrays[resistance_list])
    setattr(Data_class, attr_name, attr_val)

def get_cut(Data_class: Data, attr_name: str) -> NDArray[np.float64]:
    N = len(Data_class.Bperp)
    full_array = getattr(Data_class, attr_name)
    for i in range(N):
        yield full_array[i]

# for cut in get_cut(Data_class, 'Rxx_11_06'):
#     plt.plot(Data_class.nn[0], cut)


# %% --- original Landau_fan_model_comparison.py, cell "data extract - B vs n", lines 267-273 ---
if os.getcwd() != plot_path:
    os.chdir(plot_path)      

with open('jar/B_n_data.pickle', 'wb') as f:
    B_n_data = pickle.dump(Data_class, f)

