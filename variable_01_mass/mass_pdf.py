# variable_01_mass/mass_pdf.py
#
# PURPOSE: Define the four-regime piecewise power-law probability density
# function (PDF) for planetary mass, normalised to integrate to 1 over
# [M_min, M_max].
#
# Formula: f(m) = A_i * m^alpha_i  for m in [m_{i-1}, m_i)
# The desert regime (regime 2) has its amplitude suppressed by factor 1/7.7
# relative to the regime-1 power-law extrapolation.
#
# Derivation of structural form: the piecewise power-law emerges from the
# accretion physics — specifically the rapid runaway gas accretion transition
# that depopulates the sub-Saturn desert, and the gravitational instability
# channel that produces the super-Jupiter population.
#
# ⚠️ Flag 05: ALL alpha exponents and the 1/7.7 suppression factor are
# empirical fits to bias-corrected (Abel-inverted) RV + transit survey data.
# Confirmed across multiple planetary bodies. Not derivable from first
# principles. Source: Marcy et al. (2005); Howard et al. (2010);
# Fressin et al. (2013); Tremaine & Dong (2012);
# research session 2026-04-11 Sections 1, 5, 6.
#
# Earth calibration: Not applicable — this is a galactic demographic function.
# Benchmark: integrating f(m) over [M_min, M_max] must equal 1.0 after
# normalisation (verified in mass_cdf.py).

# Fundamental physical constants (Rule 1 Category A)
# (none required directly — regime boundaries use M_JUPITER_KG from boundaries)

# Jupiter mass
M_JUPITER_KG = 1.8982e27  # kg

# Regime boundary masses [kg]
# Regime 1: M_min to 0.087 M_J  (terrestrial to sub-Neptune)
# Regime 2: 0.087 to 0.21  M_J  (sub-Saturn desert)
# Regime 3: 0.21  to 2.2   M_J  (gas giants)
# Regime 4: 2.2   to 13    M_J  (super-Jupiters)

REGIME_BOUNDARIES_KG = [
    0.087 * M_JUPITER_KG,   # boundary 1-2
    0.21  * M_JUPITER_KG,   # boundary 2-3
    2.2   * M_JUPITER_KG,   # boundary 3-4
]

# ⚠️ Flag 05 — empirical fitted exponents
ALPHA = [-3.0, -3.0, -0.9, -1.85]

# ⚠️ Flag 05 — empirical fitted suppression factor for the desert
DESERT_SUPPRESSION = 1.0 / 7.7


def _amplitude(regime_index: int, A1: float) -> float:
    """
    Return the amplitude A_i for each regime given A1.
    Regime 2 amplitude is suppressed by DESERT_SUPPRESSION relative to A1.
    Regimes 3 and 4 amplitudes are set by continuity at regime boundaries.
    """
    # Amplitudes are computed in mass_cdf.py where continuity is enforced.
    # This function is a placeholder for documentation purposes.
    raise NotImplementedError(
        "Amplitudes are computed in mass_cdf.py via continuity conditions."
    )


def unnormalised_pdf(m_kg: float, amplitudes: list, m_min_kg: float) -> float:
    """
    Evaluate the unnormalised piecewise power-law PDF at mass m_kg.

    Parameters
    ----------
    m_kg       : mass to evaluate [kg]
    amplitudes : list of 4 floats [A0, A1, A2, A3] computed by mass_cdf
    m_min_kg   : lower boundary of regime 1 [kg]

    Returns
    -------
    f(m) [kg^-1] — unnormalised
    """
    boundaries = [m_min_kg] + REGIME_BOUNDARIES_KG + [13.0 * M_JUPITER_KG]
    for i in range(4):
        if boundaries[i] <= m_kg < boundaries[i + 1]:
            return amplitudes[i] * (m_kg ** ALPHA[i])
    return 0.0
