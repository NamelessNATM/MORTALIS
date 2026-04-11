# variable_02_composition/mass_radius_dwarf.py
#
# Sub-hydrostatic dwarf bodies: radius from the geometric uncompressed sphere
# formula. Valid from M_min up to approximately 1e24 kg, where internal pressure
# is negligible relative to the bulk modulus of rock (P << K_0).
#
# Formula
# -------
#   R = ( 3 * M / (4 * pi * rho_0) )^(1/3)
#
#   R      — radius of the body [m]
#   M      — total mass [kg]
#   rho_0  — zero-pressure bulk density of the material [kg/m^3]
#   pi     — Archimedes' constant (ratio of a circle's circumference to diameter)
#
# Derivation: Purely geometric. Volume of a sphere V = (4/3)*pi*R^3 combined with
# M = rho_0 * V. Solved for R. First-principles, Rule 1 Category B. Valid because
# at these masses, lattice Coulomb forces resist compression entirely — density
# equals zero-pressure density throughout.
#
# Source: research session 2026-04-11, Section 3.1.
#
# Ceres calibration
# -----------------
#   M = 9.38e20 kg, rho_0 = 2,162 kg/m^3 (known Ceres bulk density)
#   → R = (3 * 9.38e20 / (4 * pi * 2162))^(1/3) ≈ 469,000 m
#   Known Ceres R = 473,000 m → 0.9% error (acceptable).
#
# ⚠️ EARTH FALLBACK — DEFAULT_RHO_0 of 3500 kg/m^3 is a representative rocky body
# value from terrestrial and meteorite measurements. Flag 13.
#
# ⚠️ Flag 13: rho_0 for dwarf bodies is composition-dependent and not derivable
# from mass alone. Defaults to 3500 kg/m^3 (rocky). A future disk chemistry
# variable may supply this directly.

import math

PI = math.pi
DEFAULT_RHO_0_KG_M3 = 3500.0  # kg/m^3 — rocky body zero-pressure density


def compute_radius_dwarf(M_kg: float, rho_0_kg_m3: float = DEFAULT_RHO_0_KG_M3) -> float:
    """
    Radius [m] of an uncompressed spherical body of mass M_kg at uniform
    zero-pressure density rho_0_kg_m3.
    """
    return (3.0 * M_kg / (4.0 * PI * rho_0_kg_m3)) ** (1.0 / 3.0)
