# calibrate_tm0.py
# Binary search for T_m(0) that gives T_m(4.5 Gyr) = 1650 K at Earth inputs.
# Reports the calibrated _TM0 value to update in mantle_temperature.py.

import math
import sys

sys.path.insert(0, ".")

from variable_06_tectonics.radiogenic_heating import compute_radiogenic_heating
from variable_06_tectonics.mantle_viscosity import (
    compute_mantle_viscosity,
    compute_frank_kamenetskii,
    compute_solidus,
)
from variable_06_tectonics.rayleigh_number import compute_rayleigh_number
from variable_06_tectonics.tectonic_regime import classify_tectonic_regime
from variable_06_tectonics.surface_heat_flux import compute_surface_heat_flux

# Earth inputs
M = 5.97e24
CMF = 0.325
R = 6.371e6
T_eq = 255.0
D = 2.878e6
P_cmb = 1.229e11  # 122.9 GPa from Earth diagnostic
age_Gyr = 4.5

rho_mantle = 4457.0
g = 9.807

M_mantle = M * (1.0 - CMF)
N_STEPS = 1000
CP = 1200.0
T_SOLIDUS = compute_solidus(P_cmb)


def integrate(TM0):
    T_m = TM0
    dt_Gyr = age_Gyr / N_STEPS
    dt_s = dt_Gyr * 3.15576e16
    for step in range(N_STEPS):
        t_Gyr = step * dt_Gyr
        H_rad = compute_radiogenic_heating(M_mantle, t_Gyr)
        eta = compute_mantle_viscosity(T_m)
        theta = compute_frank_kamenetskii(T_m, T_eq)
        Ra_d = compute_rayleigh_number(rho_mantle, g, T_m, T_eq, D, eta)
        t_reg = classify_tectonic_regime(Ra_d["Ra"], Ra_d["Ra_c"])
        q_s, _ = compute_surface_heat_flux(
            T_m,
            T_eq,
            D,
            Ra=Ra_d["Ra"],
            Ra_c=Ra_d["Ra_c"],
            theta=theta,
            tectonic_regime=t_reg,
            convecting=Ra_d["convecting"],
        )
        q_total = 4.0 * math.pi * R**2 * q_s
        dT = (H_rad - q_total) / (M_mantle * CP) * dt_s
        T_m = max(T_eq, T_m + dT)
        if T_m >= T_SOLIDUS:
            T_m = T_SOLIDUS
            break
    return T_m


# Binary search for T_m(0) giving T_m(4.5 Gyr) = 1650 K
TARGET = 1650.0
lo, hi = 1700.0, 2500.0
for _ in range(60):
    mid = (lo + hi) / 2.0
    result = integrate(mid)
    if result < TARGET:
        lo = mid
    else:
        hi = mid

TM0_calibrated = (lo + hi) / 2.0
TM_final = integrate(TM0_calibrated)

print(f"Calibrated T_m(0) : {TM0_calibrated:.1f} K")
print(f"T_m at 4.5 Gyr    : {TM_final:.1f} K  (target 1650 K)")
print(f"Update _TM0 in mantle_temperature.py to: {TM0_calibrated:.1f}")
