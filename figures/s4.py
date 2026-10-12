"""Fig. S4: resistance versus displacement field with and without a parallel magnetic field."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from matplotlib.ticker import MultipleLocator

from tmote2 import io, physics, style

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'output'


def _panel(ax, data, D_correction, title, major_step, minor_step):
    D_par = data.par_d_at_fixed_n - D_correction
    D_zero = data.zero_d_at_fixed_n - D_correction

    ax.plot(D_zero, data.r_zero_sym / physics.R_Q, color='black', label=r'$0$')
    ax.plot(D_par, data.r_par_sym / physics.R_Q, color='blue', label=r'$0.9$')

    ax.set_xlabel(r'$D/\epsilon_0$ (V/nm)')
    ax.set_ylabel(r'$R_{xx}$ (h/e$^2$)')
    ax.set_xlim(D_par.min(), D_par.max())
    leg = ax.legend(title=r'$\mu_0 H_{\parallel}$ (T)')
    leg.get_frame().set_alpha(0)
    ax.set_title(title)

    ax.yaxis.set_major_locator(MultipleLocator(major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(minor_step))
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))


def build():
    """Return ``{output file name: figure}``."""
    style.apply_style()
    D_correction = physics.get_corrections()[1]
    data = io.load('parallel_field')

    fig, gs = style.new_figure(style.FIG_WIDTH, 7)
    ax1 = fig.add_subplot(gs[:, :47])
    ax2 = fig.add_subplot(gs[:, 53:])

    _panel(ax1, data.one_half_data, D_correction, r'$\nu = -1/2$', 25, 5)
    _panel(ax2, data.two_thirds_data, D_correction, r'$\nu = -2/3$', 5, 2.5)

    for ax, label in zip([ax1, ax2], ['(a)', '(b)']):
        ax.text(-0.07, 1.06, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')
    return {'figS4_parallel_field': fig}


def save(figures, directory=OUTPUT_DIR):
    style.save_pdfs(figures, directory)


if __name__ == '__main__':
    save(build())
