# variable_07_hydrology/crustal_porosity.py
#
# Athy's law porosity vs depth.

import numpy as np

PHI_0 = 0.4  # dimensionless — initial surface porosity
# ⚠️ EARTH FALLBACK — shale/mixed sedimentary crust.
# Flag 82.

K_COMP = 31.0e6  # Pa — bulk compaction modulus
# ⚠️ EARTH FALLBACK — shale/mixed sedimentary crust.
# Flag 82.

RHO_B = 2500.0  # kg m⁻³ — bulk crustal rock density for compaction
# ⚠️ EARTH FALLBACK — Flag 82.


def compute_porosity_profile(g: float, z_array_m):
    """
    Porosity φ(z) = φ₀ exp(−c z) with c = ρ_b g / K_comp.
    """
    c = RHO_B * g / K_COMP
    phi = PHI_0 * np.exp(-c * z_array_m)
    return {"c_m_inv": c, "phi_profile": phi, "z_m": z_array_m}


def compute_compaction_depth(g: float) -> float:
    """E-folding depth z_e = 1/c [m]."""
    c = RHO_B * g / K_COMP
    return 1.0 / c
