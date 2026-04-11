# variable_01_mass/mass_sampler.py
#
# PURPOSE: Deterministically map an integer seed to a planetary mass M [kg]
# using inverse transform sampling on the normalised piecewise power-law CDF.
#
# Formula (per segment):
#   M = [ (U - F(m_{i-1})) * (alpha_i + 1) / A_i
#         + m_{i-1}^(alpha_i + 1) ]^(1 / (alpha_i + 1))
#
# where U ~ Uniform(0,1) is generated deterministically from the integer seed.
#
# Determinism guarantee: same seed always produces the same mass (Rule 5).
# PRNG: Python standard library random.Random — seeded, instance-local,
# does not affect global random state.
#
# Source: research session 2026-04-11 Section 5.
# ⚠️ Flag 05 applies to all alpha values inherited from mass_cdf.

import random
from variable_01_mass.mass_pdf import ALPHA
from variable_01_mass.mass_cdf import compute_cdf_tables
from variable_01_mass.planetary_mass_boundaries import compute_m_min, compute_m_max
from variable_01_mass.planetary_mass_boundaries import (
    SIGMA_RBF_ROCK_PA, SIGMA_RBF_ICE_PA
)

# Default lower boundary uses rocky body parameters
_DEFAULT_RHO_KG_M3 = 3500.0   # kg/m^3 — representative rocky body density


def sample_mass(seed: int,
                rho_kg_m3: float = _DEFAULT_RHO_KG_M3,
                sigma_rbf_pa: float = SIGMA_RBF_ROCK_PA) -> float:
    """
    Deterministically sample a planetary mass from the bias-corrected
    piecewise power-law distribution using inverse transform sampling.

    Parameters
    ----------
    seed        : integer seed for deterministic PRNG
    rho_kg_m3   : bulk density for lower boundary computation [kg/m^3]
    sigma_rbf_pa: yield strength for lower boundary computation [Pa]

    Returns
    -------
    M [kg] — planetary mass
    """
    m_min = compute_m_min(rho_kg_m3, sigma_rbf_pa)
    m_max = compute_m_max()

    tables = compute_cdf_tables(m_min, m_max)
    boundaries  = tables['boundaries']
    amplitudes  = tables['amplitudes']
    cumulative  = tables['cumulative']

    # Generate U deterministically
    rng = random.Random(seed)
    U = rng.random()

    # Locate which regime U falls in
    regime_index = 0
    F_lower = 0.0
    for i, F_upper in enumerate(cumulative):
        if U <= F_upper:
            regime_index = i
            if i > 0:
                F_lower = cumulative[i - 1]
            break

    A     = amplitudes[regime_index]
    alpha = ALPHA[regime_index]
    m_lo  = boundaries[regime_index]
    exp   = alpha + 1.0

    # Inverse CDF formula
    M = ((U - F_lower) * exp / A + m_lo**exp) ** (1.0 / exp)
    return M
