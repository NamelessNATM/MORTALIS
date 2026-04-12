# variable_06_tectonics/accretional_energy.py
#
# FORMULA:
#   E_acc   = (3/5) * G * M**2 / R        [Gravitational binding energy of uniform sphere]
#   dE_core = 0.04 * G * M**2 / R         [Differentiation energy release, analytic estimate]
#   E_total = E_acc + dE_core
#
# SOURCE: Standard gravitational physics (Rule 1 Category A).
#         dE_core coefficient from research session V06 Section 1.1.
#         dE_core = 0.04 GM²/R is an order-of-magnitude analytic estimate, not a
#         precisely derived universal constant.
#         ⚠️ EARTH FALLBACK on dE_core coefficient — calibrated to terrestrial
#         differentiation models. Universal applicability not confirmed.
#
# EARTH CALIBRATION:
#   M = 5.97e24 kg, R = 6.37e6 m
#   E_acc   ≈ 2.24e32 J  ✓ (target ~2.2e32 J)
#   dE_core ≈ 1.49e31 J
#   E_total ≈ 2.39e32 J

from constants import G


def compute_accretional_energy(M: float, R: float) -> dict:
    """
    Compute total gravitational heat budget from accretion and differentiation.

    Parameters
    ----------
    M : float — planetary mass [kg]
    R : float — planetary radius [m]

    Returns
    -------
    dict with keys:
        E_acc_J   : float — gravitational binding energy [J]
        dE_core_J : float — differentiation energy release [J]
        E_total_J : float — combined heat budget [J]
    """
    E_acc = (3 / 5) * G * M**2 / R
    dE_core = 0.04 * G * M**2 / R
    E_total = E_acc + dE_core

    return {
        "E_acc_J": E_acc,
        "dE_core_J": dE_core,
        "E_total_J": E_total,
    }
