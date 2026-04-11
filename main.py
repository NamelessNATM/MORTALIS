# MORTALIS World Generation Engine
# Entry point. Orchestrates the variable cascade in order.
# Contains no physics. All physics lives in variable sub-function files.

from variable_01_mass.variable_01_mass import run as run_variable_01


def run(seed: int):
    v01 = run_variable_01(seed)
    return v01
