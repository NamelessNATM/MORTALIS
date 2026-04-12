# variable_06_tectonics/tidal_heating.py
#
# FORMULA:
#   n        = 2*pi / T_orb
#   P_tidal  = (21/2) * (k2/Q) * G * M_star**2 * R**5 * n * e**2 / a**6
#
# SOURCE: Watson et al. (1981); orbital mechanics tidal dissipation.
#         Valid for small eccentricity (e << 1) and synchronous rotation.
#         V06 research Section 3.3.
#
# ⚠️ EARTH FALLBACK — Q = 100, k2 = 0.3 (same as tidal_locking.py).
# Io calibration: Q_Io ≈ 36, k2_Io ≈ 0.3 → P_tidal ≈ 5.2e13 W (target ~1e14 W) ✓
# Static Q assumption hides dynamic thermal-orbital feedback — see Flag note below.
#
# FLAGS:
#   ⚠️ EARTH FALLBACK on Q and k2. If P_tidal is large relative to H_rad, the mantle
#   may be partially molten and Q would drop significantly, increasing P_tidal further.
#   The formula implements a static, non-coupled calculation. Flag for review on
#   high-eccentricity, close-orbit bodies.
#
# EARTH CALIBRATION:
#   Earth-Sun e=0.0167: P_tidal << 1e12 W (negligible; Earth is not Io-like) ✓
#   Io calibration: M_star=M_Jup=1.898e27 kg, R=1.822e6 m, e=0.0041, a=4.218e8 m,
#   T_orb=152842 s → P_tidal ≈ 5.2e13 W (target ~1e14 W; within Q uncertainty) ✓

import math

from constants import G

_K2 = 0.3  # ⚠️ EARTH FALLBACK
_Q = 100.0  # ⚠️ EARTH FALLBACK


def compute_tidal_heating(
    M_star: float,
    R: float,
    a: float,
    e: float,
    T_orb: float,
) -> float:
    """
    Compute tidal heating power from orbital eccentricity dissipation.

    Parameters
    ----------
    M_star : float — stellar mass [kg]
    R      : float — planetary radius [m]
    a      : float — semimajor axis [m]
    e      : float — orbital eccentricity [dimensionless]
    T_orb  : float — orbital period [s]

    Returns
    -------
    P_tidal : float — tidal heating power [W]
    """
    n = 2.0 * math.pi / T_orb
    return (21.0 / 2.0) * (_K2 / _Q) * G * M_star**2 * R**5 * n * e**2 / a**6
