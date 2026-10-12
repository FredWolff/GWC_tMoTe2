"""Gate-voltage / carrier-density / displacement-field conversions and corrections."""
from . import io

######### Resistance quantum ##########
h_Planck = 6.62607015e-34
elementary_q = 1.602176634e-19
R_Q = h_Planck / elementary_q**2
#######################################

# Gate capacitances (F/m^2) and zero-displacement-field offset
cbg = 3 * 8.85e-12 / (34e-9)
ctg = 3 * 8.85e-12 / (35.5e-9)
D_0 = 0


def n_D_to_Vt_Vb(n_fixed, D_fixed, cbg, ctg):
    """Top and bottom gate voltages for a given density and displacement field."""
    Vt = (((D_fixed - D_0) + (cbg / 2 / 8.85e-12 / 1e9 * n_fixed) / (cbg / 1.6e-19 / 1e4))
          / (ctg / 2 / 8.85e-12 / 1e9 + ((cbg / 2 / 8.85e-12 / 1e9) * (ctg / 1.6e-19 / 1e4)) / (cbg / 1.6e-19 / 1e4)))
    Vb = (n_fixed * (1.6e-19 * 1e4) - ctg * Vt) / cbg
    return Vt, Vb


def _n_12(probe: str) -> float:
    return {'11_06': -2.652e12, '19_20': -2.660e12, '20_24': -2.601e12, '06_05': -2.673e12}[probe]


def _n_to_12_v(probe: str) -> float:
    n_23 = -3.349e12
    return (n_23 - _n_12(probe)) * 6


def get_n_correction(probe: str) -> float:
    """Shift (cm^-2) that puts the 1/2 filling of ``probe`` at its nominal density."""
    return _n_to_12_v(probe) / 2 - _n_12(probe)


def get_v_conversion(probe: str) -> float:
    """Density (cm^-2) that corresponds to one filling factor, for ``probe``."""
    return _n_to_12_v(probe)


def get_corrections(probe: str = '11_06'):
    """``[n_correction, D_correction]`` as used by all figures."""
    return [get_n_correction(probe), io.load('gate_corrections')['D_correction']]
