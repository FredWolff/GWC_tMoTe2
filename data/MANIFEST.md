# Data manifest

Written by `provenance/convert_pickles.py`. Each file was verified field by field
against its source pickle after conversion.

| Dataset | Original pickle | Fields kept | Used by |
|---|---|---|---|
| `gate_corrections` | `probe_dependence_half_paper_plot.pickle` | `D_correction` | all (shared gate correction) |
| `gg_map_fig1` | `fig1_gg_map.pickle` | `nn`, `DD`, `Rxx_11_06_sym_200`, `Rxy_11_19_sym_200` | Fig 1, S1, S6(d) |
| `gg_map_fig2` | `fig2_gg_map.pickle` | `nn`, `DD`, `Rxx_11_06_sym_200`, `Rxx_11_06_sym_2` | Fig 2 (a, b) |
| `B_dependence_one_third` | `B_dependence_one_third_paper_plot_small_err.pickle` | `B_array`, `fit_array`, `peak_loc_err`, `y_0`, `fit_params`, `model_function`, `n_post_correction` | Fig 3 (a) |
| `B_dependence_half` | `B_dependence_half_paper_plot_small_err.pickle` | `B_array`, `fit_array`, `peak_loc_err`, `y_0`, `fit_params`, `model_function`, `n_post_correction` | Fig 3 (a) |
| `B_dependence_two_thirds` | `B_dependence_two_thirds_paper_plot_small_err.pickle` | `B_array`, `fit_array`, `peak_loc_err`, `y_0`, `fit_params`, `model_function`, `n_post_correction` | Fig 3 (a) |
| `fit_expansion` | `SI_peaks_expans.pkl` | `expans/one_third_75` | Fig 3 (a): extra fitted point at 0.75 T [peak position, uncertainty] |
| `D_dependence` | `D_dependence_paper_plot.pickle` | `D_list`, `B_list_gen`, `model_list`, `fit_array_list`, `B_array_list`, `peak_fit_loc_err` | Fig 3 (b) |
| `probe_dependence_half` | `probe_dependence_half_paper_plot.pickle` | `D_correction`, `D_array_20_06`, `R_array_20_06`, `D_array_06_11`, `R_array_06_11`, `D_array_19_20`, `R_array_19_20` | Fig 3 (c) |
| `edge_movement` | `SI_edge_movement.pkl` | `two_d_map`, `cuts` | S2 |
| `probe_n_B` | `SI_probe_n_B.pkl` | `probe_data/B_perp`, `probe_data/nn`, `probe_data/R_11_06_long`, `probe_data/R_19_20_long`, `probe_data/R_20_24_long`, `probe_data/R_06_05_long` | S3 |
| `parallel_field` | `SI_B_par.pkl` | `one_half_data`, `two_thirds_data` | S4 |
| `temperature` | `SI_temperature.pkl` | `temp_data/nn_list_comb_p`, `temp_data/T_set_list_comb_p`, `temp_data/Rxx_11_06_sym`, `temp_data/Rxy_06_20_anti` | S5 |
| `topology` | `SI_topology.pkl` | `topology_11_06_20/Rxy_06_20_anti_landau_full_n`, `topology_11_06_20/nn_sym_landau_full_n`, `topology_11_06_20/Bperp_sym_landau_full_n`, `topology_11_06_20/nn_B_finite_D` (first displacement-field slice), `topology_11_06_20/Bperp_B_finite_D` (first displacement-field slice), `topology_11_06_20/Rxy_06_20_anti_B_finite_D` (first displacement-field slice), `topology_11_06_20/nn`, `topology_11_06_20/Rxx_11_06`, `topology_11_06_20/Rxy_06_20` | S6 (a, b, c); panel (d) uses `gg_map_fig1` |
| `n_B_map` | `B_n_data.pickle` | `nn`, `DD`, `Bperp`, `Rxx_11_06` | Fig 2 (c, d), Fig 3 inset |
