# variable_02_composition/regime_classifier.py
#
# Map planetary mass [kg] to a compositional regime string.
#
# Regime boundary masses (derived from constants below):
#   DWARF_ROCKY_BOUNDARY_KG = 1e24 kg — the boundary where internal pressure P_c
#     begins to exceed ~1% of the bulk modulus K_0 of silicate rock (~200 GPa).
#     Below this, mean density equals zero-pressure density.
#     Source: research session 2026-04-11 Section 3.1.
#   ROCKY_SUBNEPTUNE_BOUNDARY_KG (~4.4 M_earth):
#     Radius valley / transition between rocky and volatile-rich envelopes in
#     the exoplanet population (Fulton et al.; demographic threshold).
#   SUBNEPTUNE_GASGIANT_BOUNDARY_KG (~127 M_earth):
#     Onset of electron degeneracy pressure in the core; interior physics
#     shifts from primarily thermal to degenerate (mass–radius inflection).
#   Gas giant / brown dwarf boundary [kg]:
#     Z-dependent deuterium-burning minimum mass M_DB(Z) from Spiegel et al.
#     (2011), used in classify_regime(M_kg, Z). Legacy 13 M_J constant
#     GASGIANT_BROWNDWARF_BOUNDARY_KG remains for V01 optional regime clamps
#     (planetary_mass_boundaries / mass_sampler) only.
#
# Flag 06 (closed): static 13 M_J replaced by Spiegel et al. (2011) quadratic
#   M_DB(Z) = 3407 Z² − 271 Z + 16.3 [M_J] in classify_regime.
# ⚠️ Note 186: Spiegel quadratic non-monotonic above Z ≈ 0.0398; formula turns
#   upward beyond. Model applicability limit. Cascade max Z ≈ 0.024 at minimum
#   age (τ = 0.5 Gyr in JJ2010 envelope) is well below this limit — no clamp
#   needed at present cascade scope.
#
# Source: research session 2026-04-11
#
# Note 08: Compositional degeneracy in the ~2–10 M_earth range is real; the
# regime boundary here is a statistical threshold from demographics, not a
# deterministic physical knife-edge between classes.

M_EARTH_KG = 5.972e24
M_JUPITER_KG = 1.8982e27

DWARF_ROCKY_BOUNDARY_KG = 1.0e24  # kg — onset of significant compression

ROCKY_SUBNEPTUNE_BOUNDARY_KG = 4.4 * M_EARTH_KG
SUBNEPTUNE_GASGIANT_BOUNDARY_KG = 127.0 * M_EARTH_KG
GASGIANT_BROWNDWARF_BOUNDARY_KG = 13.0 * M_JUPITER_KG


def m_deuterium_burning_mj(z: float) -> float:
    """
    Spiegel et al. (2011) Z-dependent deuterium-burning minimum mass [M_J].

    M_DB(Z) = 3407 Z² − 271 Z + 16.3. Anchors: M_DB(0) = 16.3 M_J;
    M_DB(0.0152) ≈ 13.0 M_J at solar Z; M_DB(0.045) ≈ 11.0 M_J at 3 Z⊙.
    """
    if z < 0.0:
        raise ValueError("Metallicity Z must be non-negative.")
    return 3407.0 * z * z - 271.0 * z + 16.3


def gas_giant_upper_mass_kg(z: float) -> float:
    """Upper planetary mass for gas-giant regime [kg] at stellar metallicity Z."""
    return m_deuterium_burning_mj(z) * M_JUPITER_KG


def classify_regime(M_kg: float, Z: float) -> str:
    """
    Classify mass into one of five compositional regimes.

    Parameters
    ----------
    M_kg : float
        Planetary mass [kg].
    Z : float
        Stellar metal mass fraction from Variable 03 (Spiegel boundary).

    Returns one of: 'dwarf', 'rocky', 'sub_neptune', 'gas_giant', 'brown_dwarf'.
    """
    if M_kg < DWARF_ROCKY_BOUNDARY_KG:
        return "dwarf"
    if M_kg <= ROCKY_SUBNEPTUNE_BOUNDARY_KG:
        return "rocky"
    if M_kg <= SUBNEPTUNE_GASGIANT_BOUNDARY_KG:
        return "sub_neptune"
    if M_kg <= gas_giant_upper_mass_kg(Z):
        return "gas_giant"
    return "brown_dwarf"
