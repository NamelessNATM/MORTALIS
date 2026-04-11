# coordinate_system/coordinate_system.py
#
# Entry point for the coordinate system.
# Imports sub-functions. Assembles outputs. Contains no physics.

from coordinate_system.grid_builder import build_grid
from coordinate_system.grid_io import save_grid


def run(v02: dict, npz_path: str) -> tuple:
    """
    Build the planetary grid from Variable 02 outputs and save to disk.

    Parameters
    ----------
    v02      : dict — output of variable_02_composition.run()
    npz_path : str  — path to write the .npz file

    Returns
    -------
    grid : dict of numpy arrays
    meta : dict of scalar metadata
    """
    grid, meta = build_grid(v02)
    save_grid(grid, meta, npz_path)
    return grid, meta
