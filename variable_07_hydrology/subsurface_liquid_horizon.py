# variable_07_hydrology/subsurface_liquid_horizon.py
#
# Depth z* where geothermal gradient crosses Ice Ih melting curve (H2O).

from variable_07_hydrology.volatile_phase_state import SPECIES_DATA

K_CRUST = 2.5  # W m⁻¹ K⁻¹ — thermal conductivity of rocky crust
# ⚠️ EARTH FALLBACK — derived from terrestrial silicate
# rock measurements. Universal applicability not confirmed.
# Flag 80.

RHO_CRUST = 2800.0  # kg m⁻³ — mean crustal density
# ⚠️ EARTH FALLBACK — terrestrial continental crust.
# Flag 81.

# Ice Ih melting linearisation (Wagner et al. 1994); triple-point anchor.
# ⚠️ EARTH-MEASURED MOLECULAR CONSTANT — Ice Ih Clapeyron slope
# 1.35e8 Pa derived from laboratory measurements. Intrinsic to H2O
# crystal structure; universal. Flag 79.
ICE_IH_P_SLOPE_PA = 1.35e8
T_TRIPLE_H2O_K = 273.16
P_TRIPLE_H2O_PA = 611.7


def compute_subsurface_liquid_horizon(
    T_eq_K: float,
    q_s_Wm2,
    g: float,
    P_s_Pa: float,
    rho_mean_kgm3: float,
):
    """
    Depth [m] to first crossing of Ice Ih melting temperature, or None.

    # ⚠️ T_s APPROXIMATION — T_eq used as surface temperature proxy.
    # Greenhouse correction deferred (Flag 43).

    rho_mean_kgm3 is reserved for future lithosphere models (unused here).
    """
    _ = rho_mean_kgm3

    T_s = T_eq_K
    T_c_h2o = SPECIES_DATA["H2O"]["T_c"]

    if q_s_Wm2 is None or q_s_Wm2 == 0.0:
        return None

    if T_s > T_c_h2o:
        return None

    # T(z) = T_s + (q_s / k) * z ; P(z) = P_s + rho_crust * g * z
    # T_melt(P) = T_TRIPLE * (1 - (P - P_TRIPLE) / ICE_IH_P_SLOPE_PA)
    a = q_s_Wm2 / K_CRUST
    b = T_TRIPLE_H2O_K / ICE_IH_P_SLOPE_PA * RHO_CRUST * g
    T_melt_surface = T_TRIPLE_H2O_K * (
        1.0 - (P_s_Pa - P_TRIPLE_H2O_PA) / ICE_IH_P_SLOPE_PA
    )

    denom = a + b
    if denom == 0.0:
        return None

    z_star = (T_melt_surface - T_s) / denom

    if z_star <= 0.0:
        return 0.0

    if z_star > 1.0e6:
        return None

    return z_star
