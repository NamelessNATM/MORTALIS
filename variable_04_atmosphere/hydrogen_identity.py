# variable_04_atmosphere/hydrogen_identity.py
#
# PURPOSE: Determine whether atomic H or molecular H₂ is the dominant
# hydrogen species at the exobase. The selection controls which Jeans
# parameter governs hydrogen escape physics downstream.
#
# Rule: T_exo >= 400 K → atomic H dominant (H₂ thermally/photolytically
#         dissociated before reaching exobase).
#       T_exo <  400 K → molecular H₂ persists to exobase.
#
# ⚠️ Flag 151: The 400 K heuristic is Earth/Solar-System calibrated only.
#   The underlying physics is the ratio of H₂ photolysis rate (from F_XUV
#   and the H₂ photoabsorption cross-section) to vertical eddy diffusion
#   rate (K_eddy). K_eddy is an empirical turbulence parameterisation
#   not derivable from cascade inputs — it would require the photochemistry
#   cascade variable that is also blocking Flag 154. The heuristic stands
#   as the flagged fallback.
#
# Sources: Hunten (1973); Zahnle & Kasting (1986); Tian (2015).
#
# Earth calibration: T_exo ~1000 K → atomic H dominant (correct — matches
#   observed Earth thermosphere composition).
# Titan calibration: T_exo ~150 K → molecular H₂ dominant (correct —
#   matches observed Titan exobase composition; H₂ persists).

_T_EXO_IDENTITY_THRESHOLD_K = 400.0


def select_dominant_hydrogen(T_exo_K: float | None) -> dict:
    """
    Select the dominant hydrogen species at the exobase.

    Parameters
    ----------
    T_exo_K : float or None
        Exobase temperature from exobase_temperature.py.
        None for dwarf / brown_dwarf regimes (no atmosphere).

    Returns
    -------
    dict with keys:
        dominant_h_species : str, one of "H", "H2", or "none"
        m_h_effective_kg   : float or None
        notes              : str
    """
    if T_exo_K is None:
        return {
            "dominant_h_species": "none",
            "m_h_effective_kg": None,
            "notes": "No atmosphere; hydrogen identity not applicable.",
        }

    if T_exo_K >= _T_EXO_IDENTITY_THRESHOLD_K:
        return {
            "dominant_h_species": "H",
            "m_h_effective_kg": 1.67e-27,
            "notes": (
                f"T_exo={T_exo_K:.1f} K >= 400 K. Atomic H dominant at "
                "exobase (H2 dissociated before reaching exobase). Flag 151."
            ),
        }

    return {
        "dominant_h_species": "H2",
        "m_h_effective_kg": 3.34e-27,
        "notes": (
            f"T_exo={T_exo_K:.1f} K < 400 K. Molecular H2 persists to "
            "exobase (cold thermosphere). Flag 151."
        ),
    }
