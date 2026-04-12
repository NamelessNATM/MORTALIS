# variable_04_atmosphere/jeans_parameter.py
#
# PURPOSE: Compute the Jeans escape parameter lambda for each atmospheric
# species and determine which species are retained over geological timescales.
#
# Formula: lambda = v_e² / v_th²   where v_th = sqrt(2 * k_B * T_exo / m)
# Equivalently: lambda = G * M * m / (k_B * T_exo * R)
#
# Derivation: Ratio of gravitational binding energy to thermal kinetic energy
# at the exobase, from the Maxwell-Boltzmann velocity distribution.
# Source: Chamberlain & Hunten (1987).
#
# lambda_crit = 15–20: species with lambda > lambda_crit are retained over Gyr
# timescales. Not a hard physical constant — a time-integrated statistical
# threshold confirmed empirically across Solar System atmospheres.
# Source: Chamberlain & Hunten (1987). (Flag 27)
#
# Earth calibration:
#   v_e = 11,186 m/s, T_exo = 1,000 K
#   H:  v_th = 4,064 m/s → lambda = 7.57  (escapes — correct ✓)
#   O:  v_th = 1,019 m/s → lambda = 120.3 (retained — correct ✓)

# Fundamental physical constant (Rule 1 Category A)
K_B = 1.381e-23  # J/K — Boltzmann constant

# Molecular masses [kg] — confirmed universal atomic/molecular masses
SPECIES_MASS_KG = {
    "H":   1.67e-27,
    "He":  6.65e-27,
    "O":   2.66e-26,
    "H2O": 2.99e-26,
    "N2":  4.65e-26,
    "CO2": 7.31e-26,
}

# ⚠️ Flag 27: lambda_crit is a statistical threshold, not a physical constant.
# Confirmed empirically across Solar System atmospheres (Chamberlain & Hunten 1987).
# Scatter exists — some species with lambda ~12–15 may be partially retained.
LAMBDA_CRIT = 15.0


def compute_lambda(v_e_m_s: float, T_exo_K: float, m_kg: float) -> float:
    """
    Jeans escape parameter lambda for a single species.

    Parameters
    ----------
    v_e_m_s : escape velocity [m/s] from Variable 02
    T_exo_K : exobase temperature [K] from exobase_temperature.py
    m_kg    : molecular mass of species [kg]

    Returns
    -------
    lambda [dimensionless]
    """
    v_th_sq = 2.0 * K_B * T_exo_K / m_kg
    return (v_e_m_s ** 2) / v_th_sq


def compute_all_species(v_e_m_s: float, T_exo_K: float) -> dict:
    """
    Jeans parameter for all tracked species.

    Returns
    -------
    dict mapping species name -> {'lambda': float, 'retained': bool}
    """
    results = {}
    for species, m_kg in SPECIES_MASS_KG.items():
        lam = compute_lambda(v_e_m_s, T_exo_K, m_kg)
        results[species] = {
            "lambda": lam,
            "retained": lam >= LAMBDA_CRIT,
        }
    return results
