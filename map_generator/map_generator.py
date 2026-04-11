# map_generator/map_generator.py
#
# Entry point for the map generator.
# Imports sub-functions. Assembles outputs. Contains no physics.

from map_generator.renderer import render


def run(grid: dict, meta: dict, png_path: str) -> None:
    """
    Render the current grid state to a PNG.

    Parameters
    ----------
    grid     : dict of numpy arrays
    meta     : dict of scalar metadata
    png_path : str — output path
    """
    render(grid, meta, png_path)
