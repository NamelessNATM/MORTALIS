# variable_01_5_disk_chemistry/molar_abundances.py
#
# FORMULA:
#   N_Si ≡ 1.000
#   N_Mg = 10^((MgH + A_SUN_MG) - (SiH + A_SUN_SI))
#        = 10^(MgH - SiH + 0.02)
#   N_Fe = 10^((FeH + A_SUN_FE) - (SiH + A_SUN_SI))
#        = 10^(FeH - SiH - 0.06)
#
# Converts host-star logarithmic [X/H] dex inputs into linear molar
# abundance ratios normalized to N_Si = 1.0 in the protoplanetary disk
# solid phase.
#
# Physical assumption: at refractory condensation temperatures (≈1200–
# 1500 K) typical of inner-disk rocky planetesimal formation, gas-to-
# solid partitioning of Fe, Mg, Si is effectively 100%. Stellar molar
# ratios are preserved into bulk planetary composition.
#
# Source: Lodders (2003) cosmochemical scale; condensation sequence
#         physics from equilibrium thermochemistry literature.
#
# Earth calibration ([Fe/H] = [Mg/H] = [Si/H] = 0):
#   N_Si = 1.000
#   N_Mg = 10^0.02  = 1.0471
#   N_Fe = 10^-0.06 = 0.8710

from variable_01_5_disk_chemistry.solar_abundance_constants import (
    A_SUN_FE,
    A_SUN_MG,
    A_SUN_SI,
)


def compute_molar_abundances(FeH: float, MgH: float, SiH: float) -> dict:
    """
    Convert [X/H] dex inputs to refractory molar abundances (N_Si = 1).

    Parameters
    ----------
    FeH, MgH, SiH : float
        Stellar [Fe/H], [Mg/H], [Si/H] in dex.

    Returns
    -------
    dict with keys:
        N_Si : float — silicon molar abundance (≡ 1.0)
        N_Mg : float — magnesium molar abundance relative to silicon
        N_Fe : float — iron molar abundance relative to silicon
    """
    N_Si = 1.0
    N_Mg = 10.0 ** ((MgH + A_SUN_MG) - (SiH + A_SUN_SI))
    N_Fe = 10.0 ** ((FeH + A_SUN_FE) - (SiH + A_SUN_SI))
    return {"N_Si": N_Si, "N_Mg": N_Mg, "N_Fe": N_Fe}
