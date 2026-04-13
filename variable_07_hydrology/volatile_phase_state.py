# variable_07_hydrology/volatile_phase_state.py
#
# Volatile phase state from saturation thermodynamics.
# One exported group: vapor pressure + phase evaluation + batch over speciation.

import math

# Universal gas constant — Variable 07 authorised value (J mol⁻¹ K⁻¹).
R_GAS = 8.314

# Antoine coefficients: log10(P_sat / bar) = A - B / (T + C)
# All coefficients are intrinsic molecular properties measured in Earth
# laboratories. Universal across planetary bodies.
# Sources as noted per species.

SPECIES_DATA = {
    "H2O": {
        "antoine": [
            # Source: standard Antoine, Earth-fitted, universal molecular physics
            # Valid: 273–373 K
            {
                "A": 5.11564,
                "B": 1687.537,
                "C": -42.98,
                "T_min": 273.0,
                "T_max": 373.0,
            }
        ],
        "T_tp": 273.16,  # K  — NIST, universal molecular constant
        "P_tp": 611.7,  # Pa — NIST, universal molecular constant
        "T_c": 647.1,  # K  — NIST, universal molecular constant
        "P_c": 22064000,  # Pa — NIST, universal molecular constant
        "dH_sub": 51000.0,  # J/mol — latent heat sublimation, NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        "molar_mass": 0.01802,  # kg/mol
    },
    "CO2": {
        "antoine": [
            # Source: Giauque & Egan (1937) via NIST. Sublimation curve only.
            # Valid: 154.26–195.89 K. Below 154.26 K use Clausius-Clapeyron.
            # Above T_c (304.18 K) fluid is supercritical — Antoine not valid.
            # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT — universal molecular physics
            {
                "A": 6.81228,
                "B": 1301.679,
                "C": -3.494,
                "T_min": 154.26,
                "T_max": 195.89,
            }
        ],
        "T_tp": 216.58,  # K  — NIST, universal molecular constant
        "P_tp": 518500.0,  # Pa — NIST, universal molecular constant
        "T_c": 304.18,  # K  — NIST, universal molecular constant
        "P_c": 7380000.0,  # Pa — NIST, universal molecular constant
        "dH_sub": 26100.0,  # J/mol — NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        "molar_mass": 0.04401,  # kg/mol
        # NOTE: CO2 liquid-vapor regime (216.58 K < T_s < 304.18 K,
        # P_s > 518500 Pa) requires Span-Wagner EOS for accurate P_sat.
        # Engine returns 'liquid_possible' in this window. Quantitative
        # pressure evaluation deferred — Flag 88.
    },
    "SO2": {
        "antoine": [
            # Source: Stull (1947) via NIST.
            # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT — universal molecular physics
            # Low-temp set: 177.7–263.0 K
            # High-temp set: 263.0–414.9 K
            # 4.7% discontinuity at 263.0 K — known model limitation,
            # not patched. Hard branch at handoff temperature.
            # Below 177.7 K use Clausius-Clapeyron fallback.
            {
                "A": 3.48586,
                "B": 668.225,
                "C": -72.252,
                "T_min": 177.7,
                "T_max": 263.0,
            },
            {
                "A": 4.37798,
                "B": 966.575,
                "C": -42.071,
                "T_min": 263.0,
                "T_max": 414.9,
            },
        ],
        "T_tp": 197.7,  # K  — NIST
        "P_tp": 1670.0,  # Pa — NIST independent value (Antoine-derived
        # value gives 1440 Pa; 14% deviation at triple
        # point. NIST value used. Flag 73).
        "T_c": 430.8,  # K  — NIST
        "P_c": 7884000,  # Pa — NIST
        "dH_sub": 24900.0,  # J/mol — NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        # Not returned by research; sourced directly
        # from NIST thermochemical tables.
        "molar_mass": 0.06406,  # kg/mol
    },
    "CH4": {
        "antoine": [
            # Source: standard Antoine, Earth-fitted, universal molecular physics
            # Valid: 90–190 K
            {
                "A": 3.9895,
                "B": 443.028,
                "C": -0.49,
                "T_min": 90.0,
                "T_max": 190.0,
            }
        ],
        "T_tp": 90.69,  # K  — NIST
        "P_tp": 11696.0,  # Pa — NIST
        "T_c": 190.6,  # K  — NIST
        "P_c": 4599000,  # Pa — NIST
        "dH_sub": 9703.0,  # J/mol — NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        "molar_mass": 0.01604,  # kg/mol
    },
    "NH3": {
        "antoine": [
            # Source: standard Antoine, Earth-fitted, universal molecular physics
            # Valid: 179–261 K
            {
                "A": 4.86886,
                "B": 1113.928,
                "C": -10.409,
                "T_min": 179.0,
                "T_max": 261.0,
            }
        ],
        "T_tp": 195.41,  # K  — NIST
        "P_tp": 6060.0,  # Pa — NIST
        "T_c": 405.6,  # K  — NIST
        "P_c": 11333000,  # Pa — NIST
        "dH_sub": 28850.0,  # J/mol — NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        "molar_mass": 0.01703,  # kg/mol
    },
    "H2": {
        # T_c = 33.0 K. Any rocky planet surface has T_s >> T_c.
        # H2 is a permanent non-condensing gas for all rocky planet regimes
        # this engine produces. Antoine coefficients included for completeness
        # but will never execute for T_s > 33 K.
        "antoine": [
            # Source: van Itterbeek et al. via Yaws / NIST
            # Converted from ln to log10 form (divided by ln(10) = 2.302585)
            # Valid: 21.01–32.27 K
            # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
            {
                "A": 1.5387,
                "B": 43.1667,
                "C": 7.726,
                "T_min": 21.01,
                "T_max": 32.27,
            }
        ],
        "T_tp": 14.0,  # K  — NIST
        "P_tp": 7000.0,  # Pa — NIST
        "T_c": 33.0,  # K  — NIST
        "P_c": 1300000,  # Pa — NIST
        "dH_sub": 904.0,  # J/mol — NIST
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
        "molar_mass": 0.00202,  # kg/mol
    },
}


