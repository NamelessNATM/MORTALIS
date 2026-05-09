# variable_01_5_disk_chemistry/core_mass_fraction.py
#
# CLOSED-FORM:
#   M_core   = N_Fe (1 - χ_ox) μ_Fe
#   M_mantle = N_Mg (μ_Mg + μ_O) + N_Si (μ_Si + 2 μ_O)
#              + N_Fe χ_ox (μ_Fe + μ_O)
#   CMF      = M_core / (M_core + M_mantle)
#
# Stoichiometric mass balance: Mg→MgO (1 mol O per mol Mg), Si→SiO2
# (2 mol O per mol Si), Fe partitioned between metallic core
# (fraction 1-χ_ox) and mantle FeO (fraction χ_ox).
#
# χ_ox = 0.0 is the deterministic V01.5 baseline, representing the
# idealized zero-fugacity case where all iron is reduced and segregates
# entirely into the core. This produces the foundational structural
# proxy used in comparative exoplanetology for unstripped, inner-disk-
# accreted rocky planets.
#
# Source: stoichiometric mass balance from condensation sequence
#         equilibrium thermochemistry; see V01.5 research deliverable.
#
# EARTH CALIBRATION ([X/H] = 0, χ_ox = 0):
#   N_Mg = 1.0471, N_Si = 1.000, N_Fe = 0.8710
#   M_core   = 0.8710 × 55.845 = 48.641
#   M_mantle = 1.0471 × (24.305 + 15.999)
#              + 1.000 × (28.085 + 2 × 15.999) + 0
#            = 42.198 + 60.083 = 102.281
#   CMF = 48.641 / (48.641 + 102.281) = 0.3223
#
# Earth target: 0.325. Residual 0.003 ≈ Ni in core + light elements
# in core ≈ FeO in mantle compensation (out of V01.5 scope).
#
# Propagated 1σ on CMF from Lodders ±0.01 dex inputs: ±0.010.

from variable_01_5_disk_chemistry.solar_abundance_constants import (
    MU_FE_GMOL,
    MU_MG_GMOL,
    MU_O_GMOL,
    MU_SI_GMOL,
)


def compute_cmf(
    N_Fe: float,
    N_Mg: float,
    N_Si: float,
    chi_ox: float = 0.0,
) -> float:
    """
    Stoichiometric mass-balance core mass fraction.

    Parameters
    ----------
    N_Fe, N_Mg, N_Si : float
        Refractory molar abundances (N_Si = 1.0 convention).
    chi_ox : float, optional
        Iron oxidation fraction in [0, 1]. Default 0.0 = all iron
        reduced into core (V01.5 deterministic baseline).
        Future cascade restructure may feed V08 ΔIW back to compute
        χ_ox. See Note opened in this scaffold.

    Returns
    -------
    CMF : float — core mass fraction in [0, 1].
    """
    M_core = N_Fe * (1.0 - chi_ox) * MU_FE_GMOL
    M_mantle = (
        N_Mg * (MU_MG_GMOL + MU_O_GMOL)
        + N_Si * (MU_SI_GMOL + 2.0 * MU_O_GMOL)
        + N_Fe * chi_ox * (MU_FE_GMOL + MU_O_GMOL)
    )
    return M_core / (M_core + M_mantle)
