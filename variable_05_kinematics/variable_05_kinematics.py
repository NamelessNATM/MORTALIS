# variable_05_kinematics/variable_05_kinematics.py
#
# Variable 05: Planetary Kinematics
# Entry point. Imports sub-functions. Assembles outputs. Contains no physics.
#
# Cascade outputs:
#   a_m          — semimajor axis [m]
#   e            — orbital eccentricity [dimensionless]
#   obliquity_deg— axial tilt [degrees]
#   T_orb_s      — orbital period [s]
#   F_mean_W_m2  — orbit-averaged stellar flux [W/m^2]
#   F_XUV_W_m2   — orbit-averaged XUV flux [W/m^2]
#   T_eq_K       — equilibrium temperature [K] (Pass 1; main may overwrite after V04)
#   T_eq_proxy_K — same as T_eq_K at V05 exit (Pass 1 reference)
#   albedo_proxy — Bond albedo Pass 1 (bond_albedo.compute_pass1_albedo)
#   R_H_m        — Hill radius [m]
#   M_dot_kg_s   — energy-limited atmospheric escape rate [kg/s]
#   a_roche_m    — Roche limit inner boundary [m]
#   a_max_m      — disk outer boundary [m]

from variable_05_kinematics.roche_limit import compute_roche_limit
from variable_05_kinematics.disk_outer_boundary import compute_disk_outer_boundary
from variable_05_kinematics.semimajor_axis_sampler import sample_semimajor_axis
from variable_05_kinematics.orbital_eccentricity_sampler import sample_eccentricity
from variable_05_kinematics.stellar_flux import compute_stellar_flux, compute_xuv_flux
from variable_05_kinematics.bond_albedo import compute_pass1_albedo
from variable_05_kinematics.equilibrium_temperature import compute_equilibrium_temperature
from variable_05_kinematics.hill_radius import compute_hill_radius
from variable_05_kinematics.orbital_period import compute_orbital_period
from variable_05_kinematics.obliquity_sampler import sample_obliquity
from variable_05_kinematics.atmospheric_escape import compute_atmospheric_escape


def run(seed: int, v01: dict, v02: dict, v03: dict) -> dict:
    """
    Execute Variable 05: sample orbital parameters and derive all
    orbital and insolation quantities.

    Parameters
    ----------
    seed : int  — cascade integer seed
    v01  : dict — Variable 01 outputs (M_kg, mu)
    v02  : dict — Variable 02 outputs (regime, R_m, rho_mean_kg_m3, ...)
    v03  : dict — Variable 03 outputs (M_star_kg, mu_star, L_star_W,
                                        R_star_m, L_XUV_W, ...)

    Returns
    -------
    dict with all cascade outputs listed above
    """
    M_kg      = v01['M_kg']
    mu_planet = v01['mu']
    regime    = v02['regime']
    R_m       = v02['R_m'] if v02['R_m'] is not None else 0.0
    rho_mean  = v02['rho_mean_kg_m3'] if v02['rho_mean_kg_m3'] is not None else 3500.0

    M_star_kg = v03['M_star_kg']
    mu_star   = v03['M_star_solar'] * 1.989e30 * 6.674e-11
    L_star_W  = v03['L_star_W']
    R_star_m  = v03['R_star_m']
    L_XUV_W   = v03['L_XUV_W']

    # Orbital boundaries
    a_roche = compute_roche_limit(R_star_m, M_star_kg, rho_mean)
    a_max   = compute_disk_outer_boundary(M_star_kg)

    # Sample orbital elements
    a_m          = sample_semimajor_axis(seed, regime, a_roche, a_max)
    e            = sample_eccentricity(seed, a_m, a_roche)
    obliquity_deg = sample_obliquity(seed)

    # Derived orbital quantities
    T_orb_s     = compute_orbital_period(a_m, mu_star, mu_planet)
    F_mean      = compute_stellar_flux(L_star_W, a_m, e)
    F_XUV       = compute_xuv_flux(L_XUV_W, a_m, e)
    A_proxy = compute_pass1_albedo(
        F_mean_W_m2=F_mean,
        regime=regime,
        v02_composition_tag=v02.get("composition_tag", "silicate-iron"),
        T_eff_K=v03["T_eff_K"],
    )
    T_eq_K = compute_equilibrium_temperature(F_mean, A_proxy)
    R_H_m       = compute_hill_radius(a_m, M_kg, M_star_kg)

    M_dot = 0.0
    if R_m > 0.0 and M_kg > 0.0:
        M_dot = compute_atmospheric_escape(F_XUV, R_m, M_kg, regime)

    return {
        'a_m':           a_m,
        'e':             e,
        'obliquity_deg': obliquity_deg,
        'T_orb_s':       T_orb_s,
        'F_mean_W_m2':   F_mean,
        'F_XUV_W_m2':    F_XUV,
        'T_eq_K':        T_eq_K,
        'T_eq_proxy_K':  T_eq_K,
        'albedo_proxy':  A_proxy,
        'R_H_m':         R_H_m,
        'M_dot_kg_s':    M_dot,
        'a_roche_m':     a_roche,
        'a_max_m':       a_max,
    }