def _antoine_P_Pa_from_segment(T_K: float, seg: dict) -> float:
    # Antoine equation — source: SPECIES_DATA segment citations; Flag 71–74.
    log10_p_bar = seg["A"] - seg["B"] / (T_K + seg["C"])
    p_bar = 10.0**log10_p_bar
    return p_bar * 1.0e5


def _select_antoine_segment(species: str, T_K: float):
    sets = SPECIES_DATA[species]["antoine"]
    if species == "SO2" and T_K >= 263.0:
        for seg in sets:
            if seg["T_min"] == 263.0 and seg["T_min"] <= T_K <= seg["T_max"]:
                return seg
        return None
    for seg in sets:
        if seg["T_min"] <= T_K <= seg["T_max"]:
            return seg
    return None


def evaluate_vapor_pressure(species: str, T_K: float):
    """
    Saturation vapor pressure [Pa]. None if T_K > T_c (supercritical branch).
    """
    data = SPECIES_DATA[species]
    T_c = data["T_c"]
    if T_K > T_c:
        return None

    antoine_sets = data["antoine"]
    global_T_min = min(s["T_min"] for s in antoine_sets)
    global_T_max = max(s["T_max"] for s in antoine_sets)
    dH_sub = data["dH_sub"]

    def clapeyron_P(T: float, T_ref: float, P_ref_Pa: float) -> float:
        # Clausius-Clapeyron — source: standard thermodynamics from ΔH_sub;
        # ⚠️ EARTH-MEASURED MOLECULAR CONSTANT (dH_sub); Flag 75–77.
        exponent = -(dH_sub / R_GAS) * (1.0 / T - 1.0 / T_ref)
        return P_ref_Pa * math.exp(exponent)

    if T_K < global_T_min:
        seg0 = min(antoine_sets, key=lambda s: s["T_min"])
        T_ref = seg0["T_min"]
        # Antoine at T_min — source: SPECIES_DATA; Flag 71–74.
        P_ref_Pa = _antoine_P_Pa_from_segment(T_ref, seg0)
        return clapeyron_P(T_K, T_ref, P_ref_Pa)

    seg = _select_antoine_segment(species, T_K)
    if seg is not None:
        # Antoine equation — source: SPECIES_DATA segment citations; Flag 71–74.
        return _antoine_P_Pa_from_segment(T_K, seg)

    # Above Antoine upper bound but T_K <= T_c: continue vapor pressure with CC
    # from the highest tabulated Antoine temperature.
    upper_seg = max(antoine_sets, key=lambda s: s["T_max"])
    T_ref = upper_seg["T_max"]
    # Antoine at T_ref — source: SPECIES_DATA; Flag 71–74.
    P_ref_Pa = _antoine_P_Pa_from_segment(T_ref, upper_seg)
    return clapeyron_P(T_K, T_ref, P_ref_Pa)


