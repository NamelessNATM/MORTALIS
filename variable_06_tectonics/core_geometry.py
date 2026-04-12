# variable_06_tectonics/core_geometry.py
#
# FORMULA:
#   R_core    = R * (CMF / (CMF + chi * (1 - CMF)))**(1/3)
#   rho_mantle = rho_mean * (1 - CMF + CMF / chi)
#   rho_core   = chi * rho_mantle
#
# where chi = rho_core / rho_mantle ≈ 2.44 (Earth-calibrated density contrast)
#
# SOURCE: V06 Follow-Up A, Question A1. Two-layer mass-volume conservation.
#         Mathematical structure is universally applicable to any differentiated body.
#
# ⚠️ EARTH FALLBACK — chi = 2.44 derived from Earth mean core density (~11,000 kg/m³)
# divided by Earth mean mantle density (~4,500 kg/m³). Universal applicability not
# confirmed. Flag 50 applies.
#
# EARTH CALIBRATION:
#   M = 5.97e24 kg, R = 6.37e6 m, CMF = 0.325, rho_mean = 5515 kg/m³
#   R_core    ≈ 3,487 km  (target ~3,480 km) ✓
#   rho_mantle ≈ 4,457 kg/m³ ✓
#   rho_core   ≈ 10,875 kg/m³ ✓

# ⚠️ EARTH FALLBACK — chi is Earth-calibrated. Flag 50.
_CHI = 2.44  # core-to-mantle density contrast


def compute_core_geometry(R: float, CMF: float, rho_mean: float) -> dict:
    """
    Derive core radius and layer densities from a two-layer mass-volume model.

    Parameters
    ----------
    R        : float — planetary radius [m]
    CMF      : float — core mass fraction [dimensionless]
    rho_mean : float — mean bulk density [kg/m³]

    Returns
    -------
    dict with keys:
        R_core_m      : float — core radius [m]
        rho_mantle_kgm3 : float — mean mantle density [kg/m³]
        rho_core_kgm3   : float — mean core density [kg/m³]
    """
    chi = _CHI
    ratio = CMF / (CMF + chi * (1.0 - CMF))
    R_core = R * ratio ** (1.0 / 3.0)

    rho_mantle = rho_mean * (1.0 - CMF + CMF / chi)
    rho_core = chi * rho_mantle

    return {
        "R_core_m": R_core,
        "rho_mantle_kgm3": rho_mantle,
        "rho_core_kgm3": rho_core,
    }
