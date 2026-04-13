# variable_03_stellar/bolometric_correction.py
#
# PURPOSE: Compute the visual bolometric correction BC_V for a main-sequence
# star as a function of effective temperature, using the Eker et al. (2020)
# fourth-degree polynomial calibrated to the IAU 2015 absolute bolometric
# magnitude scale.
#
# Formula: BC_V = a + b*x + c*x² + d*x³ + e*x⁴
#   where x = log₁₀(T_eff)
#   evaluated using Horner's method for numerical stability
#
# Coefficients (Eker et al. 2020, Table 5):
#   a = -2360.69565
#   b = +2109.00655
#   c =  -701.96628
#   d =  +103.30304
#   e =    -5.68559
#
# Domain of validity: 3100 K ≤ T_eff ≤ 36000 K (main-sequence only)
# Outside this range the polynomial diverges — hard exception required.
#
# IAU 2015 calibration (Resolution B2 zero-point = 71.197425):
#   Input:  T_eff = 5772 K (IAU 2015 nominal solar temperature)
#   Output: BC_V = -0.016 mag
#   Target: -0.016 mag (derived: M_Bol,☉ = 4.7400, M_V,☉ = 4.756)
#   Deviation: 0.000 mag ✓
#
# ⚠️ IMPLEMENTATION CRITICAL — DOUBLE PRECISION MANDATORY:
#   At solar temperatures the polynomial's positive and negative terms
#   inflate to ±13,000 before cancelling to a residual near zero.
#   Single-precision float (7 significant digits) cannot preserve this
#   residual and will produce catastrophic cancellation errors of ~1.4 mag.
#   All variables and coefficients must be 64-bit float throughout.
#
# ⚠️ IMPLEMENTATION CRITICAL — USE LOG BASE 10:
#   The independent variable is log₁₀(T_eff), not the natural logarithm.
#   Using math.log(T_eff) instead of math.log10(T_eff) produces
#   x ≈ 8.66 at solar temperature, sending all terms to extreme values.
#
# ⚠️ Flag 70 — M_V,☉ = 4.756 mag:
#   The solar absolute visual magnitude used to derive the IAU 2015
#   calibration target is an empirically adopted value from Eker et al.
#   (2020). Not derivable from Category A constants.
#   Category: Earth/Solar System fallback.
#
# Source: Eker, Z., Soydugan, F., Bilir, S., Bakış, V., Aliçavuş, F.,
#   Özer, S., Aslan, G., Alpsoy, M., Köse, Y., 2020, Monthly Notices of
#   the Royal Astronomical Society, Volume 496, Issue 3, Pages 3887–3905,
#   DOI: 10.1093/mnras/staa1659
import math

# Eker et al. (2020) Table 5 coefficients — all 64-bit float, full precision
_A = -2360.69565
_B = +2109.00655
_C = -701.96628
_D = +103.30304
_E = -5.68559

_T_MIN = 3100.0   # K — lower domain boundary
_T_MAX = 36000.0  # K — upper domain boundary


def compute_bolometric_correction(T_eff_K: float) -> float:
    """
    Compute the visual bolometric correction BC_V for a main-sequence star.

    Parameters
    ----------
    T_eff_K : float — stellar effective temperature in Kelvin

    Returns
    -------
    float — BC_V in magnitudes (may be positive near 5859–8226 K under IAU 2015)

    Raises
    ------
    ValueError if T_eff_K is outside [3100, 36000] K
    """
    if not (_T_MIN <= T_eff_K <= _T_MAX):
        raise ValueError(
            f"T_eff = {T_eff_K} K is outside the Eker et al. (2020) domain "
            f"[{_T_MIN}, {_T_MAX}] K. Polynomial diverges outside this range."
        )

    x = math.log10(T_eff_K)  # Must be log base 10 — not math.log()

    # Horner's method — mandatory for numerical stability at solar temperatures
    BC_V = _A + x * (_B + x * (_C + x * (_D + x * _E)))

    return BC_V
