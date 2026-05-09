"""V01.5 disk chemistry entry point: rocky interior structure
from host-star elemental abundances."""

from __future__ import annotations

# variable_01_5_disk_chemistry/variable_01_5_disk_chemistry.py
#
# Entry point. Orchestrates V01.5 sub-functions. No physics here.
#
# INPUTS:
#   regime : str — one of {dwarf, rocky, sub_neptune, gas_giant}
#   FeH, MgH, SiH : float — stellar [X/H] dex (from V03)
#
# OUTPUTS (regime-conditional):
#   CMF                    : float | None
#   mg_si_mantle           : float | None
#   fe_si_bulk             : float | None
#   rho_uncompressed_kgm3  : float | None
#   regime_applicable      : bool
#
# For sub_neptune and gas_giant regimes, CMF in this stoichiometric
# sense is not defined — these regimes have massive volatile
# envelopes whose mass-radius relationship is dominated by the H/He
# layer rather than the refractory core. All outputs return None
# with regime_applicable = False.

from variable_01_5_disk_chemistry.bulk_fe_si_ratio import compute_fe_si_ratio
from variable_01_5_disk_chemistry.core_mass_fraction import compute_cmf
from variable_01_5_disk_chemistry.mantle_mg_si_ratio import compute_mg_si_ratio
from variable_01_5_disk_chemistry.molar_abundances import compute_molar_abundances
from variable_01_5_disk_chemistry.uncompressed_density import (
    compute_uncompressed_density,
)

_APPLICABLE_REGIMES = ("dwarf", "rocky")


def compute_disk_chemistry(
    regime: str,
    FeH: float,
    MgH: float,
    SiH: float,
) -> dict:
    """
    V01.5 entry point.

    Returns
    -------
    dict with keys:
        CMF                    : float | None
        mg_si_mantle           : float | None
        fe_si_bulk             : float | None
        rho_uncompressed_kgm3  : float | None
        regime_applicable      : bool
    """
    if regime not in _APPLICABLE_REGIMES:
        return {
            "CMF": None,
            "mg_si_mantle": None,
            "fe_si_bulk": None,
            "rho_uncompressed_kgm3": None,
            "regime_applicable": False,
        }

    molar = compute_molar_abundances(FeH, MgH, SiH)
    CMF = compute_cmf(molar["N_Fe"], molar["N_Mg"], molar["N_Si"])
    mg_si = compute_mg_si_ratio(molar["N_Mg"], molar["N_Si"])
    fe_si = compute_fe_si_ratio(molar["N_Fe"], molar["N_Si"])
    rho_unc = compute_uncompressed_density(CMF)

    return {
        "CMF": CMF,
        "mg_si_mantle": mg_si,
        "fe_si_bulk": fe_si,
        "rho_uncompressed_kgm3": rho_unc,
        "regime_applicable": True,
    }
