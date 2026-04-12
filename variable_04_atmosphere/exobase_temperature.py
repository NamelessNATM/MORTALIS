# variable_04_atmosphere/exobase_temperature.py
#
# PURPOSE: Compute exobase temperature T_exo from XUV flux and planetary
# properties using a corrected conduction-dominated thermosphere model.
#
# Formula: T_exo = T_eq + (epsilon * F_XUV * alpha * H_0) / K_c
#
# Where H_0 = k_B * T_eq / (m_mean * g)   [atmospheric scale height, m]
#       alpha = 7                            [pressure depth factor, dimensionless]
#
# Derivation: 1D steady-state heat equation for the thermosphere:
#   d/dz (K_c * dT/dz) = -q_XUV
# Integrating from mesopause (T ≈ T_eq) to XUV absorption peak, the
# conduction path length is alpha scale heights — the natural log of the
# pressure ratio between the mesopause (~0.1 Pa) and XUV absorption peak
# (~1e-4 to 1e-6 Pa). ln(10^3) ≈ 6.9 ≈ 7.
# Source: Watson et al. (1981); Erkaev et al. (2013); Banks & Kockarts (1973).
#
# Regime applicability:
#   rocky       — model holds. Validated on Earth, Venus, Mars.
#   sub_neptune — model gives maximum T before hydrodynamic blowout.
#                 Use as upper bound. (Flag 26/34)
#   gas_giant   — model underpredicts T_exo due to Giant Planet Energy Crisis
#                 (internal Joule/auroral heating dominates over XUV on stable
#                 giants). XUV baseline is correct cascade input but is a
#                 lower bound only. (Flag 47)
#   dwarf       — model does not apply. Dwarf bodies have collisionless
#                 exospheres; bulk thermal conduction does not hold.
#                 Returns None.
#
# Earth calibration:
#   F_XUV = 0.005 W/m², g = 9.807 m/s², T_eq = 255 K,
#   m_mean = 4.815e-26 kg (N₂/O₂ mix, 0.029 kg/mol),
#   epsilon = 0.15, K_c = 0.05 W/m/K, alpha = 7
#   H_0 = (1.381e-23 * 255) / (4.815e-26 * 9.807) = 7,456 m
#   delta_z = 7 * 7,456 = 52,192 m
#   delta_T = (0.15 * 0.005 * 52,192) / 0.05 = 782.9 K
#   T_exo = 255 + 782.9 = 1,037.9 K
#   Known Earth dayside T_exo ~1,000–1,200 K ✓
#
# ⚠️ Flag 26/34: epsilon = 0.15 is empirical, multi-body confirmed
#   (Chassefière 1996; Murray-Clay et al. 2009). Range 0.1–0.3.
# ⚠️ Flag 39: K_c is a gas-dependent laboratory measurement.
#   O/N₂ thermosphere: 0.05 W/m/K (Banks & Kockarts 1973).
#   H₂/He thermosphere: 0.30 W/m/K (same source).
# ⚠️ Flag 46: alpha = 7 is a universal physical approximation from
#   ln(P_meso/P_XUV) ≈ ln(10³). Theoretically universal; empirically
#   confirmed on Earth and Mars only.
# ⚠️ Flag 47: Gas giant T_exo is a lower bound only. Giant Planet Energy
#   Crisis — internal Joule/auroral heating dominates on stable giants.
#   No cascade variable currently represents this contribution.

# Fundamental physical constant (Rule 1 Category A)
K_B = 1.381e-23  # J/K — Boltzmann constant

# ⚠️ Flag 26/34 — empirical, multi-body confirmed
EPSILON_XUV = 0.15

# ⚠️ Flag 39 — gas-dependent laboratory measurements (Banks & Kockarts 1973)
K_C_ROCKY = 0.05   # W/m/K — O/N₂-dominated thermosphere
K_C_GIANT = 0.30   # W/m/K — H₂/He-dominated thermosphere

# ⚠️ Flag 46 — universal approximation, empirically narrow
ALPHA_PRESSURE_DEPTH = 7.0

# Pass-1 mean molecular masses [kg] assigned from regime before T_exo is known.
# Rocky: N₂/CO₂ mix → 0.029 kg/mol
# Giant: H₂/He solar mix → 0.0023 kg/mol
# Source: standard atmospheric composition per regime (Section 6, research 2026-04-12)
M_MEAN_ROCKY_KG = 4.815e-26   # 0.029 kg/mol
M_MEAN_GIANT_KG = 3.800e-27   # 0.0023 kg/mol


def compute_exobase_temperature(F_XUV_W_m2: float,
                                 g_m_s2: float,
                                 T_eq_K: float,
                                 regime: str,
                                 m_mean_kg: float | None = None) -> float | None:
    """
    Exobase temperature T_exo [K], or None for dwarf regime.

    Parameters
    ----------
    F_XUV_W_m2 : orbit-averaged XUV flux [W/m²] from Variable 05
    g_m_s2     : surface gravity [m/s²] from Variable 02
    T_eq_K     : equilibrium temperature [K] from Variable 05 (used as T_0)
    regime     : compositional regime string from Variable 02
    m_mean_kg  : mean molecular mass [kg]. If None, assigned from regime
                 (Pass-1 default). Supply explicitly for Pass-2 refinement.

    Returns
    -------
    T_exo [K] or None if regime is dwarf or brown_dwarf
    """
    if regime in ('dwarf', 'brown_dwarf'):
        return None

    if m_mean_kg is None:
        m_mean_kg = (M_MEAN_GIANT_KG
                     if regime in ('gas_giant', 'sub_neptune')
                     else M_MEAN_ROCKY_KG)

    K_c = K_C_GIANT if regime in ('gas_giant', 'sub_neptune') else K_C_ROCKY

    H_0 = (K_B * T_eq_K) / (m_mean_kg * g_m_s2)
    delta_z = ALPHA_PRESSURE_DEPTH * H_0
    delta_T = (EPSILON_XUV * F_XUV_W_m2 * delta_z) / K_c

    return T_eq_K + delta_T
