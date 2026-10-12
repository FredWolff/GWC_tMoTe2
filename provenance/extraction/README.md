# Extraction excerpts

Verbatim copies of the cells of the original analysis scripts that read the raw measurement
database and wrote each dataset in `data/`. Each file says which original file and lines it was
copied from.

They are documentation, not runnable scripts:

- They need the raw qcodes database and the instrument configuration, which are not shared.
- They depend on `analysis_functions.py`, a verbatim copy of the helper functions of the original
  `functions.py` that they (transitively) call. The original scripts start with `from functions import *`.
- They also use a few names that the original scripts define at the top of the file: `base_path` and
  `plot_path` (where the original pickles were written), `pickle`, and in some cases results of
  earlier cells (`data_class`, `corr_vec`).
- Some cells also draw plots that are not part of the paper or SI.
