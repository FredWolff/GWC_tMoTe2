# Data and plotting code for arXiv:2610.02493v1

This folder holds the compressed data and the plotting code for the figures of
[arXiv:2610.02493v1](https://arxiv.org/abs/2610.02493v1): the main-text Figs. 1-3 and the
supplementary Figs. S1-S6. The paper reports the magnetic-field (B) and displacement-field (D)
dependence of the presumed charge-density-wave states at hole filling factors 1/3, 1/2 and 2/3
in twisted MoTe2.

The figures are built from the files in `data/` alone. The raw measurement database is not
included; `provenance/` documents how the data files were derived from it.

## Reproducing the figures

```
pip install -r requirements.txt
python make_figures.py              # all figures, written to output/ as PDF
python make_figures.py fig3 s6      # selected figures
python figures/fig3.py              # or run one figure script directly
python -m unittest discover tests   # check that every figure builds and plots the expected data
```

| Figure | Script | Shows |
|---|---|---|
| Fig. 1 | `figures/fig1.py` | gate-gate maps of Rxx (log scale) and Rxy in (n, D), with a filling-factor axis |
| Fig. 2 | `figures/fig2.py` | Rxx maps at 0.2 T and 2 T (a, b); n-B map at fixed D (c); cuts of (c) at fixed density against field (d) |
| Fig. 3 | `figures/fig3.py` | field dependence of the peak positions with fits and an n-B inset (a); D dependence of the 1/2 peak (b); probe dependence (c) |
| Fig. S1 | `figures/s1.py` | conversion between gate voltages and (n, D) |
| Fig. S2 | `figures/s2.py` | magnetic-field response of the resistance edge |
| Fig. S3 | `figures/s3.py` | n-B maps of the other probe pairs |
| Fig. S4 | `figures/s4.py` | response to a parallel magnetic field |
| Fig. S5 | `figures/s5.py` | temperature dependence |
| Fig. S6 | `figures/s6.py` | topology: Hall resistance in the n-B plane, cuts and the Rxy map (the fitted slopes are printed) |

The figure numbers are those of the paper. In the original analysis code, Fig. 3 is called "Fig. 4".

Colour conventions: Rxx is drawn with `inferno` and Rxy with `PuOr`, i.e. orange for negative and
purple for positive Rxy. Fonts are Arial where installed and DejaVu Sans otherwise.

## Layout

```
data/          compressed data: .npz (arrays) and .json (numbers, strings); MANIFEST.md lists
               every file, the fields it holds and the figures that use it
tmote2/        helper modules: loading data (io), gate conversions (physics), shared style
               (style), peak-position models and the fits of Fig. S6 (fitting)
figures/       one script per figure; each has build() -> {name: figure} and save()
tests/         one test per figure, comparing what is plotted with values recorded from the
               original analysis code
provenance/    how the data files were made (not runnable without the raw database)
output/        generated PDFs
```

## Conventions

- `n` is the carrier density in cm^-2 (negative for holes), `D/epsilon_0` the displacement field in V/nm.
- Probe pairs are named by their contacts, e.g. `11_06`. All figures use the corrections of probe `11_06`
  unless stated otherwise (`tmote2/physics.py`).
- Resistances are divided by the resistance quantum h/e^2 for plotting.

## License

MIT, see `LICENSE`.
