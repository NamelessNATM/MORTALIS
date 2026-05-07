# Changelog Flag Audit (v2)

Total open flags reviewed: 148
Flag (stay actionable):     9
Note (reclassify):          102
Cleanup (remove from open list): 5
Pending Reclassification:   32

---

## Flag (Stay Actionable)

### Flag 160c
**Current text:** Flag 160c–160f: isosteric placeholders for CO₂-CO₂, H₂-H₂, H₂-He,
  N₂-CO₂, CH₄-CH₄, N₂-CH₄ pairs not directly tabulated by HITRAN.
  Targeted research required to confirm or correct.
  File: cia_coefficients.py.
**Triggering signal:** Targeted research required

### Flag 160d
**Current text:** Flag 160c–160f: isosteric placeholders for CO₂-CO₂, H₂-H₂, H₂-He,
  N₂-CO₂, CH₄-CH₄, N₂-CH₄ pairs not directly tabulated by HITRAN.
  Targeted research required to confirm or correct.
  File: cia_coefficients.py.
**Triggering signal:** Targeted research required

### Flag 160e
**Current text:** Flag 160c–160f: isosteric placeholders for CO₂-CO₂, H₂-H₂, H₂-He,
  N₂-CO₂, CH₄-CH₄, N₂-CH₄ pairs not directly tabulated by HITRAN.
  Targeted research required to confirm or correct.
  File: cia_coefficients.py.
**Triggering signal:** Targeted research required

### Flag 160f
**Current text:** Flag 160c–160f: isosteric placeholders for CO₂-CO₂, H₂-H₂, H₂-He,
  N₂-CO₂, CH₄-CH₄, N₂-CH₄ pairs not directly tabulated by HITRAN.
  Targeted research required to confirm or correct.
  File: cia_coefficients.py.
**Triggering signal:** Targeted research required

### Flag 161
**Current text:** Flag 161: H₂O line k coefficient inverted from Earth τ targets
  (fit, not derived). Targeted research required to source from
  MT_CKD v4.3 or HITRAN 2020 before V10 begins.
  File: line_absorption_coefficients.py.
**Triggering signal:** Targeted research required

### Flag 161c
**Current text:** Flag 161c: Titan CH₄ lines suppressed (no value sourced; N₂-CH₄
  CIA carries bulk thermal opacity). Research-incompleteness gap.
  File: line_absorption_coefficients.py.
**Triggering signal:** Research-incompleteness gap

### Flag 180
**Current text:** Flag 180: Earth implicit τ_rc solver returns ~0.064 vs literature
  0.1 used for calibration anchor. Gray-model Earth-water-vapor
  n=2 limitation. Calibration uses literature τ_rc; runtime cascade
  uses solver τ_rc. ~10 K T_surface discrepancy propagates.
  Targeted research required. File: tau_rc_implicit_solver.py;
  validation note.
**Triggering signal:** Targeted research required

### Flag 181
**Current text:** Flag 181: H₂O line k coefficient in Flag 161 is a fit, not a
  derivation. Targeted research required to source from MT_CKD v4.3
  or HITRAN 2020 and re-validate Earth τ₀ from derived value.
  File: line_absorption_coefficients.py; validation note.
**Triggering signal:** Targeted research required

### Flag 182
**Current text:** Flag 182: Active V09 branch verification incomplete. Cascade-
  integrated runs through V01–V08 to V09 terrestrial_thick,
  venus_class, titan_class, and gas_envelope branches require
  non-dwarf seeds not exercised by benchmark pair. To be addressed
  in subsequent scaffold.
**Triggering signal:** verification incomplete

---

## Note (Reclassify to Note)

### Flag 04
**Current text:** - Flag 04: σ_rbf universality — Earth fallback
**Triggering signal:** Earth fallback

### Flag 05
**Current text:** - Flag 05: Power-law alpha exponents — inherent
**Triggering signal:** — inherent

### Flag 08
**Current text:** - Flag 08: Compositional degeneracy — inherent
**Triggering signal:** — inherent

### Flag 09
**Current text:** - Flag 09: Rocky M-R universality — Earth fallback
**Triggering signal:** Earth fallback

### Flag 11
**Current text:** - Flag 11: Uniform density P_c — inherent approximation
**Triggering signal:** — inherent

### Flag 12
**Current text:** - Flag 12: Bashi gas-giant 17% overestimate — inherent to model
**Triggering signal:** — inherent

