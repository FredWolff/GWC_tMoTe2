"""Reduce a matplotlib figure to a small, comparable summary of what it plots.

The same summary is recorded from the original analysis code (see
``provenance/record_golden.py``) and computed from the figures built here, so
the two can be compared without the original code or its data.
"""
import numpy as np
from matplotlib.colors import to_hex
from matplotlib.collections import LineCollection, PathCollection, PolyCollection, QuadMesh
from matplotlib.lines import Line2D


def array_stats(values):
    """Shape and a handful of order-independent statistics of an array."""
    a = np.ma.filled(np.ma.asarray(values, dtype=float), np.nan)
    finite = a[np.isfinite(a)]
    return {
        'shape': list(a.shape),
        'n_nan': int(np.isnan(a).sum()),
        'sum': float(finite.sum()) if finite.size else 0.0,
        'abs_sum': float(np.abs(finite).sum()) if finite.size else 0.0,
        'min': float(finite.min()) if finite.size else 0.0,
        'max': float(finite.max()) if finite.size else 0.0,
        # position-sensitive, so a permuted array does not compare equal
        'weighted': float((finite * np.arange(1, finite.size + 1)).sum()) if finite.size else 0.0,
    }


def _flat(arrays):
    arrays = [np.asarray(a, dtype=float).ravel() for a in arrays]
    return np.concatenate(arrays) if arrays else np.array([])


def _artist_summary(artist):
    if isinstance(artist, Line2D):
        x, y = artist.get_xdata(orig=False), artist.get_ydata(orig=False)
        return {'kind': 'line', 'x': array_stats(x), 'y': array_stats(y),
                'color': to_hex(artist.get_color()), 'linestyle': artist.get_linestyle()}
    if isinstance(artist, QuadMesh):
        return {'kind': 'mesh', 'values': array_stats(artist.get_array()),
                'coordinates': array_stats(artist.get_coordinates()),
                'cmap': artist.get_cmap().name,
                'clim': [float(v) for v in artist.get_clim()],
                'norm': type(artist.norm).__name__}
    if isinstance(artist, LineCollection):
        return {'kind': 'segments', 'segments': array_stats(_flat(artist.get_segments()))}
    if isinstance(artist, PathCollection):
        return {'kind': 'points', 'offsets': array_stats(artist.get_offsets())}
    if isinstance(artist, PolyCollection):
        return {'kind': 'polygons', 'vertices': array_stats(_flat([p.vertices for p in artist.get_paths()]))}
    return None


def summarize_axes(ax):
    # artists with this gid are drawn at positions that depend on the installed font
    artists = [s for s in (_artist_summary(a) for a in ax.get_children() if a.get_gid() != 'legend_rule')
               if s is not None]
    legend = ax.get_legend()
    return {
        'xlabel': ax.get_xlabel(), 'ylabel': ax.get_ylabel(), 'title': ax.get_title(),
        'xlim': [float(v) for v in ax.get_xlim()], 'ylim': [float(v) for v in ax.get_ylim()],
        'xscale': ax.get_xscale(), 'yscale': ax.get_yscale(),
        'xticks': [float(v) for v in ax.get_xticks()], 'yticks': [float(v) for v in ax.get_yticks()],
        'texts': [t.get_text() for t in ax.texts],
        'legend': [t.get_text() for t in legend.get_texts()] if legend else [],
        'artists': artists,
    }


def summarize_figure(fig):
    return {
        'size_inches': [float(v) for v in fig.get_size_inches()],
        'axes': [summarize_axes(ax) for ax in fig.axes],
    }


def compare(expected, got, rtol=1e-7, atol=1e-12, where='figure'):
    """List the differences between two summaries (empty if they agree)."""
    diffs = []
    if isinstance(expected, dict):
        if not isinstance(got, dict) or set(expected) != set(got):
            return [f'{where}: keys differ']
        for key in expected:
            diffs += compare(expected[key], got[key], rtol, atol, f'{where}.{key}')
    elif isinstance(expected, list):
        if not isinstance(got, list) or len(expected) != len(got):
            return [f'{where}: length {len(got) if isinstance(got, list) else got!r} != {len(expected)}']
        for i, (e, g) in enumerate(zip(expected, got)):
            diffs += compare(e, g, rtol, atol, f'{where}[{i}]')
    elif isinstance(expected, float):
        if not np.isclose(expected, got, rtol=rtol, atol=atol):
            diffs.append(f'{where}: {got!r} != {expected!r}')
    elif expected != got:
        diffs.append(f'{where}: {got!r} != {expected!r}')
    return diffs
