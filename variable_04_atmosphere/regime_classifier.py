# variable_04_atmosphere/regime_classifier.py
#
# PURPOSE: Map planetary regime + Jeans parameters + escape rate to an
# atmospheric class and dominant composition.
#
# Decision logic (Source: research session 2026-04-12):
#
#   gas_giant   → H/He always retained. lambda_H >> 20 at any physical T_exo.
#                 Envelope loss < 1% of total mass over stellar lifetime.
#
#   sub_neptune → H/He retained UNLESS cumulative hydrodynamic loss exceeds
#                 initial envelope mass. Initial envelope mass fraction is not
#                 in cascade (Flag 42). Default: retained. Flag raised.
#
#   rocky       → Secondary atmosphere possible if lambda_N2 >= lambda_crit
#                 AND lambda_CO2 >= lambda_crit. Composition indeterminate
#                 without mantle oxygen fugacity (Flag 29).
#
#   dwarf       → No atmosphere. lambda < lambda_crit for all species.
#
# ⚠️ Flag 42: Sub-Neptune stripping boundary ambiguous. Initial envelope mass
# fraction requires protoplanetary disk accretion variable not in cascade.
# Classification defaults to retained; cumulative loss check uses M_dot * age
# against a flagged placeholder envelope mass.
# ⚠️ Flag 29: Rocky planet atmospheric composition underdetermined without
# mantle oxygen fugacity. Composition reported as 'secondary_possible' only.

# Placeholder sub-Neptune envelope mass fraction (Flag 42)
# Earth fallback: ~1–10% of planet mass for close-in sub-Neptunes
# ⚠️ EARTH FALLBACK — Flag 42
SUB_NEPTUNE_ENVELOPE_FRACTION = 0.05


def attach_photochemically_limited_species(jeans: dict) -> dict:
    """
    Attach photochemically-limited entries for H2S and SO2 to the jeans
    dict. These species do not reach the exobase intact on any planet
    with a thick atmosphere — altitude photochemistry and source-proximate
    chemistry both destroy them faster than vertical transport.

    ⚠️ Flag 154: H2S and SO2 retention not computable from current cascade.
      Blocked on T_surface, tropospheric OH concentration, and ocean
      volume. Requires downstream photochemistry cascade variable.
      Decision A3 per research cycle: return None (not zero, not preserved)
      to force downstream None-safe handling.

    Parameters
    ----------
    jeans : dict
        Existing jeans dict from compute_all_species().

    Returns
    -------
    dict with H2S and SO2 entries added, each of form:
        {"lambda": None, "retained": None, "flag": "photochemically_limited"}
    """
    for species in ("H2S", "SO2"):
        jeans[species] = {
            "lambda": None,
            "retained": None,
            "flag": "photochemically_limited",
        }
    return jeans


def classify_atmosphere(regime: str,
                         jeans: dict,
                         M_kg: float,
                         M_dot_kg_s: float,
                         age_Gyr: float) -> dict:
    """
    Atmospheric class and dominant composition.

    Parameters
    ----------
    regime      : compositional regime string from Variable 02
    jeans       : output of jeans_parameter.compute_all_species()
    M_kg        : planetary mass [kg] from Variable 01
    M_dot_kg_s  : hydrodynamic mass loss rate [kg/s] from Variable 05
    age_Gyr     : stellar age [Gyr] from Variable 03

    Returns
    -------
    dict with keys:
        'atm_class'   : str — 'none', 'primary_retained', 'primary_stripped',
                               'secondary_possible', 'exosphere_only'
        'composition' : str — 'H2_He', 'N2_CO2_unknown', 'none', 'trace'
        'notes'       : str — flag summary
    """
    GYR_TO_S = 3.156e16

    if regime == "gas_giant":
        return {
            "atm_class":   "primary_retained",
            "composition": "H2_He",
            "notes":       "Gas giant; H/He gravitationally bound regardless of T_exo.",
        }

    if regime == "sub_neptune":
        # ⚠️ Flag 42: envelope mass fraction is a placeholder
        M_envelope = SUB_NEPTUNE_ENVELOPE_FRACTION * M_kg
        M_lost = M_dot_kg_s * age_Gyr * GYR_TO_S
        if M_lost >= M_envelope:
            return {
                "atm_class":   "primary_stripped",
                "composition": "none",
                "notes":       "Flag 42: stripping boundary uses placeholder envelope "
                               "fraction. Treat as indicative only.",
            }
        return {
            "atm_class":   "primary_retained",
            "composition": "H2_He",
            "notes":       "Flag 42: envelope retention uses placeholder mass fraction.",
        }

    if regime == "rocky":
        n2_retained  = jeans.get("N2",  {}).get("retained", False)
        co2_retained = jeans.get("CO2", {}).get("retained", False)
        if n2_retained and co2_retained:
            return {
                "atm_class":   "secondary_possible",
                "composition": "N2_CO2_unknown",
                "notes":       "Flag 29: composition underdetermined without mantle "
                               "oxygen fugacity. Flag 40: M_atm blocked — X_vol "
                               "not in cascade.",
            }
        return {
            "atm_class":   "exosphere_only",
            "composition": "trace",
            "notes":       "Heavy species do not meet Jeans retention threshold.",
        }

    # dwarf
    return {
        "atm_class":   "none",
        "composition": "none",
        "notes":       "Dwarf regime; gravity insufficient to retain any species.",
    }