### Flag 13
**Current text:** - Flag 13: Dwarf rho_0 — Earth fallback
**Triggering signal:** Earth fallback

### Flag 20
**Current text:** - Flag 20: Kroupa α empirical — inherent
**Triggering signal:** — inherent

### Flag 22
**Current text:** - Flag 22: JJ2010 single measurement context — inherent
**Triggering signal:** — inherent

### Flag 23
**Current text:** - Flag 23: τ_min anchor — Earth fallback
**Triggering signal:** Earth fallback

### Flag 31
**Current text:** - Flag 31: a_max ALMA scaling — single-survey approximation; varies between
  star-forming regions. Candidate C rejected (see research path above).
**Triggering signal:** single-survey approximation

### Flag 34
**Current text:** - Flag 34: ε = 0.15 XUV heating efficiency — Solar System calibrated only.
**Triggering signal:** Solar System calibrated

### Flag 39
**Current text:** - Flag 39: K_c (thermospheric thermal conductivity) is gas-dependent,
  lab-measured. O/N2: 0.05 W/m/K; H2/He: 0.30 W/m/K.
  Source: Banks & Kockarts (1973).
**Triggering signal:** lab-measured

### Flag 46
**Current text:** - Flag 46: α = 7 (pressure depth factor) theoretically universal from
  ln(P_meso/P_XUV) ≈ ln(10³). Empirically confirmed on Earth and Mars
  only.
**Triggering signal:** Empirically confirmed on

### Flag 48
**Current text:** - Flag 48: Sudarsky albedo applied to brown_dwarf regime — internal
  luminosity not represented. Category: inherent model limitation.
**Triggering signal:** Category: inherent model limitation

### Flag 50
**Current text:** - Flag 50: χ = 2.44 core-mantle density contrast. Earth-calibrated.
**Triggering signal:** Earth-calibrated

### Flag 51
**Current text:** - Flag 51: P_cmb uniform-density assumption. 9.5% underestimate. Inherent.
**Triggering signal:** Inherent.

### Flag 52
**Current text:** - Flag 52: C_p = 1200 J/(kg·K). Earth silicate calibration.
**Triggering signal:** Earth silicate calibration

### Flag 54
**Current text:** - Flag 54: E_a = 300,000 J/mol dry peridotite. Earth-calibrated. Assumes
  dry rheology.
**Triggering signal:** Earth-calibrated

### Flag 55
**Current text:** - Flag 55: Cᵢ BSE-calibrated isotope concentrations. Not universal.
**Triggering signal:** BSE-calibrated

### Flag 59
**Current text:** - Flag 59: Constant T_m(0) across rocky mass range. Inherent to model.
**Triggering signal:** inherent to model

### Flag 60
**Current text:** - Flag 60: ODE self-regulation fails below Ra_c throughout thermal
  history. Inherent to model for low-mass rocky planets.
**Triggering signal:** inherent to model

### Flag 62
**Current text:** - Flag 62: A_mob = 0.122 mobile lid prefactor. Earth-calibrated.
**Triggering signal:** Earth-calibrated

### Flag 64
**Current text:** - Flag 64: Sluggish lid uses mobile lid formula approximation. Inherent.
**Triggering signal:** Inherent.

### Flag 65
**Current text:** - Flag 65: T_solidus Simon-Glatzel fit. Earth peridotite DAC calibration.
**Triggering signal:** Earth peridotite DAC calibration

### Flag 67
**Current text:** - Flag 67: k = 3.5 W/(m·K) thermal conductivity. Kite et al. use
  4.18. Our value produces R_melt ~36% below Kite calibration target.
  Earth silicate fallback. Category: Earth fallback.
**Triggering signal:** Earth fallback

### Flag 68
**Current text:** - Flag 68: Kite (2009) parameterization invalid above ~3 M_Earth.
  Dorn et al. (2018), Noack et al. (2017): pressure suppression
  nonlinearly truncates melting column and raises lower-mantle
  viscosity. One-dimensional Kite model overestimates melt on massive
  super-Earths. Flag for review if M_planet > 3 M_Earth and
  R_melt_kgs used as output. Category: model applicability limit.
**Triggering signal:** Category: model applicability limit

### Flag 69
**Current text:** - Flag 69: A_0 = E_a/R_g = 36,083 K activation temperature. Inherits
  Flag 54 (E_a Earth-calibrated dry peridotite). Category: Earth
  fallback (derived).
