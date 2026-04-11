# variable_05_kinematics/stellar_flux.py
#
# PURPOSE: Compute orbit-averaged stellar flux and XUV flux at the planet.
#
# Formula (bolometric): <F> = L_star / (4 * pi * a^2 * sqrt(1 - e^2))
#
# Derivation: Instantaneous flux F(r) = L / (4*pi*r^2). For an eccentric
# orbit, time-averaging using Kepler's Second Law (r^2 dtheta = h dt)
# transforms the time integral to an integral over true anomaly, yielding
# the (1 - e^2)^(-1/2) correction factor. Universally applicable.
# Source: Murray & Dermott (1999) Solar System Dynamics.
#
# Earth calibration:
#   L = 3.828e26 W, a = 1.496e11 m, e = 0.0167
#   <F> = 3.828e26 / (4*pi*(1.496e11)^2 * sqrt(1-0.0167^2))
#        = 3.828e26 / (2.812e23) = 1361.3 W/m^2 ✓ (known 1361 W/m^2)

import math

PI = math.pi


def compute_stellar_flux(L_star_W: float, a_m: float, e: float) -> float:
    """
    Orbit-averaged stellar flux <F> [W/m^2].

    Parameters
    ----------
    L_star_W : stellar bolometric luminosity [W] from Variable 03
    a_m      : semimajor axis [m]
    e        : orbital eccentricity [dimensionless]

    Returns
    -------
    <F> [W/m^2]
    """
    denom = 4.0 * PI * a_m * a_m * math.sqrt(1.0 - e * e)
    return L_star_W / denom


def compute_xuv_flux(L_XUV_W: float, a_m: float, e: float) -> float:
    """
    Orbit-averaged XUV flux F_XUV [W/m^2].

    Same formula as bolometric flux with L_XUV substituted.
    Source: same derivation — orbit-averaged inverse-square law.

    Earth calibration:
      L_XUV ~ 9.08e-6 * 3.828e26 = 3.477e21 W (from Variable 03 seed 1)
      At 1 AU, e=0: F_XUV = 3.477e21 / (4*pi*(1.496e11)^2)
                           = 3.477e21 / 2.812e23 = 0.01236 W/m^2
      Solar XUV flux at Earth ~0.005-0.01 W/m^2 -- order of magnitude ✓
    """
    denom = 4.0 * PI * a_m * a_m * math.sqrt(1.0 - e * e)
    return L_XUV_W / denom
