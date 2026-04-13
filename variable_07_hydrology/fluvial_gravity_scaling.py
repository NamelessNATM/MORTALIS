# variable_07_hydrology/fluvial_gravity_scaling.py
#
# Darcy–Weisbach relative velocity scaling with gravity.

G_EARTH = 9.81  # m s⁻² — Earth reference gravity
# ⚠️ EARTH REFERENCE VALUE — used only as scaling denominator.

F_DARCY = 0.05  # dimensionless — Darcy-Weisbach friction factor
# ⚠️ EARTH FALLBACK — midpoint of 0.04–0.06 range.
# Validated for gravel-bed rocky channels: Earth, Mars, Titan.
# Flag 84.


def compute_fluvial_gravity_scaling(g: float):
    """
    U_planet / U_earth = sqrt(g_planet / g_earth) for identical geometry.
    """
    scaling_factor = (g / G_EARTH) ** 0.5
    return {
        "U_scaling": scaling_factor,
        "Q_scaling": scaling_factor,
        "note": (
            "Relative scaling only. Absolute velocity requires R_h and S_lope "
            "(topographic inputs — deferred). "
            "U_planet = U_earth_equivalent * U_scaling for identical channel geometry."
        ),
    }