**Triggering signal:** Earth-calibrated

### Flag 70
**Current text:** - Flag 70: M_V,☉ = 4.756 mag — empirically adopted solar visual
  magnitude used to anchor the IAU 2015 calibration target.
  Not derivable from Category A constants.
  Category: Earth/Solar System fallback.
**Triggering signal:** Earth/Solar System fallback

### Flag 71
**Current text:** Flag 71: H2O Antoine coefficients — Earth-measured molecular constant,
  intrinsic molecular physics, universal.
**Triggering signal:** Earth-measured molecular constant

### Flag 72
**Current text:** Flag 72: CO2 Antoine coefficients (sublimation) — Giauque & Egan (1937)
  via NIST. Earth-measured, universal molecular physics.
**Triggering signal:** Antoine

### Flag 73
**Current text:** Flag 73: SO2 Antoine coefficients — Stull (1947) via NIST. 4.7%
  discontinuity at 263 K handoff documented; not patched.
  SO2 triple point pressure: NIST value 1670 Pa used; Antoine-derived
  value gives 1440 Pa (14% deviation at boundary — known Antoine limit).
**Triggering signal:** not patched

### Flag 74
**Current text:** Flag 74: CH4, NH3 Antoine coefficients — standard NIST.
  Earth-measured molecular constants, universal.
**Triggering signal:** Earth-measured molecular constant

### Flag 75
**Current text:** Flag 75: dH_sub H2O 51,000 J/mol — NIST. Earth-measured molecular constant.
**Triggering signal:** Earth-measured molecular constant

### Flag 76
**Current text:** Flag 76: dH_sub CO2 26,100 J/mol — NIST. Earth-measured molecular constant.
**Triggering signal:** Earth-measured molecular constant

### Flag 77
**Current text:** Flag 77: dH_sub SO2 24,900 J/mol — NIST. Not returned by research;
  sourced directly from NIST thermochemical tables.
**Triggering signal:** NIST thermochemical tables

### Flag 78
**Current text:** Flag 78: dH_vap H2O 40,650 J/mol at 373 K — NIST.
  Earth-measured molecular constant.
**Triggering signal:** Earth-measured molecular constant

### Flag 79
**Current text:** Flag 79: Ice Ih Clapeyron slope 1.35e8 Pa — Wagner et al. (1994).
  Intrinsic to H2O crystal structure; Earth-measured, universal.
**Triggering signal:** intrinsic to H2O crystal structure

### Flag 80
**Current text:** Flag 80: k_crust = 2.5 W/m/K — terrestrial silicate rock. Earth fallback.
  Universal applicability not confirmed.
**Triggering signal:** Earth fallback

### Flag 81
**Current text:** Flag 81: rho_crust = 2800 kg/m³ — terrestrial continental crust.
  Earth fallback.
**Triggering signal:** Earth fallback

### Flag 82
**Current text:** Flag 82: phi_0 = 0.4 — Athy's Law initial porosity, Earth shale/
  sedimentary baseline. Earth fallback.
**Triggering signal:** Earth fallback

### Flag 83
**Current text:** Flag 83: K_comp = 31 MPa — Athy's Law compaction modulus, Earth shale/
  sedimentary baseline. Earth fallback.
**Triggering signal:** Earth fallback

### Flag 84
**Current text:** Flag 84: rho_b = 2500 kg/m³ — Athy's Law bulk crustal density.
  Earth fallback.
**Triggering signal:** Earth fallback

### Flag 85
**Current text:** Flag 85: N_BUDYKO = 2.0 — MCY shape parameter. Earth-fitted; varies
  1.5–3.0 with biology. Abiotic bare-rock default used. Earth fallback.
**Triggering signal:** Earth fallback

### Flag 86
**Current text:** Flag 86: f_Darcy = 0.05 — Darcy-Weisbach friction factor. Validated
  rocky channels: Earth, Mars, Titan. Earth fallback with multi-body
  partial confirmation.
**Triggering signal:** Earth fallback

### Flag 87
**Current text:** Flag 87: A_GLEN = 2.4e-15 kPa⁻³ s⁻¹ — Glen's flow parameter, Earth
  H2O ice (Paterson 1994). Different values required for CO2/CH4 ice.
  Earth fallback.
**Triggering signal:** Earth fallback

