# variable_08_volatile_inventory/b12_coefficients.py
#
# PURPOSE: Return binary diffusion parameter b_12 [cm^-1 s^-1] for a
# light-heavy species pair at temperature T, used by the crossover mass
# formalism (Hunten, Pepin & Owen 1987).
#
# Covered pairs:
#   H2-N2    : Flag 150 (Marrero & Mason 1972, direct measurement)
#   H2-CO2   : Flag 150 (Marrero & Mason 1972, direct measurement)
#   H2-CO    : Flag 152 (H2-N2 isosteric; Ivakin & Suetin 1964 <2% validation
#              per Marrero & Mason 1972)
#   H-O      : Flag 153 (Zahnle & Kasting 1986; Chapman-Enskog with
#              Lennard-Jones parameters)
#
# Uncovered pairs (return None with Flag 156):
#   H-CO, H-S, H2-S, H2-O
#   Searched: Mason & Marrero (1970); Marrero & Mason (1972); Zahnle &
#   Kasting (1986); Tian (2015); Wordsworth et al. (2018); Poling,
#   Prausnitz & O'Connell (2001); Hu & Seager (2013, 2014); Loftus et
#   al. (2019). No direct measurement or structurally-similar analogue
#   located for these four pairs.
#
# Temperature exponent convention: b_12 = n * D_12. D_12 ~ T^1.75
# (Chapman-Enskog). At constant pressure n ~ T^-1. Therefore b_12 ~ T^0.75.
# The T^1.75 exponent applies to D_12 only — do not use it for b_12.
#
# Units: cm^-1 s^-1 per Marrero & Mason (1972) convention.

import math

# ⚠️ Flag 150: Marrero & Mason (1972) coefficients. Earth laboratory
#   calibration, 300 K to ~1000 K. Chapman-Enskog rooted but pre-exponential
#   factors are empirical curve fits.
_A_H2_N2   = 2.80e17
_ALPHA_H2_N2 = 0.74

_A_H2_CO2  = 3.1e16
_ALPHA_H2_CO2 = 0.75
_E_H2_CO2  = 11.7  # K, Arrhenius correction specific to H2-CO2

# ⚠️ Flag 152: H2-CO via H2-N2 isosteric approximation. CO and N2 are
#   isoelectronic with near-identical polarisability and kinetic diameter.
#   Marrero & Mason (1972) state H2-CO measurements by Ivakin & Suetin
#   (1964) deviate <2% from H2-N2. Earth-calibrated fallback.
_A_H2_CO   = _A_H2_N2
_ALPHA_H2_CO = _ALPHA_H2_N2

# ⚠️ Flag 153: H-O from Zahnle & Kasting (1986). Chapman-Enskog with
#   Lennard-Jones parameters. Cited directly in Tian (2015) and Wordsworth
#   et al. (2018). Earth/Solar-System calibrated; valid 300 K to >1000 K.
_A_H_O     = 4.8e17
_ALPHA_H_O = 0.75


def _pair_key(light: str, heavy: str) -> tuple:
    """Canonical pair ordering — light species first."""
    return (light, heavy)


def get_b12(light_species: str, heavy_species: str, T_K: float) -> dict:
    """
    Binary diffusion parameter b_12 for a given light-heavy species pair
    at temperature T.

    Parameters
    ----------
    light_species : str   e.g., "H", "H2"
    heavy_species : str   e.g., "N2", "CO2", "CO", "O", "S"
    T_K           : float  Temperature [K] — typically T_exo for escape
                           calculations.

    Returns
    -------
    dict with keys:
        b12_cm_inv_s_inv : float or None
        pair             : (light, heavy)
        source_flag      : str — "Flag 150", "Flag 152", "Flag 153",
                           or "Flag 156"
        notes            : str
    """
    pair = _pair_key(light_species, heavy_species)

    if pair == ("H2", "N2"):
        b12 = _A_H2_N2 * (T_K ** _ALPHA_H2_N2)
        return {
            "b12_cm_inv_s_inv": b12,
            "pair": pair,
            "source_flag": "Flag 150",
            "notes": "Marrero & Mason (1972); direct measurement.",
        }

    if pair == ("H2", "CO2"):
        b12 = _A_H2_CO2 * (T_K ** _ALPHA_H2_CO2) * math.exp(-_E_H2_CO2 / T_K)
        return {
            "b12_cm_inv_s_inv": b12,
            "pair": pair,
            "source_flag": "Flag 150",
            "notes": "Marrero & Mason (1972); direct measurement with "
                     "Arrhenius correction.",
        }

    if pair == ("H2", "CO"):
        b12 = _A_H2_CO * (T_K ** _ALPHA_H2_CO)
        return {
            "b12_cm_inv_s_inv": b12,
            "pair": pair,
            "source_flag": "Flag 152",
            "notes": "H2-N2 isosteric approximation; <2% deviation per "
                     "Ivakin & Suetin (1964) via Marrero & Mason (1972).",
        }

    if pair == ("H", "O"):
        b12 = _A_H_O * (T_K ** _ALPHA_H_O)
        return {
            "b12_cm_inv_s_inv": b12,
            "pair": pair,
            "source_flag": "Flag 153",
            "notes": "Zahnle & Kasting (1986); Chapman-Enskog with LJ "
                     "parameters.",
        }

    # Uncovered pairs — H-CO, H-S, H2-S, H2-O, and any others
    return {
        "b12_cm_inv_s_inv": None,
        "pair": pair,
        "source_flag": "Flag 156",
        "notes": (
            f"b_12 not located in primary literature for pair "
            f"{light_species}-{heavy_species}. Crossover mass not "
            "computable for this pair. Flag 156."
        ),
    }
