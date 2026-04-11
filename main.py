# MORTALIS World Generation Engine
# Entry point. Orchestrates the variable cascade in order.
# Contains no physics. All physics lives in variable sub-function files.

from variable_01_mass.variable_01_mass import run as run_variable_01
from variable_02_composition.variable_02_composition import run as run_variable_02


def run(seed: int):
    v01 = run_variable_01(seed)
    v02 = run_variable_02(seed, v01["M_kg"], v01["mu"])
    return {"v01": v01, "v02": v02}
