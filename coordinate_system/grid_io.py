# coordinate_system/grid_io.py
#
# PURPOSE: Save and load the grid data structure to/from .npz on disk.
# The .npz format stores all numpy arrays in a single compressed file.
# Meta scalars are stored as zero-dimensional arrays for portability.

import os

import numpy as np


def save_grid(grid: dict, meta: dict, path: str) -> None:
    """
    Save grid arrays and meta scalars to a .npz file.

    Parameters
    ----------
    grid : dict of numpy arrays
    meta : dict of scalars
    path : output file path (should end in .npz)
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {}
    for k, v in grid.items():
        payload[f"grid__{k}"] = v
    for k, v in meta.items():
        payload[f"meta__{k}"] = np.array(v)
    np.savez_compressed(path, **payload)


def load_grid(path: str) -> tuple:
    """
    Load grid arrays and meta scalars from a .npz file.

    Returns
    -------
    grid : dict of numpy arrays
    meta : dict of scalars
    """
    data = np.load(path, allow_pickle=False)
    grid = {}
    meta = {}
    for key in data.files:
        if key.startswith("grid__"):
            grid[key[6:]] = data[key]
        elif key.startswith("meta__"):
            val = data[key]
            meta[key[6:]] = val.item() if val.ndim == 0 else val
    return grid, meta
