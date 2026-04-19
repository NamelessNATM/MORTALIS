# variable_08_volatile_inventory/crossover_mass.py
#
# PURPOSE: Compute the crossover mass m_c for hydrodynamic entrainment of
# a heavy species by an escaping light species.
#
# Formula (Hunten, Pepin & Owen 1987):
#   m_c = m_1 + k_B * T_exo * F_1 / (b_12 * g * X_1)
#
# where:
#   m_1   : mass of escaping light species [kg]
#   T_exo : exobase temperature [K]
#   F_1   : escaping number density flux of light species [m^-2 s^-1]
#   b_12  : binary diffusion parameter [cm^-1 s^-1] — converted to
#           [m^-1 s^-1] internally
#   g     : surface gravity [m/s^2]
#   X_1   : mole fraction of light constituent at the lower boundary
#
# Heavy species with m_heavy <= m_c is entrained and escapes. Heavy
# species with m_heavy > m_c is retained.
#
# F_1 derivation: F_1 = Mdot / (4 * pi * R^2 * m_1)
#   where Mdot is V05 energy-limited mass loss [kg/s] and R is planetary
#   radius. Altitude independence: in spherical steady-state outflow,
#   F_1(r) ~ 1/r^2 (continuity) and g(r) ~ 1/r^2 (Newtonian gravity), so
#   F_1 / g is r-independent. Evaluated at surface per research cycle Gap 5c.
#
# X_1 assumption: For hydrogen-dominated hydrodynamic blow-off, X_1 -> 1.
#   This is the Hunten-Pepin-Owen simplifying assumption. On mixed
#   atmospheres the light fraction must be supplied; this is a deferred
#   extension, not a current cascade quantity.
#
# ⚠️ Flag 155: Multi-species H / H2 F_1 decomposition requires the
#   dissociation fraction at the homopause. Not in cascade. If both atomic
#   H and molecular H2 are simultaneously escaping, the F_1 used here is
#   the bulk Mdot divided by the dominant-species mass — this is the
#   hydrogen identity choice from hydrogen_identity.py.
#
# Earth calibration (ancient):
#   T_exo = 8000 K (extreme XUV), g = 9.81 m/s^2, Mdot ~ 10^9 kg/s,
#   R = 6.371e6 m, m_1 = m_H = 1.67e-27 kg, X_1 = 1.
#   F_1 = 10^9 / (4*pi*(6.371e6)^2 * 1.67e-27) = 1.17e21 m^-2 s^-1
#   b_12 (H-O, T=8000 K) = 4.8e17 * 8000^0.75 = 4.06e20 cm^-1 s^-1
#                       = 4.06e22 m^-1 s^-1
#   m_c - m_1 = (1.381e-23 * 8000 * 1.17e21) / (4.06e22 * 9.81 * 1.0)
#             = 1.29e2 / 3.98e23 = 3.25e-22 kg = 196 amu
#   Crossover mass ~196 amu is consistent with Mars-history ancient
#   entrainment of CO2 (44 amu) and heavier noble gases. ✓
#
# Modern Mars (current XUV): Mdot ~ 10^6 kg/s, T_exo ~ 2000 K.
#   F_1 = 1.17e18, b_12 = 4.8e17 * 2000^0.75 = 1.43e20 cm^-1 s^-1
#                      = 1.43e22 m^-1 s^-1
#   m_c - m_1 = (1.381e-23 * 2000 * 1.17e18) / (1.43e22 * 3.71 * 1.0)
#             = 3.23e-2 / 5.31e22 = 6.09e-25 kg = 0.37 amu
#   Crossover mass ~1.4 amu means no entrainment of anything heavier
#   than H itself — consistent with modern Mars losing only H. ✓

import math
from variable_08_volatile_inventory.b12_coefficients import get_b12

_K_B = 1.381e-23   # J/K
_PI = math.pi
_CM_TO_M = 1.0e2   # cm^-1 s^-1 to m^-1 s^-1: multiply by 100


