# variable_01_5_disk_chemistry/uncompressed_density.py
#
# FORMULA (mass-weighted harmonic mean):
#   ρ_uncompressed = ( CMF / ρ_core + (1 - CMF) / ρ_mantle )^(-1)
#
# REFERENCE DENSITIES at 0 GPa, 300 K:
#   ρ_core   = 8278.9 kg/m³  (Fe_0.9 Ni_0.1 alloy)
#   ρ_mantle = 3323.5 kg/m³  (olivine + pyroxene equilibrium assemblage)
#
# Source: Plotnykov, M. & Valencia, D. (2020), MNRAS 499, Issue 1,
#         Table 1.
#         ρ_core adapted from Morrison et al. (2018) Fe-Ni alloy EOS.
#         ρ_mantle uses Stixrude & Lithgow-Bertelloni (2011) mineral
#         parameters for olivine and pyroxene end members.
# Confirmation scope: Universal mineral physics; multi-stellar
#         confirmed exoplanet interior modeling.
#
# ⚠️ Note: a closed-form ρ_mantle(Mg/Si) relation does not exist in
# primary literature — modern interior models use Voigt-Reuss-Hill
# averaging of olivine/pyroxene phases dynamically. The fixed
# 3323.5 kg/m³ baseline is the documented standard for static
# uncompressed-density initialization. Future scaffold may upgrade
# this to a Mg/Si-dependent value via V-R-H averaging.
#
# Earth calibration (CMF = 0.3223):
#   ρ_uncompressed = (0.3223/8278.9 + 0.6777/3323.5)^-1
#                  = (3.892e-5 + 2.040e-4)^-1
#                  = (2.429e-4)^-1
#                  = 4117 kg/m³
# (Earth's actual uncompressed bulk density ≈ 4050 kg/m³; agreement
# to ~1.7%.)

RHO_CORE_KGM3 = 8278.9
RHO_MANTLE_KGM3 = 3323.5


def compute_uncompressed_density(CMF: float) -> float:
    """
    Mass-weighted harmonic mean uncompressed bulk density [kg/m³].
    """
    return 1.0 / (CMF / RHO_CORE_KGM3 + (1.0 - CMF) / RHO_MANTLE_KGM3)
