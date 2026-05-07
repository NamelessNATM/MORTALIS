# variable_09_atmospheric_column/tau_zero_compositional.py
#
# Gray-band optical depth τ₀ from CIA + line terms (Scaffold §6).

from __future__ import annotations

import math
from typing import Mapping

from variable_09_atmospheric_column.cia_coefficients import (
    CIA_COEFFICIENTS_M5_PER_MOLECULE2,
    get_cia_coefficient_m5,
)
from variable_09_atmospheric_column.line_absorption_coefficients import (
    get_line_absorption_coeff_m2,
)

_K_B = 1.381e-23  # J/K — Boltzmann (Rule 1 Category A)

# Molar masses [kg/mol] — NIST (Rule 1 Category A)
MOLAR_MASS_KG_MOL = {
    "N2": 0.028014,
    "O2": 0.031998,
    "CO2": 0.04401,
    "H2O": 0.018015,
    "CH4": 0.01604,
    "H2": 0.002016,
    "He": 0.004002602,
    "Ar": 0.039948,
    "NH3": 0.017031,
    "SO2": 0.064066,
    "H2S": 0.034081,
    "CO": 0.02801,
}


def _mean_molar_mass_kg_mol(speciation: Mapping[str, float]) -> float:
    m_bar = 0.0
    for sp, x in speciation.items():
        if x is None or x <= 0.0:
            continue
        mm = MOLAR_MASS_KG_MOL.get(sp)
        if mm is None:
            continue
        m_bar += float(x) * mm
    if m_bar <= 0.0:
        raise ValueError("Cannot compute m_bar — empty or unknown speciation.")
    return m_bar


def _cia_pairs_from_catalog(speciation: Mapping[str, float]) -> list[tuple[str, str]]:
    """Pairs listed in the CIA catalog with both mole fractions > 0."""
    pairs: list[tuple[str, str]] = []
    for (si, sj), raw in CIA_COEFFICIENTS_M5_PER_MOLECULE2.items():
        if raw is None:
            continue
        xi = float(speciation.get(si, 0.0) or 0.0)
        xj = float(speciation.get(sj, 0.0) or 0.0)
        if xi <= 0.0 or xj <= 0.0:
            continue
        pairs.append((si, sj))
    return pairs


def compute_tau_zero(
    *,
    P_s_Pa: float,
    g_m_s2: float,
    T_eq_K: float,
    speciation: Mapping[str, float],
    branch: str,
) -> float:
    """
    τ₀ = Σ k_ij x_i x_j P_s² / (2 m̄ g k_B T_ref)
         + Σ_j k_line,j x_j P_s / (m̄ g)

    T_ref = T_eq — ⚠️ Note 159 — column-mean temperature approximation.
    """
    if P_s_Pa <= 0.0 or g_m_s2 <= 0.0 or T_eq_K <= 0.0:
        raise ValueError("Invalid P_s, g, or T_eq for τ₀ composition.")

    m_bar = _mean_molar_mass_kg_mol(speciation)
    # ⚠️ Note 159 — column-mean temperature approximation
    T_ref = float(T_eq_K)
    denom_cia = 2.0 * m_bar * float(g_m_s2) * _K_B * T_ref
    denom_line = m_bar * float(g_m_s2)

    tau = 0.0
    pairs_done: set[tuple[str, str]] = set()
    for si, sj in _cia_pairs_from_catalog(speciation):
        key = tuple(sorted((si, sj)))
        if key in pairs_done:
            continue
        pairs_done.add(key)
        xi = float(speciation[si])
        xj = float(speciation[sj])
        k_ij = get_cia_coefficient_m5((si, sj), branch)
        if si != sj:
            tau += 2.0 * k_ij * xi * xj * P_s_Pa**2 / denom_cia
        else:
            tau += k_ij * xi * xj * P_s_Pa**2 / denom_cia

    # Line terms (catalog keys map to species tags)
    line_map = (
        ("H2O", "H2O_continuum"),
        ("H2O", "H2O_lines"),
        ("CO2", "CO2_15um"),
        ("CH4", "CH4_lines"),
        ("NH3", "NH3_lines"),
    )
    for species, line_key in line_map:
        x = float(speciation.get(species, 0.0) or 0.0)
        if x <= 0.0:
            continue
        # ⚠️ Note 161b — 15 µm gray line term is calibrated for Earth-thin CO2
        # columns; for Venus-class thick CO2 it multiplies unphysically with P_s.
        # CIA term carries thermal opacity here; line row suppressed pending ck.
        if branch == "venus_class" and line_key == "CO2_15um":
            continue
        # ⚠️ Flag 161c — CH4_lines not supplied by research; Titan uses CIA only.
        if branch == "titan_class" and line_key == "CH4_lines":
            continue
        k_line = get_line_absorption_coeff_m2(line_key, branch)
        tau += float(k_line) * x * P_s_Pa / denom_line

    return float(tau)
