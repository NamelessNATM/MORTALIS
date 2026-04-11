# variable_03_stellar/stellar_stability.py
#
# Stability classification vs stellar mass (Eker et al. 2018 regime structure;
# Ribas 2005 XUV context). Boundaries 0.5 and 1.5 M☉ are physically motivated
# thresholds from prior research — empirically established bands, not knife-edges.
#
# ⚠️ Flag 19: Stability filter Option B — full mass range, tag and pass.

"""Stellar habitability stability classification (Flag 19)."""

from __future__ import annotations


def classify_stellar_stability(m_star_solar: float) -> dict:
    """
    Classify stellar mass into a stability regime.

    Parameters
    ----------
    m_star_solar : float
        Stellar mass [M☉].

    Returns
    -------
    dict
        Keys ``stability`` (str) and ``stable`` (bool, True only for ``"stable"``).
    """
    m = m_star_solar
    if m < 0.5:
        regime = "unstable_low"
    elif m <= 1.5:
        regime = "stable"
    else:
        regime = "unstable_high"
    return {"stability": regime, "stable": regime == "stable"}
