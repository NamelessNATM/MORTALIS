# variable_09_atmospheric_column/regime_router.py
#
# V09 regime routing from V02 + V04 + surface pressure + speciation.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

# ⚠️ Flag 158 (procedural regime threshold; not derived from physics, set to
# match Solar System reference bodies' regime classifications).
P_THIN_BAR = 0.5
P_VENUS_THICK_BAR = 10.0
T_TITAN_ROUTING_K = 150.0
X_CH4_TITAN = 0.02


@dataclass(frozen=True)
class V09Routing:
    kind: str  # "skip" | "terrestrial" | "gas_envelope"
    terrestrial_route: str | None  # thin | thick_terrestrial | venus_class | titan_class
    n: int | None
    tau_rc_override: float | None
    skip_reason: str | None


def _x(speciation: Mapping[str, Any] | None, sp: str) -> float:
    if not speciation:
        return 0.0
    v = speciation.get(sp)
    if v is None:
        return 0.0
    return float(v)


def resolve_v09_routing(
    *,
    regime: str,
    atm_class: str,
    P_s_Pa: float | None,
    T_eq_K: float,
    speciation: Mapping[str, Any] | None,
) -> V09Routing:
    """
    Map cascade state to V09 branch. Physics-free classification only.
    """
    if atm_class == "exosphere_only":
        return V09Routing("skip", None, None, None, "exosphere_only")
    if regime == "dwarf" or atm_class == "none":
        return V09Routing("skip", None, None, None, "dwarf_or_no_atmosphere")

    if regime in ("gas_giant", "sub_neptune") and atm_class == "primary_retained":
        return V09Routing("gas_envelope", None, 2, None, None)

    if atm_class not in ("secondary_possible", "primary_stripped"):
        return V09Routing("skip", None, None, None, f"atm_class={atm_class!r}")

    if P_s_Pa is None or P_s_Pa <= 0.0:
        return V09Routing("skip", None, None, None, "P_s unavailable")

    p_bar = P_s_Pa / 1.0e5
    x_co2 = _x(speciation, "CO2")
    x_ch4 = _x(speciation, "CH4")

    if p_bar > P_VENUS_THICK_BAR and x_co2 > 0.5:
        return V09Routing(
            "terrestrial",
            "venus_class",
            1,
            1.0,
            None,
        )
    if p_bar > P_THIN_BAR and x_ch4 > X_CH4_TITAN and T_eq_K < T_TITAN_ROUTING_K:
        return V09Routing("terrestrial", "titan_class", 2, None, None)
    if p_bar < P_THIN_BAR:
        return V09Routing("terrestrial", "thin", 2, None, None)
    return V09Routing("terrestrial", "thick_terrestrial", 2, None, None)
