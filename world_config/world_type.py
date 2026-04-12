# world_config/world_type.py
#
# PURPOSE: Define valid world types, map each to its planetary regime string,
# and validate user-supplied world type input.
#
# World type is a user-facing input. It tells the mass sampler which slice
# of the galactic demographic PDF to draw from. It does not affect any physics.
# The underlying PDF is unchanged — only the CDF renormalization boundaries
# change.
#
# Valid world types and their regime mappings:
#   'rocky'       -> 'rocky'       (4.4 M_earth lower, rocky-subneptune upper)
#   'sub_neptune' -> 'sub_neptune' (rocky-subneptune lower, 127 M_earth upper)
#   'gas_giant'   -> 'gas_giant'   (127 M_earth lower, 13 M_J upper)
#   'dwarf'       -> 'dwarf'       (M_min lower, 1e24 kg upper)
#
# 'brown_dwarf' is excluded — outside planetary atmosphere domain;
# simulation produces no meaningful surface outputs.
#
# None (unrestricted) -> full galactic demographic draw, all regimes.
# This is the default. Used for diagnostic and research runs.
#
# GUI note: CLI args are the current interface. A GUI will be built later
# that supplies the same parameters to world_config at the backend.
# This module does not need to change when the interface changes.

VALID_WORLD_TYPES = ('rocky', 'sub_neptune', 'gas_giant', 'dwarf')

WORLD_TYPE_TO_REGIME = {
    'rocky':       'rocky',
    'sub_neptune': 'sub_neptune',
    'gas_giant':   'gas_giant',
    'dwarf':       'dwarf',
}


def validate_world_type(world_type: str | None) -> str | None:
    """
    Validate user-supplied world type string.

    Parameters
    ----------
    world_type : str or None
        User input. None means unrestricted galactic draw.

    Returns
    -------
    str or None — validated world type, or None if unrestricted.

    Raises
    ------
    ValueError if world_type is not a recognised value.
    """
    if world_type is None:
        return None
    wt = world_type.strip().lower()
    if wt not in VALID_WORLD_TYPES:
        raise ValueError(
            f"Invalid world_type '{world_type}'. "
            f"Valid options: {', '.join(VALID_WORLD_TYPES)}, or None for unrestricted."
        )
    return wt
