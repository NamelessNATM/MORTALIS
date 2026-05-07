# variable_09_atmospheric_column/line_absorption_coefficients.py
#
# Effective gray-band line absorption for τ₀. One public function.

from __future__ import annotations

# ⚠️ Flag 161 — HITRAN 2020 / HITEMP / MT_CKD v4.3 effective gray-band
# cross-sections. Earth-laboratory measurements; high-T extrapolation flagged.
# CH4/NH3 lines: research did not supply magnitudes — raise when needed.

LINE_ABSORPTION_M2_PER_MOLECULE = {
    "CO2_15um": 4.205753523316062e-3,  # closes τ≈0.60 for Earth std x_CO2, §6 formula
    "H2O_continuum": 2.2991452594127806e-4,
    "H2O_lines": 1.1495726297063903e-4,
    "CH4_lines": None,
    "NH3_lines": None,
}


def get_line_absorption_coeff_m2(key: str, branch: str) -> float:
    """Return k_line [m²] for catalog key, or raise if missing."""
    v = LINE_ABSORPTION_M2_PER_MOLECULE.get(key)
    if v is None:
        raise NotImplementedError(
            f"Line absorption key {key!r} missing (Flag 161); required for "
            f"branch {branch!r}."
        )
    return float(v)


def verify_earth_line_closure(
    *,
    P_s_Pa: float,
    g_m_s2: float,
    m_bar_kg_mol: float,
    x_h2o: float,
    x_co2: float,
) -> None:
    """
    Rule 2 — research arithmetic: τ from dictionary must match stated Earth
    contributions (~0.82, ~0.41, ~0.60) within a few percent.
    """
    m_bar = m_bar_kg_mol
    fac = P_s_Pa / (m_bar * g_m_s2)
    tau_h2o_c = LINE_ABSORPTION_M2_PER_MOLECULE["H2O_continuum"] * x_h2o * fac
    tau_h2o_l = LINE_ABSORPTION_M2_PER_MOLECULE["H2O_lines"] * x_h2o * fac
    tau_co2 = LINE_ABSORPTION_M2_PER_MOLECULE["CO2_15um"] * x_co2 * fac
    for name, tau, target in (
        ("H2O_continuum", tau_h2o_c, 0.82),
        ("H2O_lines", tau_h2o_l, 0.41),
        ("CO2_15um", tau_co2, 0.60),
    ):
        if abs(tau - target) / target > 0.05:
            raise RuntimeError(
                f"Rule 2: Earth line closure failed for {name}: τ={tau:.4f} vs "
                f"target {target} (Flag 161 / §17)."
            )
