# variable_07_hydrology/glacial_gravity_scaling.py
#
# Glen's law / shallow-ice relative velocity scaling with gravity.

N_GLEN = 3  # dimensionless — Glen's stress exponent
# Dislocation creep in crystalline solids. Universal.

A_GLEN = 2.4e-15  # kPa⁻³ s⁻¹ — Glen's flow parameter for temperate H2O ice
# ⚠️ EARTH FALLBACK — empirical Arrhenius coefficient,
# Earth H2O ice measurements (Paterson 1994).
# Different values required for CO2 ice, CH4 ice.
# Flag 85.
# UNIT NOTE: A must be in kPa⁻³ s⁻¹ and stress computed
# in kPa throughout this formula. Converting to Pa units
# requires A_Pa = A_kPa * 1e-9 (since 1 kPa⁻³ = 1e9 Pa⁻³).

RHO_ICE = 917.0  # kg m⁻³ — density of H2O ice
# ⚠️ EARTH-MEASURED MOLECULAR CONSTANT.
# Applies to H2O ice; different values for exotic ices.

G_EARTH = 9.81  # m s⁻² — Earth reference gravity


def compute_glacial_gravity_scaling(g: float):
    """
    U_ice_planet / U_ice_earth = (g_planet / g_earth)^n, n = 3.
    """
    scaling_factor = (g / G_EARTH) ** N_GLEN
    return {
        "U_ice_scaling": scaling_factor,
        "note": (
            "Relative scaling only. Absolute velocity requires ice thickness h "
            "and surface slope alpha (topographic inputs — deferred). "
            "U_ice_planet = U_ice_earth_equivalent * U_ice_scaling for identical geometry. "
            "A_GLEN applies to H2O ice only (Flag 85)."
        ),
    }