### Flag 89
**Current text:** Flag 89: CO2 Antoine lower bound 154.26 K; Clausius-Clapeyron fallback
  below this. ~20% overshoot confirmed at 149 K extrapolation.
  Model limitation.
**Triggering signal:** Model limitation

### Flag 94
**Current text:** Flag 94: A = 210 W/m² — OLR linear intercept. Budyko (1969).
  Earth-calibrated empirical coefficient. Fails for dense CO2 or
  H2/He atmospheres. Universal applicability not confirmed.
  Category: Earth fallback.
**Triggering signal:** Earth fallback

### Flag 95
**Current text:** Flag 95: B = 2.0 W/m²/K — OLR temperature sensitivity. Earth-
  calibrated. Encodes water-vapour feedback; wrong for non-H2O
  atmospheres. Category: Earth fallback.
**Triggering signal:** Earth fallback

### Flag 97
**Current text:** Flag 97: β = 54.74° singularity — s2 = 0, T2 = 0, formula undefined.
  Handled via explicit branch: if T0 > T_f → ice_free; else →
  full_glaciation. Category: model limitation.
**Triggering signal:** Category: model limitation

### Flag 98
**Current text:** Flag 98: P2 Legendre truncation — 3–7% error on φ_ice as function
  of obliquity. Not patchable without spatial grid.
  Category: model limitation.
**Triggering signal:** Category: model limitation

### Flag 99
**Current text:** Flag 99: Ice-albedo feedback absent. Global mean albedo used at
  ice-edge; local albedo step not modelled. Underestimates ice extent
  near runaway glaciation. Category: model limitation.
**Triggering signal:** Category: model limitation

### Flag 100
**Current text:** Flag 100: EBM annual-mean assumption breaks down at e > 0.3.
  Apoastron winters may drive volatile condensation or atmospheric
  collapse. Formula underestimates maximum glaciation extent on highly
  eccentric worlds. Category: model limitation.
**Triggering signal:** Category: model limitation

### Flag 101
**Current text:** Flag 101: X_dry = 1e-3 — EH3 enstatite chondrite hydration.
  Solar System meteoritic measurement. Earth fallback.
  File: bulk_volatile_fraction.py
**Triggering signal:** Earth fallback

### Flag 102
**Current text:** Flag 102: R_snow,H2O 2.7 AU coefficient — solar system snow line
  calibration. Solar System specific. Earth fallback.
  File: snow_lines.py
**Triggering signal:** Solar System specific

### Flag 103
**Current text:** Flag 103: T_cond values (170 K, 88 K, 45 K) — nebular-pressure
  condensation temperatures. Solar System calibrated.
  File: snow_lines.py
**Triggering signal:** Solar System calibrated

### Flag 104
**Current text:** Flag 104: M² scaling breaks down above ~5 M_☉.
  Model applicability limit.
  File: snow_lines.py
**Triggering signal:** Model applicability limit

### Flag 105
**Current text:** Flag 105: k = 0.44 — oligarchic feeding zone width (Kokubo & Ida 1998).
  Solar System calibrated. Earth fallback.
  File: bulk_volatile_fraction.py
**Triggering signal:** Solar System calibrated

### Flag 107
**Current text:** Flag 107: EH3 fractions f_i — Solar System meteoritic measurements.
  Earth fallback.
  File: elemental_partitioning.py
**Triggering signal:** Earth fallback

### Flag 108
**Current text:** Flag 108: K_D,H = 29 at Earth P_cmb — diamond anvil cell + SIMS.
  Lab measurement. Earth fallback.
  File: core_mantle_partitioning.py
**Triggering signal:** Lab measurement

### Flag 109
**Current text:** Flag 109: K_D,C = 107 at Earth P_cmb — experimental petrology.
  Earth fallback.
  File: core_mantle_partitioning.py
**Triggering signal:** Earth fallback

### Flag 110
**Current text:** Flag 110: K_D,N = 14 at Earth P_cmb — experimental petrology.
  Earth fallback.
  File: core_mantle_partitioning.py
**Triggering signal:** Earth fallback

### Flag 111
**Current text:** Flag 111: K_D,S = 100 at Earth P_cmb — thermodynamic models.
  Earth fallback.
  File: core_mantle_partitioning.py
**Triggering signal:** Earth fallback