def compute_crossover_mass(
    m_1_kg: float,
    T_exo_K: float,
    M_dot_kg_s: float,
    R_m: float,
    g_m_s2: float,
    light_species: str,
    heavy_species: str,
    X_1: float = 1.0,
) -> dict:
    """
    Compute the crossover mass for a light-heavy species pair.

    Parameters
    ----------
    m_1_kg        : mass of escaping light species [kg]
    T_exo_K       : exobase temperature [K]
    M_dot_kg_s    : bulk hydrodynamic mass loss rate [kg/s] from V05
    R_m           : planetary radius [m] from V02
    g_m_s2        : surface gravity [m/s^2] from V02
    light_species : e.g., "H", "H2"
    heavy_species : e.g., "CO", "O"
    X_1           : mole fraction of light species at lower boundary
                    (default 1.0 for hydrogen-dominated blow-off)

    Returns
    -------
    dict with keys:
        m_c_kg        : float or None — crossover mass, or None if b12 unavailable
        m_c_amu       : float or None
        F_1           : float — light species number flux [m^-2 s^-1]
        b12_info      : dict returned from get_b12
        entrains      : bool or None — True if m_heavy <= m_c; None if not computable
        m_heavy_kg    : float — mass of heavy species [kg]
        notes         : str
    """
    # Heavy species masses
    m_heavy_kg_table = {
        "CO":  4.65e-26,
        "O":   2.66e-26,
        "S":   5.31e-26,
        "N2":  4.65e-26,
        "CO2": 7.31e-26,
    }
    m_heavy_kg = m_heavy_kg_table.get(heavy_species)
    if m_heavy_kg is None:
        return {
            "m_c_kg": None,
            "m_c_amu": None,
            "F_1": None,
            "b12_info": None,
            "entrains": None,
            "m_heavy_kg": None,
            "notes": f"Heavy species {heavy_species} mass not tabulated.",
        }

    # F_1 = Mdot / (4 pi R^2 m_1)
    if R_m <= 0.0 or m_1_kg <= 0.0:
        return {
            "m_c_kg": None,
            "m_c_amu": None,
            "F_1": None,
            "b12_info": None,
            "entrains": None,
            "m_heavy_kg": m_heavy_kg,
            "notes": "Invalid inputs: R or m_1 non-positive.",
        }

    F_1 = M_dot_kg_s / (4.0 * _PI * R_m * R_m * m_1_kg)

    # b_12 lookup
    b12_info = get_b12(light_species, heavy_species, T_exo_K)
    b12_cm = b12_info["b12_cm_inv_s_inv"]

    if b12_cm is None:
        return {
            "m_c_kg": None,
            "m_c_amu": None,
            "F_1": F_1,
            "b12_info": b12_info,
            "entrains": None,
            "m_heavy_kg": m_heavy_kg,
            "notes": (
                f"Crossover mass not computable for pair "
                f"{light_species}-{heavy_species}. {b12_info['notes']}"
            ),
        }

    # Convert b_12 from cm^-1 s^-1 to m^-1 s^-1
    b12_m = b12_cm * _CM_TO_M

    if X_1 <= 0.0 or g_m_s2 <= 0.0 or b12_m <= 0.0:
        return {
            "m_c_kg": None,
            "m_c_amu": None,
            "F_1": F_1,
            "b12_info": b12_info,
            "entrains": None,
            "m_heavy_kg": m_heavy_kg,
            "notes": "Invalid inputs: X_1, g, or b_12 non-positive.",
        }

    # m_c = m_1 + k_B * T_exo * F_1 / (b_12 * g * X_1)
    m_c_kg = m_1_kg + (_K_B * T_exo_K * F_1) / (b12_m * g_m_s2 * X_1)
    m_c_amu = m_c_kg / 1.661e-27

    entrains = m_heavy_kg <= m_c_kg

    return {
        "m_c_kg": m_c_kg,
        "m_c_amu": m_c_amu,
        "F_1": F_1,
        "b12_info": b12_info,
        "entrains": entrains,
        "m_heavy_kg": m_heavy_kg,
        "notes": (
            f"m_c = {m_c_amu:.2f} amu; m_heavy ({heavy_species}) = "
            f"{m_heavy_kg/1.661e-27:.2f} amu; "
            f"{'ENTRAINED' if entrains else 'RETAINED against entrainment'}. "
            f"{b12_info['source_flag']}."
        ),
    }
