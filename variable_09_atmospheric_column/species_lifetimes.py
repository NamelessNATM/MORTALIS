# variable_09_atmospheric_column/species_lifetimes.py
#
# Chemical lifetimes τ_chem = 1 / (J_i + k [OH]) (Scaffold §12.3).

from __future__ import annotations

import math
from typing import Mapping

# ⚠️ Note 175 — JPL Arrhenius OH destruction (H2S, SO2).
K_OH_H2S = 3.3e-12
K_OH_SO2 = 1.3e-12


def compute_species_lifetimes_s(
    *,
    speciation: Mapping[str, float],
    photolysis_J: Mapping[str, float],
    T_K: float,
    OH_cm3: float | None,
) -> dict[str, float | None]:
    out: dict[str, float | None] = {}
    oh = OH_cm3 if OH_cm3 is not None else 0.0
    for sp, x in speciation.items():
        if x is None or x <= 0.0:
            continue
        j = float(photolysis_J.get(sp, 0.0) or 0.0)
        k_oh = 0.0
        if oh > 0.0:
            if sp == "H2S":
                k_oh = K_OH_H2S * math.exp(-200.0 / float(T_K))
            elif sp == "SO2":
                k_oh = K_OH_SO2 * math.exp(-330.0 / float(T_K))
        rate = j + k_oh * oh
        out[sp] = (1.0 / rate) if rate > 0.0 else None
    return out
