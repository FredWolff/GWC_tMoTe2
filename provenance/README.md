# Provenance

How the compressed data in `data/` was derived. **Nothing in this folder can be run without the raw
measurement database and the original analysis code, neither of which is shared.** It is here so that
questions of the form "how was this made?" can be answered from the code.

## Contents

| | |
|---|---|
| `convert_pickles.py` | The converter. Turns the original pickles into the `.npz` / `.json` files of `data/` and keeps only the fields the shared figures read. Reads the pickles with stand-in classes, so it does not need the original code; it checks every file it writes against its source. `data/MANIFEST.md` is its output. |
| `extraction/` | Verbatim excerpts of the original analysis code that read the raw database and produced each dataset, one file per dataset (see `extraction/README.md`). |
| `record_golden.py` | Runs the original plotting cells unchanged and records what they draw. The result is in `tests/golden/` and is what `tests/` compares the shared figures to. |

## Where each dataset comes from

| `data/` file | Original pickle | Extraction excerpt |
|---|---|---|
| `gg_map_fig1` | `fig1_gg_map.pickle` | `gg_map_fig1.py` |
| `gg_map_fig2` | `fig2_gg_map.pickle` | `gg_map_fig2.py` |
| `n_B_map` | `B_n_data.pickle` | `n_B_map.py` |
| `B_dependence_*` | `B_dependence_*_paper_plot_small_err.pickle` | `B_dependence.py` (see note 1) |
| `D_dependence` | `D_dependence_paper_plot.pickle` | `D_dependence.py` (see note 2) |
| `probe_dependence_half`, `gate_corrections` | `probe_dependence_half_paper_plot.pickle` | `probe_dependence_half.py` |
| `fit_expansion` | `SI_peaks_expans.pkl` | `fit_expansion.py` |
| `probe_n_B` | `SI_probe_n_B.pkl` | `s3_probe_n_B.py` |
| `edge_movement` | `SI_edge_movement.pkl` | `s2_edge_movement.py` |
| `parallel_field` | `SI_B_par.pkl` | `s4_parallel_field.py` |
| `temperature` | `SI_temperature.pkl` | `s5_temperature.py` |
| `topology` | `SI_topology.pkl` | `s6_topology.py` |

## Notes and gaps

1. **`B_dependence_*`.** The shared files come from the "small err" variant of the B-dependence
   pickles. The extraction cell that wrote them is not in the repository; the cell in
   `extraction/B_dependence.py` wrote the plain `B_dependence_*_paper_plot.pickle` files. The two sets hold
   the same measured peak positions, uncertainties and `y_0`; they differ only in the stored `fit_params`.
2. **`D_dependence`.** The shared file holds `fit_array_list`, `B_array_list` and `peak_fit_loc_err`, which
   Fig. 3(b) needs. The extraction cell in `extraction/D_dependence.py` does not write them (the version of
   the file in the repository, which does not have them, cannot draw Fig. 3(b)). The code that added them
   was not saved with the analysis.
3. **Fig. 3(a)** adds one extra peak position, at 0.75 T for 1/3, from a Lorentzian fit in
   `extraction/fit_expansion.py` (a field where the automatic fit was difficult), and refits the constant
   models of 1/3 and 2/3. The 2/3 trace uses only the points up to 1 T. The refits are done in
   `figures/fig3.py`.
4. **`topology`** keeps only the first displacement-field slice of the three `*_B_finite_D` arrays,
   the only slice Fig. S6 uses.
5. **Plot-time choices in the original code that the shared code makes explicit.** The original plotting
   cells depend on variables left over from earlier cells. Where that matters the shared code uses the value
   that the exported figures show: for example the filling-factor axis of Fig. 1 uses the
   `11_06` density conversion, and the colour scale of the S1 map is (0.01, 50).
6. **Fig. S3** is arranged (a) top left, (b) top right, (c) bottom right, (d) bottom left. The original code
   has (b) at the bottom left, (c) at the top right and the fourth panel at the bottom right, labelled "(e)".
   Its colour-bar labels read "R" with the probe pair as subscript instead of "|Z|" with it. `record_golden.py` applies the same
   changes to the original cell (`AMENDMENTS`).

7. **Fig. S2(b)** draws its cuts from black (0 T) to green (RGB 0, 197, 91; 1 T) in equal steps,
   instead of the default colour cycle of the original code. `record_golden.py` applies the same colours
   to the original cell (`AMENDMENTS`).

8. **Fig. 2(d)** (Rxx against field along two cuts of panel (c), at the densities marked at the top of (c))
   is not made by any code in the original repository. It was recreated from the data of panel (c)
   (`n_B_map`): the 2/3 cut is at the density where the 2/3 peak is highest at 0 T, the 1/3 cut where the
   1/3 peak is highest at 2.25 T (each searched within 0.35e12 cm^-2 of its filling factor; the result does
   not change with a window of 0.2e12 or 0.5e12). The layout of (c) and (d) and the colours follow a
   screenshot of the published figure. The rule under the legend title is drawn by
   `tmote2/style.add_legend_rule`. `record_golden.py` adds the panel to a copy of the original Fig. 2 cell
   (`AMENDMENTS`).

## How the migration was checked

- Every data file was compared field by field with its source pickle when it was written.
- `tests/` compares what each shared figure draws (data, limits, labels, ticks, colormaps) with what the
  original plotting code drew, which `record_golden.py` recorded. For Fig. 3 the recorder first applies the
  change that the original code in the repository lacks (the 2/3 trace described in note 3; see
  `AMENDMENTS` in `record_golden.py`), so the recorded figure is the final one.
- Each shared figure was also rendered and compared pixel by pixel with the PDF that the original code
  exported. Fig. 1 and S1-S5 are identical. S6 differs only in the label of its last colour bar, which the
  original code changed after that export from `R_xx` to `R_xy`. Fig. 2 was identical to the rasterised
  export and Fig. 3 to the export of Feb 21 before they were changed as in notes 8 and 3.
