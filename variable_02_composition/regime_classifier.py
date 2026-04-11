# variable_02_composition/regime_classifier.py
#
# Map planetary mass [kg] to a compositional regime string.
#
# Regime boundary masses (derived from constants below):
#   ROCKY_SUBNEPTUNE_BOUNDARY_KG (~4.4 M_earth):
#     Radius valley / transition between rocky and volatile-rich envelopes in
#     the exoplanet population (Fulton et al.; demographic threshold).
#   SUBNEPTUNE_GASGIANT_BOUNDARY_KG (~127 M_earth):
#     Onset of electron degeneracy pressure in the core; interior physics
#     shifts from primarily thermal to degenerate (mass–radius inflection).
#   GASGIANT_BROWNDWARF_BOUNDARY_KG (13 M_Jupiter):
#     Deuterium burning limit — upper mass for objects typically classed as
#     planets vs substellar brown dwarfs (convention from formation/spectral
#     studies).
#
# Source: research session 2026-04-11
#
# Flag 08: Compositional degeneracy in the ~2–10 M_earth range is real; the
# regime boundary here is a statistical threshold from demographics, not a
# deterministic physical knife-edge between classes.

M_EARTH_KG = 5.972e24
M_JUPITER_KG = 1.8982e27

ROCKY_SUBNEPTUNE_BOUNDARY_KG = 4.4 * M_EARTH_KG
SUBNEPTUNE_GASGIANT_BOUNDARY_KG = 127.0 * M_EARTH_KG
GASGIANT_BROWNDWARF_BOUNDARY_KG = 13.0 * M_JUPITER_KG


def classify_regime(M_kg: float) -> str:
    """
    Classify mass into one of four compositional regimes.

    Returns one of: 'rocky', 'sub_neptune', 'gas_giant', 'brown_dwarf'.
    """
    if M_kg <= ROCKY_SUBNEPTUNE_BOUNDARY_KG:
        return "rocky"
    if M_kg <= SUBNEPTUNE_GASGIANT_BOUNDARY_KG:
        return "sub_neptune"
    if M_kg <= GASGIANT_BROWNDWARF_BOUNDARY_KG:
        return "gas_giant"
    return "brown_dwarf"
