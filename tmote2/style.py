"""Shared matplotlib style, colours and colormaps.

Colour convention: each filling fraction has its own colour
(1/3 blue, 1/2 red, 2/3 orange).
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Figure width used throughout (the original code computes it from a width of
# 515 pt and passes it to ``figsize``, which takes inches)
FIG_WIDTH = 515 / (72 / 2.54)


def rgb_to_hex(rgb) -> str:
    rgb = np.asarray(rgb)
    return '#{:02X}{:02X}{:02X}'.format(*[int(v) for v in rgb])


color_1_3 = rgb_to_hex([0, 170, 255])
color_1_2 = rgb_to_hex([255, 85, 85])
color_2_3 = rgb_to_hex([255, 191, 33])
filling_colors = {'one_third': color_1_3, 'half': color_1_2, 'two_thirds': color_2_3}

# Rxx: inferno, Rxy: PuOr (orange for negative, purple for positive values).
# Copies are taken so that the shared matplotlib colormaps are not modified;
# masked / NaN pixels are drawn black.
Rxx_cmap = matplotlib.colormaps['inferno'].copy()
Rxx_cmap.set_bad(color='black')
Rxy_cmap = matplotlib.colormaps['PuOr'].copy()
Rxy_cmap.set_bad(color='black')


def apply_style():
    """Set the matplotlib defaults used by all figures (idempotent)."""
    # Arial as in the paper; DejaVu Sans where Arial is not installed
    matplotlib.rc('font', family=['arial', 'DejaVu Sans'], size=20)
    params = {
        'xtick.major.size': 4, 'ytick.major.size': 4,
        'xtick.minor.size': 3, 'ytick.minor.size': 3,
        'xtick.major.width': 1, 'ytick.major.width': 1,
        'xtick.minor.width': .5, 'ytick.minor.width': .5,
    }
    matplotlib.rcParams.update(params)


def new_figure(width, height, **kwargs):
    """A figure of the shared width, on a 100x100 grid for placing axes."""
    fig = plt.figure(figsize=(width, height), **kwargs)
    return fig, plt.GridSpec(100, 100, figure=fig)


def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    return np.array([int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)])


def generate_con_color(input_color_hex: str, num_colors: int):
    """``num_colors`` colours running from ``input_color_hex`` (first) to black (last)."""
    if num_colors < 2:
        raise ValueError("List length must be at least 2.")
    input_rgb = hex_to_rgb(input_color_hex) / 255
    black = np.zeros(3)
    colorlist = [(1 - i / (num_colors - 1)) * black + (i / (num_colors - 1)) * input_rgb
                 for i in range(num_colors)]
    return np.flip(colorlist, axis=0)


def save_pdfs(figures, directory, **kwargs):
    """Write each ``{name: figure}`` as ``<directory>/<name>.pdf``."""
    options = dict(dpi=300, bbox_inches='tight', transparent=True, backend='pdf')
    options.update(kwargs)
    for name, fig in figures.items():
        fig.savefig(f'{directory}/{name}.pdf', **options)


def add_legend_rule(ax, legend):
    """Draw a thin horizontal rule under the title of ``legend``, across the width of the legend."""
    fig = ax.figure
    fig.canvas.draw()
    to_axes = ax.transAxes.inverted()
    (x0, y0), (x1, _) = to_axes.transform(legend.get_frame().get_window_extent().get_points())
    y = to_axes.transform(legend.get_title().get_window_extent().get_points())[0][1]
    rule, = ax.plot([x0, x1], [y, y], transform=ax.transAxes, color='black', linewidth=1,
                    solid_capstyle='butt', gid='legend_rule')
    return rule