### Flag 114
**Current text:** Flag 114: K_D,N and K_D,S pressure scaling at Mars P_cmb not resolved.
  Earth anchor values used as fallback. Earth fallback pending
  low-pressure experimental data.
  File: core_mantle_partitioning.py
**Triggering signal:** Earth fallback

### Flag 116
**Current text:** Flag 116: 80/20 NC/CC mixing ratio — Ru isotopic anomaly constraint.
  Solar System specific.
  File: late_veneer.py
**Triggering signal:** Solar System specific

### Flag 117
**Current text:** Flag 117: CI chondrite fractions — Wasson & Kallemeyn (1988), Lodders
  (2003). Multi-meteorite confirmed.
  File: late_veneer.py
**Triggering signal:** Multi-meteorite confirmed

### Flag 118
**Current text:** Flag 118: k_H = 0.419 ppm/bar — Henry's Law for H2 in peridotitic melt.
  Lab measurement. Earth fallback.
  File: nebular_ingassing.py
**Triggering signal:** Lab measurement

### Flag 119
**Current text:** Flag 119: f_env coefficient 1.06e-5 — Ikoma & Genda (2006).
  Solar-analog calibration. Earth fallback.
  File: nebular_ingassing.py
**Triggering signal:** Earth fallback

### Flag 120
**Current text:** Flag 120: t_disk = 5×(M_star/M_☉)^−0.5 Myr — Mamajek (2009),
  Ribas et al. (2015). Multi-stellar empirical fit.
  Model applicability limit at extreme stellar masses.
  File: nebular_ingassing.py
**Triggering signal:** Model applicability limit

### Flag 122
**Current text:** Flag 122: No saturation above ~200 GPa — extrapolation beyond
  experimental dataset. Model applicability limit.
  File: oxygen_fugacity.py
**Triggering signal:** Model applicability limit

### Flag 123
**Current text:** Flag 123: K1–K6 A, B coefficients — NIST-JANAF. Universal molecular
  thermodynamics. Valid 1200–2500 K only.
  Model applicability limit outside this range.
  File: equilibrium_speciation.py
**Triggering signal:** Model applicability limit

### Flag 124
**Current text:** Flag 124: T_sol,0 = 1400 K — anhydrous peridotite solidus.
  Lab measurement. Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Lab measurement

### Flag 125
**Current text:** Flag 125: γ = 100 K/GPa — solidus Clapeyron slope.
  Lab measurement. Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Lab measurement

### Flag 126
**Current text:** Flag 126: Γ = 10 K/GPa — mantle adiabatic gradient. Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Earth fallback

### Flag 127
**Current text:** Flag 127: dF/dP = 0.12 GPa^−1 — Katz et al. (2003).
  Anhydrous peridotite. Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Earth fallback

### Flag 128
**Current text:** Flag 128: ε_stagnant Gaussian — analytical fit to Dorn et al. (2018)
  + Noack et al. (2017). Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Earth fallback

### Flag 129
**Current text:** Flag 129: ε_mobile = 1.0 — degassing efficiency of melt.
  Idealised upper bound. Earth fallback.
  File: melt_fraction.py
**Triggering signal:** Earth fallback

### Flag 130
**Current text:** Flag 130: Walker (1981) weathering constants — W_0=3.3e14 mol/yr,
  P_CO2_0=3e-4 bar, T_0=285 K, exponent=0.3, sensitivity=13.7 K.
  Earth-empirical. Not applicable without liquid water. Earth fallback.
  File: atmospheric_mass.py
**Triggering signal:** Earth fallback

### Flag 131
**Current text:** Flag 131: FeO supply treated as non-limiting — 8 wt% FeO assumed.
  FeO content not a cascade variable. Earth fallback.
  File: nebular_ingassing.py
**Triggering signal:** Earth fallback

### Flag 132
**Current text:** Flag 132: Equilibrium dissolution assumed — convective mixing
  timescale (days) << disk lifetime (Myr). Model applicability limit
  if magma ocean solidifies before disk dispersal.
  File: nebular_ingassing.py
**Triggering signal:** Model applicability limit

### Flag 133
**Current text:** Flag 133: N post-veneer overshoot — 80/20 mixing delivers ~6 ppm N
  vs 1–2 ppm MORB-source target. Known Ru isotopic tension.
  Model limitation — not patched.
  File: late_veneer.py
**Triggering signal:** Model limitation

