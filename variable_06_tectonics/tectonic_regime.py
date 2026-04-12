# variable_06_tectonics/tectonic_regime.py
#
# PURPOSE: Classify the tectonic regime of a rocky planet from its Rayleigh number.
#
# REGIME CLASSIFICATION (from V06 research Section 1.3, grain damage theory):
#   Ra < Ra_c                       → stagnant_lid (conductive only)
#   Ra_c <= Ra < Ra_sluggish        → mobile_lid   (plate tectonics)
#   Ra >= Ra_sluggish               → sluggish_lid  (episodic/drip subduction)
#
# Ra_sluggish threshold: ~1e9 (high-temperature limit from boundary layer theory).
# ⚠️ EARTH FALLBACK — Ra_sluggish = 1e9 is a literature convention from 2D/3D
# numerical models, not a closed-form universal derivation. Flag for review on
# extreme planetary parameters.
#
# SOURCE: V06 research response Section 1.3, grain damage theory discussion.
#         Numerical thresholds from Tackley (2000) and Lourenço et al. (2018).
#
# Regime is only meaningful for rocky and sub-Neptune (solid-mantle) planets.
# Gas giant, brown dwarf, and dwarf regimes handled by entry point.

_RA_SLUGGISH = 1.0e9  # ⚠️ EARTH FALLBACK threshold


def classify_tectonic_regime(Ra: float, Ra_c: float) -> str:
    """
    Classify tectonic regime from Rayleigh number.

    Parameters
    ----------
    Ra   : float — Rayleigh number
    Ra_c : float — critical Rayleigh number

    Returns
    -------
    str — one of: 'stagnant_lid', 'mobile_lid', 'sluggish_lid'
    """
    if Ra < Ra_c:
        return "stagnant_lid"
    elif Ra < _RA_SLUGGISH:
        return "mobile_lid"
    else:
        return "sluggish_lid"
