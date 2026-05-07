# variable_09_atmospheric_column/tau_rc_implicit_solver.py
#
# Robinson & Catling (2012) Eq. 31 implicit equation for τ_rc.

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import gamma, gammaincc


def compute_tau_rc_implicit(beta: float, n: float, D: float = 1.5) -> float:
    """
    Solve Γ(1 + 4β/n, D·τ_rc) / (D·τ_rc)^(4β/n) · exp(-D·τ_rc)
        = (2 + D·τ_rc) / (1 + D·τ_rc)
    for τ_rc ∈ [1e-3, 100].

    Uses Γ(a,x) = γ(a,x) complement via scipy.special.gammaincc(a,x)*Γ(a).
    """
    a = 1.0 + 4.0 * float(beta) / float(n)

    def lhs(tau_rc: float) -> float:
        x = float(D) * float(tau_rc)
        if x <= 0.0 or tau_rc <= 0.0:
            return float("nan")
        # Γ(a,x) / x^(4β/n) * exp(-x)  with x = D τ_rc
        gam_upper = gamma(a) * gammaincc(a, x)
        expo = 4.0 * float(beta) / float(n)
        return gam_upper / (x**expo) * math.exp(-x)

    def residual(tau_rc: float) -> float:
        x = float(D) * float(tau_rc)
        return lhs(tau_rc) - (2.0 + x) / (1.0 + x)

    try:
        root = brentq(residual, 1e-3, 100.0, xtol=1e-10, rtol=1e-10)
    except ValueError as e:
        raise RuntimeError(
            f"Rule 2: τ_rc implicit solver failed for beta={beta}, n={n}: {e}"
        ) from e
    if not (1e-3 <= root <= 100.0):
        raise RuntimeError(
            f"Rule 2: τ_rc={root} outside solver bracket [1e-3, 100] "
            f"(beta={beta}, n={n})."
        )
    return float(root)