### Flag 152
**Current text:** Flag 152: H₂-CO via H₂-N₂ isosteric approximation. Ivakin & Suetin
  (1964) <2% validation per Marrero & Mason (1972). Earth fallback.
  File: b12_coefficients.py.
**Triggering signal:** Earth fallback

### Flag 153
**Current text:** Flag 153: H-O binary diffusion from Zahnle & Kasting (1986). Chapman-
  Enskog with Lennard-Jones parameters. Earth/Solar-System calibrated.
  File: b12_coefficients.py.
**Triggering signal:** Solar-System calibrated

### Flag 158
**Current text:** Flag 158: procedural regime thresholds (0.5/10 bar, 0.5 CH4, 150 K)
  Solar System calibrated. File: regime_router.py.
**Triggering signal:** Solar System calibrated

### Flag 159
**Current text:** Flag 159: column-mean temperature approximation (T_ref = T_eq)
  in τ₀ integration. Model limitation.
  File: tau_zero_compositional.py.
**Triggering signal:** Model limitation

### Flag 160
**Current text:** Flag 160: HITRAN 2020 CIA gray-band averages, Earth/Solar-System
  laboratory measurements, 200–400 K validity. Earth fallback.
  File: cia_coefficients.py.
**Triggering signal:** Earth fallback

### Flag 162
**Current text:** Flag 162: Venus-class shortwave attenuation regime parameters
  (n=1, τ_rc=1.0). Solar-System calibrated.
  File: venus_shortwave_attenuation.py.
**Triggering signal:** Solar-System calibrated

### Flag 163
**Current text:** Flag 163: gray-model Venus-regime applicability limit. T_surface
  biased low by up to ~15% for τ₀ > 100. Model applicability limit.
  File: venus_shortwave_attenuation.py.
**Triggering signal:** Model applicability limit

### Flag 164
**Current text:** Flag 164: Titan tholin shortwave transmission factor f_trans ≈ 0.45.
  Titan-calibrated empirical fallback (Cassini-Huygens in situ).
  File: titan_tholin_anti_greenhouse.py.
**Triggering signal:** Cassini-Huygens in situ

### Flag 165
**Current text:** Flag 165: Jupiter F_int = 5.4 W/m² normalization (Hanel et al. 1981).
  Solar-System calibrated. File: gas_envelope_internal_heat.py.
**Triggering signal:** Solar-System calibrated

### Flag 166
**Current text:** Flag 166: Saturn helium-rain supplement +0.4 W/m². Solar-System
  calibrated; applicability boundary not derived for extrasolar
  gas giants. File: gas_envelope_internal_heat.py.
**Triggering signal:** applicability boundary not derived

### Flag 167
**Current text:** Flag 167: F_int formula valid above 30 M_⊕; sub-Neptune cores
  deviate from H/He polytrope (Lopez & Fortney 2014).
  Model applicability limit. File: gas_envelope_internal_heat.py.
**Triggering signal:** Model applicability limit

### Flag 168
**Current text:** Flag 168: high-T C_p adjustment from JANAF tables. Earth fallback.
  File: moist_adiabat_beta.py.
**Triggering signal:** Earth fallback

### Flag 170
**Current text:** Flag 170: T_mesopause approximated as T_skin in Bates thermosphere
  profile. Model approximation. File: t_p_profile.py.
**Triggering signal:** Model approximation

### Flag 171
**Current text:** Flag 171: photolysis wavelength cutoffs from JPL Data Evaluation
  2020. Earth fallback. File: photolysis_rates.py.
**Triggering signal:** Earth fallback

### Flag 172
**Current text:** Flag 172: effective broadband photolysis cross-sections (gray
  approximation), JPL Data Evaluation, 200–300 K validity.
  Earth fallback. File: photolysis_rates.py.
**Triggering signal:** Earth fallback

### Flag 173
**Current text:** Flag 173: gray photolysis approximation; full wavelength-resolved
  actinic flux integration requires correlated stellar spectrum
  coupling out of current scope. Model limitation; fallback J(O₃)
  from F_XUV when O₃ absent. File: photolysis_rates.py.
**Triggering signal:** Model limitation

### Flag 174b
**Current text:** Flag 174b: default stratospheric O₃ mole fraction when absent from
  V08 speciation. Earth fallback. File: radical_steady_state.py.
**Triggering signal:** Earth fallback

### Flag 175
**Current text:** Flag 175: JPL Arrhenius parameters for OH+H₂S, OH+SO₂. Earth-
  laboratory measured. Earth fallback. File: species_lifetimes.py.
