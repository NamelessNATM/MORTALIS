# variable_09_atmospheric_column/joined_solution_t_surface.py
#
# Robinson & Catling (2012) joined-solution surface temperature.

def compute_t_surface(T_skin, tau_zero, tau_rc, beta, n, D=1.5):
    """
    Joined-solution surface temperature for radiative-convective equilibrium.

    Source: Robinson & Catling (2012), ApJ 757, 104, joined-solution form
    derived in Scaffold 013 research cycle (Follow-up 2, §2.2).

    T_surface = T_skin · (tau_zero/tau_rc)^(beta/n) · (1 + D·tau_rc)^(1/4)

    Earth calibration: T_skin=214.4 K, tau_zero=1.86, tau_rc≈0.1, beta=0.19, n=2
        → T_surface = 293.0 K (observed: 288 K, +5 K within ±10 K target)
    Titan calibration: T_skin_eff=69 K, tau_zero=2.0, tau_rc≈0.1, beta=0.20, n=2
        → T_surface = 96.4 K (observed: 94 K, +2.4 K within ±5% target)
    Venus calibration: T_skin=195.1 K, tau_zero=400, tau_rc=1.0, beta=0.1643, n=1
        → T_surface = 658.4 K (observed: 737 K, -10.7%, GRAY-MODEL LIMIT)
    """
    return (
        float(T_skin)
        * (float(tau_zero) / float(tau_rc)) ** (float(beta) / float(n))
        * (1.0 + float(D) * float(tau_rc)) ** 0.25
    )


def compute_t_surface_gas_envelope(
    F_solar_W_m2, tau_rc, tau_zero, beta, n, F_int_W_m2, D=1.5
):
    """
    Deep-boundary joined form with internal heat (Follow-Up 2 Q1c).

    T_surface_gas = ((F_solar/2 · (1 + D·τ_rc) + F_int) / σ)^(1/4)
                    · (τ_zero/τ_rc)^(β/n)

    σ — Stefan–Boltzmann constant [W m⁻² K⁻⁴] (Rule 1 Category A).
    """
    import math

    sigma = 5.670e-8
    flux = 0.5 * float(F_solar_W_m2) * (1.0 + float(D) * float(tau_rc))
    if F_int_W_m2 is not None:
        flux += float(F_int_W_m2)
    t_rad = (flux / sigma) ** 0.25
    return t_rad * (float(tau_zero) / float(tau_rc)) ** (float(beta) / float(n))
