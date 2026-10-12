"""Peak-position models for the magnetic-field dependence of the density (Fig. 3)."""
import numpy as np


def quadratic(x, a, c):
    return a * x**2 + c


def affine(x, b, c):
    return b * x + c


def constant(x, _, c):
    return np.ones_like(x) * c


MODELS = {'quadratic': quadratic, 'affine': affine, 'constant': constant}


def model_from_name(name: str):
    """The model a data file refers to, e.g. ``'function:quadratic'``."""
    return MODELS[name.split(':', 1)[-1]]


# ------------------------------------------------------------------ Fig. S6
def sigmoid(x, L, U, x0, k):
    """Sigmoid function."""
    return L + (U - L) / (1 + np.exp(-k * (x - x0)))


def linear_model(x, m, c):
    return m * x + c


def fit_sigmoid_and_extract_transition(y_values, x0_guess, x_values=None):
    """Fit a sigmoid to ``y_values`` and return its midpoint, all parameters and their covariance."""
    from scipy.optimize import curve_fit

    if x_values is None:
        x_values = np.arange(len(y_values))

    # Initial guesses: L=max(y), U=min(y), k=1e-11 per cm^-2
    popt, pcov = curve_fit(
        sigmoid, x_values, y_values,
        p0=[np.max(y_values), np.min(y_values), x0_guess, 1e-11],
        maxfev=10000,
    )
    return popt[2], popt, pcov


def fit_transition_line(rows, densities, fields, x0_guess):
    """Fit a sigmoid to each row of ``rows`` (resistance versus ``densities``, one row
    per field in ``fields``) and a line (density versus field) through the transition midpoints.

    Returns the line's parameters ``(slope, offset)`` and their uncertainties.
    """
    from scipy.optimize import curve_fit
    from .physics import elementary_q, h_Planck

    transition_points, transition_err = [], []
    for row in rows:
        x0, _, pcov = fit_sigmoid_and_extract_transition(row, x0_guess, densities)
        transition_points.append(x0)
        transition_err.append(np.sqrt(pcov[2, 2]))

    popt, pcov = curve_fit(
        linear_model, fields, transition_points,
        sigma=transition_err, absolute_sigma=True,
        p0=[-elementary_q * 1e-4 / h_Planck, x0_guess],
    )
    return popt, np.sqrt(np.diag(pcov))
