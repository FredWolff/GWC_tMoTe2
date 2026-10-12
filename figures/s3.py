"""Fig. S3: n-B maps measured with the other probe pairs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    n_correction = physics.get_corrections()[0]
    probe_data = io.load('probe_n_B').probe_data

    fig, ax = plt.subplots(2, 2, figsize=(style.FIG_WIDTH, 10))

    nn = np.array(probe_data.nn) + n_correction
    B_perp = probe_data.B_perp

    def symmetrised(R):
        return (R[::-1] + R) / 2

    maps = [  # (axes, resistance, probe pair), clockwise from the top left
        (ax[0, 0], probe_data.R_11_06_long, '11-06'),
        (ax[0, 1], probe_data.R_19_20_long, '19-20'),
        (ax[1, 1], probe_data.R_20_24_long, '20-24'),
        (ax[1, 0], probe_data.R_06_05_long, '06-05'),
    ]
    for axes, R, probe_pair in maps:
        image = axes.pcolormesh(
            1e-12 * nn, -B_perp, symmetrised(R) / physics.R_Q,
            norm=mcolors.LogNorm(vmin=1e-1, vmax=1e2),
            cmap=style.Rxx_cmap,
            rasterized=True,
        )
        axes.set_ylabel(r'$\mu_0 H$ (T)')
        axes.set_xlabel(r'$n$ ($10^{12}$ cm$^{-2}$)')
        fig.colorbar(image, ax=axes, label=rf'$R_{{{probe_pair}}}$ (h/e$^2$)')

    fig.tight_layout()

    labels = ['(a)', '(b)', '(c)', '(d)']
    for axes, label in zip([ax[0, 0], ax[0, 1], ax[1, 1], ax[1, 0]], labels):
        axes.text(-0.08, 1.07, label, transform=axes.transAxes, fontsize=20, va='top', ha='left')
    return {'figS3_probes': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
