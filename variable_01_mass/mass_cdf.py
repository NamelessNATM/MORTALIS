# variable_01_mass/mass_cdf.py
#
# PURPOSE: Construct the cumulative distribution function (CDF) for planetary
# mass by integrating the piecewise power-law PDF. Compute normalisation
# constants A_i by enforcing continuity at regime boundaries and unit total
# probability.
#
# Formula (per segment, alpha != -1):
#   F_i(m) = F(m_{i-1}) + A_i * (m^(alpha_i+1) - m_{i-1}^(alpha_i+1))
#            / (alpha_i + 1)
#
# Inversion formula (used in mass_sampler.py):
#   M = [ (U - F(m_{i-1})) * (alpha_i + 1) / A_i
#         + m_{i-1}^(alpha_i + 1) ]^(1 / (alpha_i + 1))
#
# Source: research session 2026-04-11 Section 5.
# ⚠️ Flag 05 applies to all alpha values and DESERT_SUPPRESSION used here.
#
# Benchmark: compute_cdf_tables(m_min, m_max) must produce cumulative[-1] = 1.0

from variable_01_mass.mass_pdf import (
    ALPHA, DESERT_SUPPRESSION, REGIME_BOUNDARIES_KG, M_JUPITER_KG
)


def compute_cdf_tables(m_min_kg: float, m_max_kg: float) -> dict:
    """
    Compute normalisation amplitudes A_i and cumulative probabilities at
    each regime boundary.

    Parameters
    ----------
    m_min_kg : lower boundary (from planetary_mass_boundaries.compute_m_min)
    m_max_kg : upper boundary (from planetary_mass_boundaries.compute_m_max)

    Returns
    -------
    dict with keys:
        'boundaries' : list of 5 boundary masses [kg] including min and max
        'amplitudes' : list of 4 floats A_i
        'cumulative' : list of 4 floats F(m_i) at each upper regime boundary
    """
    boundaries = [m_min_kg] + REGIME_BOUNDARIES_KG + [m_max_kg]
    n_regimes = 4

    # --- Step 1: compute raw (unnormalised) integrals per regime ---
    # Set A_0 = 1.0 (arbitrary; will normalise at end)
    # Regime 2 amplitude is DESERT_SUPPRESSION * A_0 * m_boundary^(alpha0-alpha1)
    # ... but since alpha0 == alpha1 == -3.0, the suppression is simply
    # a multiplicative factor on A_0 at the boundary.

    raw_amplitudes = [0.0] * n_regimes
    raw_amplitudes[0] = 1.0

    # Enforce continuity: A_{i} * m_b^alpha_i = A_{i-1} * m_b^alpha_{i-1}
    # => A_{i} = A_{i-1} * m_b^(alpha_{i-1} - alpha_{i})
    # Exception: regime 2 gets additional DESERT_SUPPRESSION factor.
    for i in range(1, n_regimes):
        m_b = boundaries[i]  # upper boundary of regime i-1
        continuity_A = raw_amplitudes[i - 1] * (m_b ** (ALPHA[i - 1] - ALPHA[i]))
        if i == 1:
            raw_amplitudes[i] = continuity_A * DESERT_SUPPRESSION
        else:
            raw_amplitudes[i] = continuity_A

    # --- Step 2: integrate each regime to get raw cumulative mass ---
    def segment_integral(A, alpha, m_lo, m_hi):
        exp = alpha + 1.0
        # alpha values are -3.0, -3.0, -0.9, -1.85 — none equal -1
        return A * (m_hi**exp - m_lo**exp) / exp

    raw_integrals = []
    for i in range(n_regimes):
        raw_integrals.append(
            segment_integral(raw_amplitudes[i], ALPHA[i],
                             boundaries[i], boundaries[i + 1])
        )

    total_raw = sum(raw_integrals)

    # --- Step 3: normalise ---
    amplitudes = [A / total_raw for A in raw_amplitudes]

    # --- Step 4: compute cumulative probabilities at each upper boundary ---
    cumulative = []
    running = 0.0
    for i in range(n_regimes):
        running += segment_integral(amplitudes[i], ALPHA[i],
                                    boundaries[i], boundaries[i + 1])
        cumulative.append(running)

    # Final value must equal 1.0 (floating point tolerance ~1e-12)
    assert abs(cumulative[-1] - 1.0) < 1e-10, (
        f"CDF normalisation failed: cumulative[-1] = {cumulative[-1]}"
    )

    return {
        'boundaries': boundaries,
        'amplitudes': amplitudes,
        'cumulative': cumulative,
    }