def evaluate_phase_state(species: str, T_K: float, P_s_Pa: float):
    """
    Phase label and explanatory note for one species at (T_K, P_s).
    """
    # ⚠️ T_s APPROXIMATION — T_eq used as surface temperature proxy.
    # Greenhouse warming correction deferred (Flag 43). Surface temperatures
    # on planets with significant atmospheres will be underestimated.

    T_c = SPECIES_DATA[species]["T_c"]
    P_tp = SPECIES_DATA[species]["P_tp"]
    T_tp = SPECIES_DATA[species]["T_tp"]

    if species == "H2" and T_K > T_c:
        return (
            "gas_permanent",
            "H2 critical temperature 33 K; always gas on rocky surfaces",
        )

    if T_K > T_c:
        return "supercritical_fluid", f"{species} above critical temperature {T_c} K"

    if P_s_Pa < P_tp:
        if T_K < T_tp:
            return "solid", "P_s below triple point pressure; T_s below triple point"
        return "gas", "P_s below triple point pressure; liquid phase forbidden"

    if species == "CO2" and T_tp <= T_K <= T_c and P_s_Pa >= P_tp:
        return (
            "liquid_possible",
            (
                "CO2 in liquid stability window (T and P above triple point, below critical). "
                "Span-Wagner EOS required for quantitative P_sat — deferred. "
                "Flag 88."
            ),
        )

    if T_K < T_tp:
        return "solid", f"T_s below triple point temperature {T_tp} K"

    P_sat = evaluate_vapor_pressure(species, T_K)
    if P_sat is None:
        return "supercritical_fluid", f"{species} above critical temperature"

    if P_s_Pa >= P_sat:
        return (
            "liquid",
            f"P_s ({P_s_Pa:.2e} Pa) >= P_sat ({P_sat:.2e} Pa)",
        )
    return (
        "gas",
        f"P_s ({P_s_Pa:.2e} Pa) < P_sat ({P_sat:.2e} Pa); volatile in vapor phase",
    )


def evaluate_all_species(speciation_dict, T_eq_K: float, P_s_Pa):
    """Phase state for each outgassed species with non-zero mole fraction."""
    # ⚠️ T_s APPROXIMATION — T_eq used as surface temperature proxy.
    # Greenhouse warming correction deferred (Flag 43). Surface temperatures
    # on planets with significant atmospheres will be underestimated.
    if speciation_dict is None:
        return {
            "note": (
                "Speciation unavailable from V06; phase state evaluation deferred"
            )
        }

    if P_s_Pa is None:
        return {
            "note": (
                "P_s unavailable — atmospheric mass blocked (Flag 40); "
                "phase state evaluation deferred"
            )
        }

    if P_s_Pa == 0.0:
        out = {}
        for species, x in speciation_dict.items():
            if x is None or x == 0.0:
                continue
            out[species] = {
                "phase": "gas",
                "note": "no atmosphere; volatile cannot accumulate at surface",
                "molar_fraction": x,
            }
        return out

    out = {}
    for species, x in speciation_dict.items():
        if x is None or x == 0.0:
            continue
        if species not in SPECIES_DATA:
            continue
        phase, note = evaluate_phase_state(species, T_eq_K, P_s_Pa)
        out[species] = {"phase": phase, "note": note, "molar_fraction": x}
    return out