**Triggering signal:** Earth fallback

### Flag 176
**Current text:** Flag 176: mixing-length theory K_zz tropospheric parameterization.
  Earth/Solar-System calibrated. File: eddy_diffusion_kzz.py.
**Triggering signal:** Solar-System calibrated

### Flag 177
**Current text:** Flag 177: Lindzen 1981 gravity-wave breaking K_zz parameterization;
  1–2 orders of magnitude uncertainty for extrasolar atmospheres.
  Earth fallback. File: eddy_diffusion_kzz.py.
**Triggering signal:** Earth fallback

### Flag 178
**Current text:** Flag 178: Kombayashi-Ingersoll Earth-laboratory L_v and reference
  saturation pressure; condensable-specific universal applicability
  not derived. Earth fallback. File: kombayashi_ingersoll_limit.py.
**Triggering signal:** Earth fallback

---

## Cleanup (Remove from Open List)

### Flag 26
**Current text:** **Flag 26** — Duplicate of Flag 34. ε (XUV heating efficiency) empirical,
**Reason:** Duplicate of Flag 34

### Flag 134
**Current text:** - Flag 134: T_surface missing — RESOLVED. Joined-solution closed-form
  delivered with Earth, Mars, Titan, Saturn calibrations.
**Reason:** Resolved

### Flag 151
**Current text:** - Flag 151: H/H₂ identity at exobase blocked on K_zz — RESOLVED with
  Lindzen 1981 fallback (Flag 177 attached).
**Reason:** Resolved

### Flag 154
**Current text:** - Flag 154: H₂S/SO₂ retention — RESOLVED IN PART. Atmospheric
  chemical destruction closed via radical_steady_state.py and
  species_lifetimes.py. Ocean dissolution sink remains blocked on
  V10 topographic variance σ_h and ocean volume outputs.
**Reason:** Resolved

### Flag 155
**Current text:** - Flag 155: crossover mass dissociation fraction blocked on K_zz —
  RESOLVED with Lindzen 1981 fallback (Flag 177 attached).
**Reason:** Resolved

---

## Pending Reclassification (Manual Ruling Required)

### Flag 07
**Current text:** - Flag 07: CMF default — deferred to disk chemistry
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 16
**Current text:** - Flag 16: Metallicity Z — deferred
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 25
**Current text:** - Flag 25: log g★ solar metallicity — Flag 16 dependent
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 32
**Current text:** - Flag 32: Rocky and dwarf semimajor axes use sub-Neptune distribution.
  No separate rocky-only demographic fit exists at required precision.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 33
**Current text:** - Flag 33: Hot Jupiter 1% Bernoulli override — Kepler/RV surveys of Sun-like
  stars only. Not confirmed across all stellar mass ranges.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 35
**Current text:** - Flag 35: R_XUV multipliers (1.0 rocky, 1.1 giant) — empirical, not derived.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 36
**Current text:** - Flag 36: Isotropic obliquity distribution — theoretically motivated,
  unconfirmed observationally for exoplanets.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 37
**Current text:** - Flag 37: Beta eccentricity parameters — Kipping (2013) RV survey; confirmed
  across multiple surveys but with scatter.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 38B
**Current text:**   ⚠️ Flag 38B: empirical GCM calibration. Residual vs Earth: 0.023.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 41
**Current text:** - Flag 41: τ_degas (degassing timescale) Earth-calibrated empirical
  coefficient. Not yet implemented — recorded for when outgassing model
  is added.
**Why ambiguous:** Pending Rule: Entry says "Not yet implemented — recorded for when [model] is added"; from text alone it is ambiguous whether the model is now active or still dormant.

### Flag 42
**Current text:** - Flag 42: Sub-Neptune envelope stripping boundary uses placeholder
  envelope mass fraction (5% of M). Initial envelope mass requires
  protoplanetary disk accretion variable.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 43
**Current text:** - Flag 43: τ_IR greenhouse correction not applied. Scale height and
  surface T use T_eq as approximation. Surface values underestimated
  for planets with significant greenhouse warming.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 44
**Current text:** - Flag 44: Tidal locking atmospheric collapse — confirmed via 3D GCMs,
  no closed-form correction. Deferred to Variable 06.
**Why ambiguous:** Pending Rule: Entry says "Deferred to Variable n" where V_n is V01–V09 (already built), so completion cannot be determined from the flag text alone.

