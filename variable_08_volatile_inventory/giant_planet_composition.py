# variable_08_volatile_inventory/giant_planet_composition.py
#
# Hydrogen–helium envelope metallicity scaling for gas-rich planets.
#
# Formula: E_Z = 6.3 × (M/M_J)^−0.71; Z_planet = E_Z × Z_star; protosolar X=0.711, Y=0.274
# Source: Thorngren et al. (2016), Welbanks et al. (2019); standard stellar abundances
# Jupiter calibration: E_Z=6.3 ✓; Saturn: E_Z=14.9 ✓; Uranus/Neptune: E_Z~56 ✓

M_JUPITER_KG = 1.898e27
Z_SUN = 0.014  # solar metallicity — Asplund et al. (2009)
E_Z_COEFF = 6.3  # Thorngren et al. (2016)
E_Z_EXPONENT = -0.71
X_PROTO = 0.711  # protosolar H mass fraction
Y_PROTO = 0.274  # protosolar He mass fraction


def compute_giant_composition(M_kg: float, regime: str) -> dict:
    """
    Envelope metallicity and simplified H2/He speciation.
    Caller must only invoke for gas_giant or sub_neptune with primary_retained.
    """
    if regime not in ("gas_giant", "sub_neptune"):
        return {}

    e_z = E_Z_COEFF * (M_kg / M_JUPITER_KG) ** E_Z_EXPONENT
    z_planet = e_z * Z_SUN
    # Simplified protosolar H2/He — trace volatiles deferred
    speciation = {"H2": X_PROTO, "He": Y_PROTO}
    return {
        "E_Z": e_z,
        "Z_planet": z_planet,
        "X_H": X_PROTO,
        "Y_He": Y_PROTO,
        "speciation": speciation,
    }
