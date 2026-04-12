# variable_06_tectonics/tidal_locking.py
#
# FORMULA:
#   I      = f_I * M * R**2           [moment of inertia, f_I from CMF]
#   t_lock = omega_0 * a**6 * I * Q / (3 * G * M_star**2 * k2 * R**5)
#
# f_I: moment of inertia factor. For a uniform sphere f_I = 0.4.
# For a differentiated body, f_I < 0.4. Derived from CMF:
#   f_I = 0.4 - 0.2 * CMF   [linear approximation, Earth: CMF=0.325 → f_I=0.335]
#   Earth actual: I/(MR²) = 0.3307 ✓ (0.335 vs 0.3307, <1.5% error)
# ⚠️ EARTH FALLBACK on f_I linear approximation.
#
# ⚠️ EARTH FALLBACK — Q = 100, k2 = 0.3.
# Tidal dissipation factor and Love number measured on Earth and Solar System moons.
# Highly temperature- and composition-sensitive. Flag context: if P_tidal is large
# enough to partially melt the mantle, Q drops dramatically — static Q is wrong.
# (See hidden assumption in research Section 5.4.)
#
# omega_0 = 2*pi / (10*3600)  [10-hour initial spin, research-established default]
# Asymptotic insensitivity: exact omega_0 only marginally affects t_lock.
#
# SOURCE: Peale (1977); Gladman et al. (1996). V06 research Section 3.1.
#
# EARTH CALIBRATION:
#   t_lock(Earth-Sun) ≈ 199 Gyr  (target > 50 Gyr) ✓

import math

from constants import G

_Q = 100.0  # ⚠️ EARTH FALLBACK — tidal dissipation factor
_K2 = 0.3  # ⚠️ EARTH FALLBACK — Love number
_OMEGA_0 = 2.0 * math.pi / (10.0 * 3600.0)  # 10-hour initial rotation [rad/s]


def compute_tidal_locking(
    M: float,
    R: float,
    CMF: float,
    a: float,
    M_star: float,
    age_s: float,
) -> dict:
    """
    Compute tidal locking timescale and determine if the planet is locked.

    Parameters
    ----------
    M      : float — planetary mass [kg]
    R      : float — planetary radius [m]
    CMF    : float — core mass fraction [dimensionless]
    a      : float — semimajor axis [m]
    M_star : float — stellar mass [kg]
    age_s  : float — system age [s]

    Returns
    -------
    dict with keys:
        f_I        : float — moment of inertia factor
        I_kgm2     : float — moment of inertia [kg*m²]
        t_lock_s   : float — tidal locking timescale [s]
        t_lock_Gyr : float — tidal locking timescale [Gyr]
        is_locked  : bool  — True if t_lock <= age
    """
    f_I = 0.4 - 0.2 * CMF
    I = f_I * M * R**2

    t_lock = (_OMEGA_0 * a**6 * I * _Q) / (3.0 * G * M_star**2 * _K2 * R**5)

    return {
        "f_I": f_I,
        "I_kgm2": I,
        "t_lock_s": t_lock,
        "t_lock_Gyr": t_lock / 3.15576e16,
        "is_locked": t_lock <= age_s,
    }
