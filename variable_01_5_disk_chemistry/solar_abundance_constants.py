# variable_01_5_disk_chemistry/solar_abundance_constants.py
#
# Module-level constants for V01.5 disk chemistry derivation.
#
# SOLAR ABUNDANCE OFFSETS (logarithmic, dex):
#   A(Si)_solar = 7.54
#   A(Mg)_solar = 7.56
#   A(Fe)_solar = 7.48
#
# Source: Lodders, K. (2003), "Solar System Abundances and Condensation
#         Temperatures of the Elements", ApJ 591, 1220–1247, Table 2,
#         column "Protosolar A(El)_0".
# Confirmation scope: Multi-body confirmed empirical (Lodders protosolar
#         compilations, anchored to CI carbonaceous chondrites).
# Published 1σ uncertainty: ±0.01 dex per value.
#
# ⚠️ Note: these values are Solar System cosmochemical empirical
# constants. The astronomical [X/H] dex scale is by definition
# logarithmic relative to the Sun, so a solar-anchored conversion is
# inherent to the scale, not a project-introduced fallback.
#
# ATOMIC MOLAR MASSES (fundamental physical constants):
#   μ_Fe = 55.845 g/mol
#   μ_Mg = 24.305 g/mol
#   μ_Si = 28.085 g/mol
#   μ_O  = 15.999 g/mol

A_SUN_SI = 7.54  # dex (Lodders 2003 protosolar)
A_SUN_MG = 7.56  # dex (Lodders 2003 protosolar)
A_SUN_FE = 7.48  # dex (Lodders 2003 protosolar)

MU_FE_GMOL = 55.845
MU_MG_GMOL = 24.305
MU_SI_GMOL = 28.085
MU_O_GMOL = 15.999
