# variable_09_atmospheric_column/venus_shortwave_attenuation.py
#
# Venus-class gray-model metadata (router applies τ_rc and n overrides).

# ⚠️ Flag 162 — Venus-class shortwave attenuation regime parameters.
VENUS_CLASS_OVERRIDES = {
    "n": 1,
    "tau_rc": 1.0,
}

# ⚠️ Flag 163 — Gray-model Venus regime applicability limit.
VENUS_GRAY_MODEL_LIMIT = {
    "tau_zero_above": 100.0,
    "expected_bias_low_pct": 15,
}


def build_venus_branch_metadata() -> dict:
    """Return dict attached to V09 output for Venus-class worlds."""
    return {
        "t_surface_lower_bound": True,
        "regime": "venus_class",
        "expected_bias_low_pct": VENUS_GRAY_MODEL_LIMIT["expected_bias_low_pct"],
    }
