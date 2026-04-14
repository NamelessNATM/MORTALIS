# variable_08_volatile_inventory/elemental_partitioning.py
#
# Elemental bulk abundances (ppm) in accreting silicate + ice.
#
# Formula: X_bulk,i = X_dry × f_i,dry + X_ice,i(a_m)
# Source: EH3 unequilibrated chondrites (least thermally altered inner solar system analog)
# Earth calibration: X_bulk,H=8 ppm, X_bulk,C=67 ppm, X_bulk,N=8 ppm, X_bulk,S=916 ppm at X_vol=1e-3
# Flag 107: EH3 fractions — Solar System meteoritic measurements. Earth fallback.

# ⚠️ Flag 107 — EH3 enstatite chondrite elemental fractions (normalized to 1.0)
F_DRY = {
    "S": 0.916,
    "C": 0.067,
    "H": 0.008,
    "N": 0.008,
    "Ar": 2.0e-7,
}


def compute_elemental_bulk(
    X_dry: float,
    X_ice_H2O: float,
    X_ice_CO2: float,
    X_ice_N2: float,
) -> dict:
    """Return bulk elemental mass fractions in ppm (parts per million by mass)."""
    x_bulk_h = (X_dry * F_DRY["H"] + X_ice_H2O * (2.016 / 18.015)) * 1e6
    x_bulk_c = (X_dry * F_DRY["C"] + X_ice_CO2 * (12.011 / 44.010)) * 1e6
    x_bulk_n = (X_dry * F_DRY["N"] + X_ice_N2 * (28.014 / 28.014)) * 1e6
    x_bulk_s = X_dry * F_DRY["S"] * 1e6
    x_bulk_ar = X_dry * F_DRY["Ar"] * 1e6
    return {
        "X_bulk_H_ppm": x_bulk_h,
        "X_bulk_C_ppm": x_bulk_c,
        "X_bulk_N_ppm": x_bulk_n,
        "X_bulk_S_ppm": x_bulk_s,
        "X_bulk_Ar_ppm": x_bulk_ar,
    }
