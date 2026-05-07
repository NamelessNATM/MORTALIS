# variable_09_atmospheric_column/cia_coefficients.py
#
# Gray-band collision-induced absorption coefficients for τ₀ compositional term.
# One exported accessor (single public function).

from __future__ import annotations

# ⚠️ Flag 160 — HITRAN 2020 CIA gray-band averages, Earth/Solar-System
# laboratory measurements. Universal applicability not confirmed for
# extrasolar conditions outside 200–400 K validity range.
#
# ⚠️ EMPIRICAL — Flag 160b — CIA_SI_SCALE: HITRAN tabulated k values use a
# cgs/amagat convention; the Scaffold §6 SI formula (Pa² numerator) requires
# a uniform dimensionless scale factor derived by Earth τ₀ closure (τ₀ ≈ 1.86
# with N2–O2–H2O line budget). Pending formal unit conversion in research.
CIA_SI_SCALE = 1.0e24

CIA_COEFFICIENTS_M5_PER_MOLECULE2 = {
    ("N2", "N2"): 1.5e-56,
    ("O2", "O2"): 2.0e-57,
    ("O2", "N2"): 2.0e-57,
    # ⚠️ EARTH FALLBACK — Flag 160e N2–CO2 cross pair (O2–N2 isosteric) pending CIA row.
    ("N2", "CO2"): 2.0e-57,
    # ⚠️ EARTH FALLBACK — Flag 160d isosteric placeholder (N2–N2 magnitude) until
    # dedicated CO2–CO2 HITRAN CIA entry is ingested for Venus/Mars CO2 columns.
    ("CO2", "CO2"): 1.5e-56,
    # ⚠️ EARTH FALLBACK — Flag 160c isosteric scaling to N2–N2 / O2–N2 until
    # HITRAN H2–H2 and H2–He CIA rows are ingested for extrasolar envelopes.
    ("H2", "H2"): 1.5e-56,
    ("H2", "He"): 2.0e-57,
    # ⚠️ EARTH FALLBACK — Flag 160f Titan thermal-opacity isosteric placeholders
    # until HITRAN CH4–CH4 and N2–CH4 CIA rows are ingested.
    ("CH4", "CH4"): 1.5e-56,
    ("N2", "CH4"): 2.0e-57,
}


def get_cia_coefficient_m5(pair: tuple[str, str], branch: str) -> float:
    """
    Return k_ij [SI-compatible with τ₀ formula in tau_zero_compositional]
    for collision pair (i,j), or raise NotImplementedError if missing.

    Parameters
    ----------
    pair : (species_i, species_j) — order-independent for symmetric lookup.
    branch : routing label for error message (e.g. 'titan_class').
    """
    a, b = pair
    key = (a, b) if (a, b) in CIA_COEFFICIENTS_M5_PER_MOLECULE2 else (b, a)
    raw = CIA_COEFFICIENTS_M5_PER_MOLECULE2.get(key)
    if raw is None:
        raise NotImplementedError(
            f"CIA coefficient missing for pair {key!r}; required for branch "
            f"{branch!r}. Supply HITRAN 2020 CIA gray-band value (Flag 160)."
        )
    return float(raw) * CIA_SI_SCALE
