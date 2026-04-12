# variable_05_kinematics/equilibrium_temperature.py
#
# PURPOSE: Compute planetary equilibrium temperature from orbit-averaged flux.
#
# Formula: T_eq = ((1 - A_proxy) * <F> / (4 * sigma))^(1/4)
#
# Derivation: Energy balance between absorbed stellar radiation and blackbody
# emission. Incoming power: (1-A) * <F> * pi * R^2. Emitted power (rapid
# rotator, uniform emission): 4 * pi * R^2 * sigma * T^4. Setting equal
# and solving for T yields the formula. R cancels — T_eq is independent
# of planetary radius. Source: Selsis et al. (2007); universal physics.
#
# Bond albedo: Pass 1 proxy A_proxy is supplied by bond_albedo.compute_pass1_albedo
# before this call. Pass 2 refinement (Del Genio et al. 2019, etc.) runs in
# main.py after Variable 04 and overwrites v05['T_eq_K'] when applicable.
#
# Earth calibration (Pass 1):
#   A_proxy = 0.15 (Pass 1 silicate-iron), <F> = 1361 W/m^2, sigma = CODATA (below)
#   T_eq^(0) = ((0.85 * 1361) / (4 * sigma))^0.25 ≈ 266.7 K
#
# CERES / observed Earth (Pass 2 / observation, not output of this function):
#   A_B = 0.306 → T_eq = 254.0 K

SIGMA = 5.670374419e-8  # W m^-2 K^-4 — CODATA Stefan-Boltzmann constant


def compute_equilibrium_temperature(F_mean_W_m2: float, A_proxy: float) -> float:
    """
    Equilibrium temperature T_eq [K] from orbit-averaged flux and Pass 1 albedo.

    Parameters
    ----------
    F_mean_W_m2 : orbit-averaged stellar flux [W/m^2]
    A_proxy       : Bond albedo proxy from Pass 1 (bond_albedo)

    Returns
    -------
    T_eq_K : float — equilibrium temperature [K]
    """
    return ((1.0 - A_proxy) * F_mean_W_m2 / (4.0 * SIGMA)) ** 0.25
