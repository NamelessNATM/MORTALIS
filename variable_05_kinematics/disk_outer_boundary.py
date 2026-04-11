# variable_05_kinematics/disk_outer_boundary.py
#
# PURPOSE: Compute the outer boundary of stable planetary orbits from
# ALMA gas disk size scaling.
#
# Formula: a_max = R_0 * (M_star / M_sun)^gamma
#   R_0 = 100 AU = 1.496e13 m
#   gamma = 0.5
#
# Source: Andrews et al. (2018) ALMA survey of protoplanetary disks;
# gas disk radii (CO line emission) scale with stellar mass. Parameters
# fitted to Lupus star-forming region.
#
# 1 M_sun calibration: a_max = 100 AU. Physically reasonable — Solar System
# outer disk analogues (Kuiper Belt) extend to ~50 AU, within this bound.
#
# ⚠️ Flag 31: a_max uses ALMA gas disk size scaling (Andrews et al. 2018).
# Parameters vary between star-forming regions. SINGLE-SURVEY APPROXIMATION.
# Candidate C (internal photoevaporation gravitational radius) was rejected
# because it produces a_max = 9.2 AU for 1 M_sun, excluding outer solar
# system analogues (Uranus at 19 AU, Neptune at 30 AU).

M_SUN_KG = 1.989e30
AU_M = 1.496e11

R_0_M = 100.0 * AU_M   # 100 AU in metres
GAMMA = 0.5             # ⚠️ Flag 31 — single-survey fitted exponent


def compute_disk_outer_boundary(M_star_kg: float) -> float:
    """
    Outer disk boundary a_max [m].

    Parameters
    ----------
    M_star_kg : stellar mass [kg] from Variable 03

    Returns
    -------
    a_max [m]
    """
    return R_0_M * (M_star_kg / M_SUN_KG) ** GAMMA
