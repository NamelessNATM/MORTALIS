# variable_08_volatile_inventory/outgassing_integral.py
#
# Time-integrated volcanic outgassing from melt–vapor partitioning.
#
# Formula: M_outgassed,i = R_melt × X_melt,i × ε × age × 3.154×10¹⁶ s/Gyr
#          X_melt,i = X_mantle,i / F_bar (volatile concentration in melt)
# Earth calibration: M_outgassed,N2=3.83×10¹⁸ kg, M_outgassed,H2O=1.37×10²¹ kg ✓
# Flag 129: ε_mobile=1.0 (referenced from melt_fraction.py — no new flag)

S_PER_GYR = 3.154e16  # s/Gyr

# Molar masses (kg/mol) — prompt gives g/mol
MW = {
    "H2O": 18.015e-3,
    "CO2": 44.010e-3,
    "CO": 28.010e-3,
    "H2": 2.016e-3,
    "N2": 28.014e-3,
    "SO2": 64.066e-3,
    "H2S": 34.082e-3,
    "CH4": 16.043e-3,
    "NH3": 17.031e-3,
}


def compute_outgassing(
    R_melt_kgs: float | None,
    X_mantle: dict,
    speciation: dict | None,
    F_bar: float,
    epsilon: float,
    age_Gyr: float,
) -> dict:
    """Integrate outgassed mass over geological time; species masses from mass-weighted speciation."""
    if (
        F_bar <= 0.0
        or R_melt_kgs is None
        or R_melt_kgs <= 0.0
        or speciation is None
    ):
        return {
            "M_outgassed_total_kg": 0.0,
            "M_outgassed_per_species": {},
            "X_melt_H_ppm": 0.0,
            "X_melt_C_ppm": 0.0,
            "outgassing_note": "no melt — zero outgassing",
        }

    x_mh = X_mantle.get("X_mantle_H_ppm", 0.0) / F_bar
    x_mc = X_mantle.get("X_mantle_C_ppm", 0.0) / F_bar
    x_mn = X_mantle.get("X_mantle_N_ppm", 0.0) / F_bar
    x_ms = X_mantle.get("X_mantle_S_ppm", 0.0) / F_bar

    sum_el = (x_mh + x_mc + x_mn + x_ms) * 1e-6
    m_total = (
        R_melt_kgs * sum_el * epsilon * age_Gyr * S_PER_GYR
    )

    denom_mw = 0.0
    for sp, xm in speciation.items():
        if sp in MW:
            denom_mw += xm * MW[sp]
    if denom_mw <= 0.0:
        return {
            "M_outgassed_total_kg": 0.0,
            "M_outgassed_per_species": {},
            "X_melt_H_ppm": x_mh,
            "X_melt_C_ppm": x_mc,
            "outgassing_note": "invalid speciation weights",
        }

    per = {}
    for sp, xm in speciation.items():
        if sp not in MW:
            continue
        w_mass = (xm * MW[sp]) / denom_mw
        per[sp] = m_total * w_mass

    return {
        "M_outgassed_total_kg": m_total,
        "M_outgassed_per_species": per,
        "X_melt_H_ppm": x_mh,
        "X_melt_C_ppm": x_mc,
        "outgassing_note": "outgassing integrated",
    }
