# variable_06_tectonics/rayleigh_number.py
#
# FORMULA:
#   Ra = rho_mantle * g * alpha * DeltaT * D**3 / (kappa * eta)
#
# SOURCE: Navier-Stokes Boussinesq non-dimensionalisation. Formula is universal.
#         Coefficients alpha and kappa are Earth-calibrated (silicate assemblage).
#
# ⚠️ EARTH FALLBACK — alpha = 3e-5 K^-1, kappa = 1e-6 m²/s.
# Thermal expansivity and diffusivity calibrated to terrestrial silicates. Flag 09
# (existing Earth fallback on rocky M-R universality) does not cover these;
# these are covered by the general Earth fallback flag system. No new flag number
# assigned here — covered by the Earth fallback categories already in the record.
# Note for Cursor: add inline comments referencing ⚠️ EARTH FALLBACK on both constants.
#
# Ra_c = 1000 — critical Rayleigh number for onset of convection.
# Derived from fluid mechanics boundary layer theory. Universal.
#
# EARTH CALIBRATION:
#   rho=5515, g=9.81, alpha=3e-5, DeltaT=2700K, D=2.9e6m, kappa=1e-6, eta=1e21
#   Ra ≈ 1.1e8  (target 1e7–1e8) ✓

# ⚠️ EARTH FALLBACK — Flag: thermal expansivity, silicate calibration
_ALPHA = 3.0e-5  # thermal expansivity [K^-1]
# ⚠️ EARTH FALLBACK — Flag: thermal diffusivity, silicate calibration
_KAPPA = 1.0e-6  # thermal diffusivity [m²/s]
_RA_C = 1000.0  # critical Rayleigh number [dimensionless, universal]


def compute_rayleigh_number(
    rho_mantle: float,
    g: float,
    T_m: float,
    T_eq: float,
    D: float,
    eta: float,
) -> dict:
    """
    Compute the internal Rayleigh number for the convecting mantle.

    Parameters
    ----------
    rho_mantle : float — mean mantle density [kg/m³]
    g          : float — surface gravity [m/s²]
    T_m        : float — mantle temperature [K]
    T_eq       : float — surface equilibrium temperature [K]
    D          : float — mantle depth [m]
    eta        : float — dynamic viscosity [Pa*s]

    Returns
    -------
    dict with keys:
        Ra      : float — Rayleigh number [dimensionless]
        Ra_c    : float — critical Rayleigh number [dimensionless]
        convecting : bool — True if Ra > Ra_c
    """
    delta_T = max(T_m - T_eq, 0.0)
    Ra = rho_mantle * g * _ALPHA * delta_T * D**3 / (_KAPPA * eta)
    return {
        "Ra": Ra,
        "Ra_c": _RA_C,
        "convecting": Ra > _RA_C,
    }
