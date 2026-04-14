# variable_08_volatile_inventory/snow_lines.py
#
# Snow-line radii for major volatile carriers in a viscously heated protoplanetary disk.
#
# Formula: R_snow,H2O = 2.7 × (M_star/M_☉)² AU; R_snow,i = R_snow,H2O × (170/T_cond,i)²
# Source: viscously-heated disk power-law, calibrated to solar system architecture
# Earth calibration: H2O=2.7 AU, CO2=10.08 AU, CO/CH4/N2=38.5 AU at 1 M_☉
# Flag 102: 2.7 AU coefficient — Earth fallback. Solar System snow line calibration.
# Flag 103: T_cond values (170 K, 88 K, 45 K) — nebular-pressure condensation temperatures.
#           Solar System calibrated.
# Flag 104: M² scaling breaks down above ~5 M_☉. Model applicability limit.

M_SUN_KG = 1.989e30  # kg — fundamental constant
AU_M = 1.496e11  # m — fundamental constant
R_SNOW_H2O_SOLAR_AU = 2.7  # AU at 1 M_sun — Flag 102
T_COND = {  # K — Flag 103
    "H2O": 170.0,
    "CO2": 88.0,
    "CO_CH4_N2": 45.0,
}


def compute_snow_lines(M_star_kg: float) -> dict:
    """Snow-line radii in AU and metres for H2O, CO2, and N2 (CO_CH4_N2 group)."""
    m_ratio = M_star_kg / M_SUN_KG
    r_snow_h2o_au = R_SNOW_H2O_SOLAR_AU * m_ratio**2
    r_snow_h2o_m = r_snow_h2o_au * AU_M

    f_co2 = (170.0 / T_COND["CO2"]) ** 2
    r_snow_co2_au = r_snow_h2o_au * f_co2
    r_snow_co2_m = r_snow_co2_au * AU_M

    f_n2 = (170.0 / T_COND["CO_CH4_N2"]) ** 2
    r_snow_n2_au = r_snow_h2o_au * f_n2
    r_snow_n2_m = r_snow_n2_au * AU_M

    return {
        "R_snow_H2O_AU": r_snow_h2o_au,
        "R_snow_H2O_m": r_snow_h2o_m,
        "R_snow_CO2_AU": r_snow_co2_au,
        "R_snow_CO2_m": r_snow_co2_m,
        "R_snow_N2_AU": r_snow_n2_au,
        "R_snow_N2_m": r_snow_n2_m,
    }
