# map_generator/renderer.py
#
# PURPOSE: Render the grid to a 4096x2048 PNG.
#
# At Variables 01-02 stage, the entire surface is uniform — one colour
# representing the planetary regime. The colour palette is defined here
# and will remain stable as future variables add layers.
#
# Regime colour palette (RGB):
#   dwarf        — (160, 140, 120)   warm grey-brown
#   rocky        — (180,  90,  50)   terracotta
#   sub_neptune  — ( 70, 130, 180)   steel blue
#   gas_giant    — (210, 160,  80)   amber
#   brown_dwarf  — ( 60,  40,  80)   deep violet
#   unknown      — (  0,   0,   0)   black

import os

import numpy as np
from PIL import Image

REGIME_COLOURS = {
    0: (160, 140, 120),  # dwarf
    1: (180, 90, 50),  # rocky
    2: (70, 130, 180),  # sub_neptune
    3: (210, 160, 80),  # gas_giant
    4: (60, 40, 80),  # brown_dwarf
}
DEFAULT_COLOUR = (0, 0, 0)


def render(grid: dict, meta: dict, png_path: str) -> None:
    """
    Render the grid regime_id layer to a PNG.

    Parameters
    ----------
    grid     : dict of numpy arrays (must contain 'regime_id')
    meta     : dict of scalar metadata
    png_path : output file path (should end in .png)
    """
    regime_id = grid["regime_id"]
    H, W = regime_id.shape

    canvas = np.zeros((H, W, 3), dtype=np.uint8)

    for rid, colour in REGIME_COLOURS.items():
        mask = regime_id == rid
        canvas[mask] = colour

    # Any cell with an unrecognised regime_id gets default colour
    known_mask = np.isin(regime_id, list(REGIME_COLOURS.keys()))
    canvas[~known_mask] = DEFAULT_COLOUR

    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    img = Image.fromarray(canvas, mode="RGB")
    img.save(png_path)
