# outputs/manifest.py
#
# PURPOSE: Track versioned output files per seed.
# Reads and writes a JSON manifest at outputs/world_{seed}_manifest.json.
# Each run increments the version counter and records which variables
# were active.

import json
import os

OUTPUTS_DIR = "outputs"


def _manifest_path(seed: int) -> str:
    return os.path.join(OUTPUTS_DIR, f"world_{seed}_manifest.json")


def next_version(seed: int, active_variables: list) -> tuple:
    """
    Increment the version counter for this seed and return versioned paths.

    Parameters
    ----------
    seed             : int
    active_variables : list of str — e.g. ['v01', 'v02']

    Returns
    -------
    version  : int — the new version number
    npz_path : str
    png_path : str
    """
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    path = _manifest_path(seed)

    if os.path.exists(path):
        with open(path, "r") as f:
            manifest = json.load(f)
    else:
        manifest = {"seed": seed, "version": 0, "history": []}

    manifest["version"] += 1
    version = manifest["version"]

    npz_path = os.path.join(OUTPUTS_DIR, f"world_{seed}_v{version:03d}.npz")
    png_path = os.path.join(OUTPUTS_DIR, f"world_{seed}_v{version:03d}.png")

    manifest["history"].append(
        {
            "version": version,
            "active_variables": active_variables,
            "npz": npz_path,
            "png": png_path,
        }
    )

    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)

    return version, npz_path, png_path