### Flag 47
**Current text:** - Flag 47: Gas giant T_exo is a lower bound only. Giant Planet Energy
  Crisis — internal Joule/auroral heating dominates on stable giants.
  No cascade variable represents this contribution.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 49
**Current text:** - Flag 49: Del Genio (2019) extrapolation at S_ox < 0.3. Category:
  survey-scope limitation.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 53
**Current text:** Deferred — upstream dependency: 07, 16, 25, 42, 43, 44, 53, 91, 96,
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 56
**Current text:** - Flag 56: ρ_crust, Z_crust, P_f, P_o stagnant lid melt constants.
  Earth/Venus analogue calibration.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 57
**Current text:** - Flag 57: T_m(0) = 1,700 K canonical cool-start. Not derivable from
  cascade without accretion timescale.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 58
**Current text:** - Flag 58: T_solidus = 1,500 K sub-Neptune magma ocean gate. Earth
  silicate calibration.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 63
**Current text:** - Flag 63: A_p = 0.50 stagnant lid prefactor. Numerical simulation value.
  No independent planetary calibration available.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 88
**Current text:** Flag 88: CO2 liquid-vapor window (216.58–304.18 K, P_s > 5.185 bar):
  Span-Wagner EOS deferred; engine returns liquid_possible.
  Model limitation.
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 91
**Current text:** Flag 91: Ocean volume and depth blocked — topographic variance sigma_h
  missing. Deferred — upstream dependency.
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 96
**Current text:** Flag 96: D = 0.6 W/m²/K — meridional thermal diffusion coefficient.
  Earth-calibrated. Must scale with rotation rate (∝ Ω⁻²) and
  atmospheric column mass. Rotation rate absent from cascade entirely.
  Two resolution gates: (1) rotation rate research + V05 extension;
  (2) D scaling law derivation and numerical validation.
  Category: Earth fallback + deferred upstream dependency.
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 106
**Current text:** Flag 106: X_max values from Lodders (2003) protosolar abundances.
  Solar-metallicity calibration.
  File: bulk_volatile_fraction.py
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 112
**Current text:** Flag 112: K_D,H = 1 at Mars P_cmb (14 GPa) — H approaches neutral
  below 20 GPa. Lab data.
  File: core_mantle_partitioning.py
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 113
**Current text:** Flag 113: K_D,C = 500 at Mars P_cmb (14 GPa) — C inversely pressure
  dependent. Lab data.
  File: core_mantle_partitioning.py
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 115
**Current text:** Flag 115: Late veneer log-normal μ=−2.3, σ=0.3 — N-body Monte Carlo
  calibration. Solar System calibration.
  File: late_veneer.py
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 156
**Current text:** Flag 156: Binary diffusion coefficients missing for H-CO, H-S, H₂-S,
  H₂-O pairs. Not located in Marrero & Mason (1972), Zahnle & Kasting
  (1986), Tian (2015), Wordsworth et al. (2018), Hu & Seager (2013,
  2014), Loftus et al. (2019), Poling Prausnitz & O'Connell (2001).
  Crossover mass returns None for these pairs. Incomplete empirical
  data. File: b12_coefficients.py; crossover_mass.py.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 161b
**Current text:** Flag 161b: Venus CO₂ 15 µm line term suppressed (CIA continuum
  carries the opacity at 92 bar). Physically defensible regime
  routing decision. File: line_absorption_coefficients.py.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 169
**Current text:** Flag 169: moist adiabat correction Solar-System calibrated
  (Earth 0.19, Titan 0.20); full first-principles derivation
  deferred. File: moist_adiabat_beta.py.
**Why ambiguous:** Pending Rule: Entry uses bare "deferred" with no target variable and no research prompt phrase.

### Flag 174
**Current text:** Flag 174: chemical reaction rate constants from JPL Data Evaluation
  grids. Earth-laboratory measured, 200–400 K validity. Earth
  fallback. File: radical_steady_state.py.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.

### Flag 179
**Current text:** Flag 179: gas envelope uses 1 bar reference P_s when cascade P_s
  is None; resulting T_surface is temperature at 1 bar reference,
  not physical surface. Procedural choice for sub-Neptunes/gas
  giants. File: gas_envelope_internal_heat.py.
**Why ambiguous:** Pending Rule: The flag wording does not match any signal cleanly.
