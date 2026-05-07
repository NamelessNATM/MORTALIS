# variable_09_atmospheric_column/kombayashi_ingersoll_limit.py
#
# Steam-atmosphere outgoing longwave limit (Pierrehumbert 2010 form, Scaffold §14).

import math

_SIGMA = 5.670e-8

# ⚠️ Flag 178 — Earth-laboratory L_v and saturation pressure anchor; condensable
# universal applicability not derived.
L_V_H2O_J_PER_KG = 2.454e6
R_VAPOR_H2O_J_PER_KG_K = 461.5
P_STAR_H2O_TRIPLE_PA = 611.657

# ⚠️ EMPIRICAL — Flag 178b dimensionless κ and amplitude A tuned so Earth water
# atmosphere gives OLR_KI ≈ 282 W/m² with Pierrehumbert log term structure.
_KAPPA_KI = 0.0185
_A_KI = 2.610559256814136e-9


def compute_kombayashi_ingersoll_olr_W_m2(
    *,
    g_m_s2: float,
    r_specific_condensable_J_per_kg_K: float,
    latent_heat_J_per_kg: float,
) -> float:
    """
    OLR_KI = A · σ · (L_v/R_specific)^4 · (ln(κ·P*/g))^(-4)
    """
    rs = float(r_specific_condensable_J_per_kg_K)
    lv = float(latent_heat_J_per_kg)
    g = float(g_m_s2)
    ln_term = math.log(_KAPPA_KI * P_STAR_H2O_TRIPLE_PA / g)
    if ln_term <= 0.0:
        raise ValueError("KI limit: non-positive ln term.")
    return float(
        _A_KI * _SIGMA * (lv / rs) ** 4 * ln_term ** (-4)
    )


def evaluate_runaway_flag(
    *,
    F_mean_W_m2: float,
    albedo_final: float,
    g_m_s2: float,
) -> tuple[bool, float]:
    """Compare absorbed solar to OLR_KI for condensible H2O."""
    f_abs = float(F_mean_W_m2) * (1.0 - float(albedo_final)) / 4.0
    olr = compute_kombayashi_ingersoll_olr_W_m2(
        g_m_s2=g_m_s2,
        r_specific_condensable_J_per_kg_K=R_VAPOR_H2O_J_PER_KG_K,
        latent_heat_J_per_kg=L_V_H2O_J_PER_KG,
    )
    return (f_abs > olr), olr
