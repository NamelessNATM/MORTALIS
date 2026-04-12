# world_config/world_config.py
#
# PURPOSE: Assemble the world configuration dict from user inputs.
# Entry point for the world_config module.
# Contains no physics. Does not import from any variable folder.
#
# The config dict is the sole channel through which user selections
# reach the simulation. main.py passes it into the cascade.
# Variable sub-functions never see it directly.

from world_config.world_type import validate_world_type


def build_config(world_type: str | None = None) -> dict:
    """
    Assemble and validate the world configuration.

    Parameters
    ----------
    world_type : str or None
        User-selected world type. None = unrestricted galactic draw.

    Returns
    -------
    dict with keys:
        'world_type' : str or None — validated world type
        'regime'     : str or None — regime string for sampler conditioning
    """
    wt = validate_world_type(world_type)
    regime = wt  # world_type strings map directly to regime strings at this stage

    return {
        'world_type': wt,
        'regime':     regime,
    }
