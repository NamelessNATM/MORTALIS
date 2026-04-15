# MORTALIS World Engine — Changelog

---
## Scaffold 001 — Project Skeleton
**Date:** 2026-04-11
**Type:** Scaffold

### What was created
Full project folder structure established. No physics implemented.

### Files created
- `main.py` — entry point stub; `run(seed)` function; no physics
- `changelog.md` — this file
- `README.md` — project summary and usage stub
- `variable_01_mass/` — `__init__.py` + entry point stub
- `variable_02_composition/` — `__init__.py` + entry point stub
- `variable_03_stellar/` — `__init__.py` + entry point stub
- `variable_04_atmosphere/` — `__init__.py` + entry point stub
- `variable_05_kinematics/` — `__init__.py` + entry point stub
- `variable_06_tectonics/` — `__init__.py` + entry point stub
- `variable_07_hydrology/` — `__init__.py` + entry point stub
- `variable_08_regolith/` — `__init__.py` + entry point stub
- `variable_09_biology/` — `__init__.py` + entry point stub

### Physics implemented
None.

### Flags open
None at this stage.

### Next step
Variable 01: Planetary Mass — sub-function files to be specified and implemented.

---
## Scaffold 002 — Variable 01: Planetary Mass
**Date:** 2026-04-11
**Type:** Implementation

### What was implemented
Full implementation of Variable 01: Planetary Mass. Five sub-function files
created. Entry point updated. main.py updated to call Variable 01.

### Files created
- `variable_01_mass/planetary_mass_boundaries.py` — M_min and M_max
- `variable_01_mass/mass_pdf.py` — four-regime piecewise power-law PDF
- `variable_01_mass/mass_cdf.py` — normalised CDF with continuity conditions
- `variable_01_mass/mass_sampler.py` — inverse transform sampling, seed → M
- `variable_01_mass/gravitational_parameter.py` — mu = GM

### Files modified
- `variable_01_mass/variable_01_mass.py` — entry point implemented
- `main.py` — Variable 01 wired into cascade

### Physics implemented
**Lower boundary (M_min):** Hydrostatic equilibrium threshold derived from
integrating dP/dr = -rho*g(r) for a uniform sphere and equating central
pressure to material yield strength sigma_rbf. Formula:
M_min = (9 / (2*rho^2)) * (sigma_rbf / (pi*G))^(3/2)
Earth benchmark: sigma_rbf=10e6 Pa, rho=3500 kg/m^3 → M_min ~ 10^18-10^21 kg.

**Upper boundary (M_max):** Deuterium burning threshold at 13 M_J.
Derived from polytropic contraction (n=1.5 Lane-Emden) — numerical
convention, not closed-form. Range 11.0–16.3 M_J depending on metallicity.

**Mass sampling:** Inverse transform sampling on a four-regime bias-corrected
piecewise power-law PDF. Regimes and exponents from Abel-inverted RV + transit
survey demographics (Marcy et al. 2005; Howard et al. 2010; Tremaine & Dong
2012).

**Gravitational parameter:** mu = GM. Derived from Newton's laws.
Earth benchmark: 3.986×10^14 m^3 s^-2 ✓

### Cascade outputs
- M_kg — planetary mass [kg]
- mu   — standard gravitational parameter [m^3 s^-2]

### Flags open
- Flag 01: g, v_e, P_c require radius R — deferred to Variable 02
- Flag 02: R_H requires stellar mass and semimajor axis — deferred to Variable 05
- Flag 04: sigma_rbf is Earth-measured — M_min is composition-dependent
  ⚠️ EARTH FALLBACK on all files using yield strength values
- Flag 05: All power-law alpha exponents and desert suppression factor 1/7.7
  are empirical fits confirmed across multiple planetary bodies
- Flag 06: 13 M_J upper boundary is a simulation-derived convention

### Validation
All five Earth calibration benchmarks from research session confirmed
numerically before implementation was authorised.
CDF normalisation assertion: cumulative[-1] must equal 1.0 ± 1e-10.

### Next step
Variable 02: Bulk Composition — research prompt to be written.
Research must establish: what determines a planet's bulk composition and
internal structure, and what does that produce as a function of M?

---

## Session Close — Variable 01 Complete
**Date:** 2026-04-11
**Type:** Status

### Status
Variable 01 is fully implemented, tested, and locked. No open work remains
in this variable.

### Confirmed passing
- `compute_cdf_tables` produces `cumulative[-1] == 1.0`
- `run_variable_01(42)` is deterministic across repeated calls
- `main.run(42)` matches `run_variable_01(42)` output
- No linter issues on any modified file

### Next session
Variable 02: Bulk Composition — to be opened in a separate thread.
First act of that session: Gemini deep research prompt.
Variable 02 scope is fully undetermined until research returns.

---
## Scaffold 003 — Variable 02: Bulk Composition & Radius
**Date:** 2026-04-11
**Type:** Implementation

### What was implemented
Variable 02 maps mass to compositional regime, applies regime-specific
mass–radius relations, and derives bulk surface and interior proxy quantities.

### Files created
- `variable_02_composition/regime_classifier.py` — four-regime classification from M [kg]
- `variable_02_composition/mass_radius_rocky.py` — Zeng et al. 2016 rocky M–R
- `variable_02_composition/mass_radius_subneptune.py` — Chen & Kipping / Otegi et al. sub-Neptune M–R
- `variable_02_composition/mass_radius_gasgiant.py` — Bashi et al. 2017 gas-giant M–R
- `variable_02_composition/surface_gravity.py` — g = GM/R²
- `variable_02_composition/escape_velocity.py` — v_e = sqrt(2GM/R)
- `variable_02_composition/central_pressure.py` — uniform-sphere P_c = 3GM²/(8πR⁴)
- `variable_02_composition/mean_density.py` — rho_mean = M / (4/3 π R³)

### Files modified
- `variable_02_composition/variable_02_composition.py` — full entry point: regime routing, derived quantities, brown-dwarf domain exclusion
- `main.py` — Variable 02 wired; returns `v01` and `v02`
- `changelog.md` — this entry

### Physics implemented (with sources)
| Quantity | Formula / model | Source |
|----------|-----------------|--------|
| Regime boundaries | 4.4 M_⊕, 127 M_⊕, 13 M_J | Research session 2026-04-11 |
| Rocky R | (1.07 − 0.21·CMF)(M/M_⊕)^(1/3.7) R_⊕ | Zeng et al. 2016 |
| Sub-Neptune R | R = 0.56 M^0.67 (R,M in Earth units) | Chen & Kipping 2017; Otegi et al. 2020 |
| Gas-giant R | R = 18.6 M^(−0.06) (R,M in Earth units) | Bashi et al. 2017 |
| g | GM/R² | Newton (Rule 1 B) |
| v_e | sqrt(2GM/R) | Energy conservation (Rule 1 B) |
| P_c | 3GM²/(8πR⁴) | Uniform-density hydrostatic shell (Rule 1 B, caveat) |
| rho_mean | M / (4/3 π R³) | Definition (Rule 1 B) |

### Flags open
- **Flag 07:** CMF defaults to 0.325 (Earth). No disk chemistry variable in cascade yet. Deferred.
- **Flag 08:** Compositional degeneracy ~2–10 M_⊕; regime boundary is a statistical threshold, not a knife-edge.
- **Flag 09:** Rocky M–R coefficients from PREM / Earth only — EARTH FALLBACK; universal applicability not confirmed.
- **Flag 10:** Water phase state (Ice VII vs. supercritical steam) is underdetermined from mass alone. Planets in the 2–4 R_earth range may compress water into high-density solid phases or retain it as an inflated supercritical steam envelope depending on stellar equilibrium temperature. Deferred to stellar insolation variable. Source: research session 2026-04-11.
- **Flag 11:** Central pressure uses uniform-density assumption — approximate lower bound; real P_c higher (differentiation).
- **Flag 12:** Bashi et al. gas-giant fit: **17% Jupiter overestimate** (formula as in literature; not a patch candidate).

### Calibration notes (session benchmarks)
- **Earth (rocky formula):** M = 1 M_⊕, CMF = 0.325 → R = 1.00175 R_⊕ (0.17% error).
- **Earth (derived):** g ≈ 9.82 m/s² vs 9.807 (rounding); rho_mean = 5,514 kg/m³ ✓; v_e = 11,186 m/s ✓; P_c ≈ 171 GPa vs ~364 GPa (expected underestimate, Flag 11).
- **Neptune (sub-Neptune formula):** M = 17.15 M_⊕ → R = 3.69 R_⊕ vs 3.865 (4.5% — acceptable empirical fit).
- **Jupiter (gas-giant Formula 9 / Bashi):** M = 318 M_⊕ → R = 13.15 R_⊕ vs 11.21 known (**17% overestimate**, Flag 12).

### Next step
Variable 03 — Stellar Insolation (research prompt to be written).

---
## Scaffold 003a — Variable 02 Patch: Dwarf Regime
**Date:** 2026-04-11
**Type:** Patch

### Root cause
Zeng et al. 2016 formula applied six orders of magnitude below its valid domain,
producing rho_mean = 374 kg/m^3 (physically impossible for rock).

### Fix
Geometric uncompressed formula R = (3M / (4πρ₀))^(1/3) for the sub-hydrostatic
dwarf regime (M < 1e24 kg). Formula was already present in research session
2026-04-11 Section 3.1 — not a new research requirement.

### Flags
- **Flag 13 opened:** rho_0 defaults to 3500 kg/m^3 (Earth fallback).

### Calibration
- Ceres: 0.9% error on known radius.

### Expected outcome
Seed 1 re-run expected to produce physically sensible rho_mean ~3500 kg/m^3.


## Scaffold 004 — Variable 03: Stellar Properties
**Date:** 2026-04-11
**Type:** Implementation

### What was implemented
Variable 03 samples a host star deterministically from a seed. It produces
stellar mass, stability classification, age, luminosity, radius, effective
temperature, main-sequence lifetime, and XUV luminosity. All outputs depend
only on the seed — no v01 or v02 inputs are passed in at this stage. Orbital
coupling is deferred to Variable 05.

### Files created
- `variable_03_stellar/stellar_mass_sampler.py` — Kroupa (2001) IMF, inverse
  transform sampling, renormalised over Eker MLR valid domain (0.179–31 M☉).
  Regime 1 (0.01–0.179 M☉) excluded to prevent MLR ValueError. Documented
  as design decision.
- `variable_03_stellar/stellar_stability.py` — three-outcome stability
  classification per Flag 19 Option B: unstable_low (<0.5 M☉), stable
  (0.5–1.5 M☉), unstable_high (>1.5 M☉). Full mass range passes forward;
  unstable stars tagged, not discarded.
- `variable_03_stellar/stellar_age_sampler.py` — Just & Jahreiß (2010) Model A
  SFH; closed-form CDF integral I(t); scipy.optimize.brentq root-finding;
  mass-conditional τ_min and τ_max bounds. Returns age_Gyr and τ_frac.
- `variable_03_stellar/mass_luminosity.py` — Eker et al. (2018) six-regime
  piecewise MLR. Returns L_star_solar and L_star_W.
- `variable_03_stellar/mass_radius_lowmass.py` — Eker et al. (2018) quadratic
  MRR. Valid for M★ ≤ 1.5 M☉.
- `variable_03_stellar/surface_gravity_evolution.py` — log g★(M★, τ_frac)
  fitted to PARSEC v1.2S isochrone grids at solar metallicity. Valid for
  M★ > 1.5 M☉. Flag 25 applies.
- `variable_03_stellar/stellar_radius_highmass.py` — Torres (2010) exact
  gravitational identity log(R/R☉) = 0.5·log(M/M☉) − 0.5·(log g − 4.438).
  Valid for M★ > 1.5 M☉.
- `variable_03_stellar/stellar_temperature.py` — Stefan-Boltzmann law. Sole
  T_eff derivation path for both mass regimes. MTR excised (Flag 24).
- `variable_03_stellar/main_sequence_lifetime.py` — simplified scaling law
  t_MS = 10·(M/M☉)^(−2.5) Gyr. Hurley (2000) precision model deferred
  pending metallicity (Flag 16).
- `variable_03_stellar/xuv_luminosity.py` — Ribas (2005) saturation and
  power-law decay model. Returns L_XUV_fraction and L_XUV_W.

### Files modified
- `variable_03_stellar/variable_03_stellar.py` — entry point fully implemented;
  orchestrates all ten sub-functions; no physics directly
- `main.py` — Variable 03 wired into cascade; v03 print block added
- `requirements.txt` — scipy added for brentq
- `changelog.md` — this entry

### Physics implemented
| Quantity | Formula / model | Source |
|---|---|---|
| M★ | Kroupa (2001) broken power-law IMF, ITS | Kroupa 2001 |
| Stability | 0.5 / 1.5 M☉ thresholds | Eker 2018; Ribas 2005 |
| age, τ_frac | Just & Jahreiß (2010) Model A SFH + brentq | JJ 2010 |
| L★ | Six-regime piecewise MLR | Eker 2018 |
| R★ (low-mass) | Quadratic MRR | Eker 2018 |
| log g★ | PARSEC isochrone polynomial (M★, τ_frac) | PARSEC v1.2S |
| R★ (high-mass) | Torres (2010) gravitational identity | Torres 2010; Moya 2018 |
| T_eff | Stefan-Boltzmann from L and R | Rule 1 Category A |
| t_MS | 10·(M/M☉)^(−2.5) Gyr | Scaling law |
| L_XUV | Ribas (2005) saturation + decay | Ribas 2005 |

### Design note — IMF domain restriction
The Kroupa IMF is defined over 0.01–150 M☉. The Eker (2018) MLR is valid only
over 0.179–31 M☉. To avoid MLR ValueError on low-mass draws, the IMF sampler
renormalises the CDF over the MLR-compatible overlap (0.179–31 M☉), excluding
regime 1 entirely. This is a documented architectural constraint, not a silent
patch. It means the engine does not currently generate stars below 0.179 M☉.
This should be revisited if a luminosity model for ultra-low-mass stars is
added in a future session.

### Calibration notes
- L(1.0 M☉) = 0.984 L☉ (−1.6%, physically expected — empirical MLR averages
  over main-sequence ages)
- R(1.0 M☉) = 0.992 R☉ (−0.8%, same cause)
- T_eff(L☉, R☉) = 5772 K ✓
- t_MS(1.0 M☉) = 10.0 Gyr ✓
- XUV at 4.57 Gyr: 9.08×10⁻⁶ (within observed solar cycle range ✓)
- Torres identity: Sirius A −4.9%, Fomalhaut −2.2%, Vega −8.7% (residual
  from oblate geometry, not formula error)
- Median age for 1.0 M☉ at U=0.5: verified numerically as 6.58 Gyr (research
  document reported 5.6 Gyr — discrepancy due to rounding in manual integral
  evaluation; brentq result is authoritative)

### Seed 1 verified output
- Planet: dwarf regime, M = 4.11×10¹⁸ kg
- Star: M★ = 0.2187 M☉, unstable_low, age = 1.40 Gyr
- T_eff = 3399 K, R★ = 0.201 R☉, L★ = 0.00484 L☉
- t_MS = 447 Gyr, L_XUV/L = 3.88×10⁻⁵
- Map: uniform dwarf colour (160, 140, 120) — correct; V03 adds no grid layers

### Flags opened this session
- Flag 20: Kroupa α exponents empirical — inherent to model
- Flag 22: JJ2010 SFH parameters — Milky Way solar neighbourhood only
- Flag 23: τ_min anchor — Earth/Solar System only
- Flag 24: MTR excised from high-mass radius and temperature paths
- Flag 25: log g★ coefficients fitted at solar metallicity only

### Flags resolved this session
- Flag 15: Stellar age — resolved as JJ2010 SFH with brentq sampling
- Flag 17: High-mass radius calibration — resolved; three-step path rejected;
  Torres identity adopted
- Flag 18: Stellar wind Ṁ — moved to Variable 04 or 05; V03 outputs L_XUV only
- Flag 19: Stability filter — resolved as Option B (tag and pass, full range)
- Flag 21: log g★ evolution formula — resolved via PARSEC isochrone fit

### Flags still open
- Flag 02: Hill radius — deferred to Variable 05
- Flag 04: σ_rbf universality — Earth fallback
- Flag 05: Power-law alpha exponents — inherent
- Flag 06: 13 M_J upper boundary — review if metallicity added
- Flag 07: CMF default — deferred to disk chemistry
- Flag 08: Compositional degeneracy — inherent
- Flag 09: Rocky M-R universality — Earth fallback
- Flag 10: Water phase state — deferred to Variable 03 stellar insolation
- Flag 11: Uniform density P_c — inherent approximation
- Flag 12: Bashi gas-giant 17% overestimate — inherent to model
- Flag 13: Dwarf rho_0 — Earth fallback
- Flag 14: BC polynomial coefficients — deferred
- Flag 16: Metallicity Z — deferred
- Flag 20: Kroupa α empirical — inherent
- Flag 22: JJ2010 single measurement context — inherent
- Flag 23: τ_min anchor — Earth fallback
- Flag 25: log g★ solar metallicity — Flag 16 dependent

### Next step
Variable 04: Atmosphere — research prompt to be written.

---
## Scaffold 005 — Variable 05: Planetary Kinematics
**Date:** 2026-04-11
**Type:** Implementation

### What was implemented
Variable 05 samples semimajor axis and eccentricity from empirically
established demographic distributions, derives all orbital and insolation
quantities, and provides the orbital inputs that Variable 04 (atmosphere)
requires. Obliquity is sampled from an isotropic distribution.

### Files created
- `variable_05_kinematics/__init__.py` — empty
- `variable_05_kinematics/roche_limit.py` — fluid Roche limit inner boundary
- `variable_05_kinematics/disk_outer_boundary.py` — ALMA scaling outer boundary
- `variable_05_kinematics/semimajor_axis_sampler.py` — regime-conditioned broken
  power-law inverse-CDF sampler with hot Jupiter override
- `variable_05_kinematics/orbital_eccentricity_sampler.py` — Beta(0.867, 3.03)
  sampler with tidal circularisation cutoff and Roche periapsis floor
- `variable_05_kinematics/stellar_flux.py` — orbit-averaged bolometric and XUV flux
- `variable_05_kinematics/equilibrium_temperature.py` — Stefan-Boltzmann T_eq
  with regime-based albedo placeholders
- `variable_05_kinematics/hill_radius.py` — three-body restricted problem Hill radius
- `variable_05_kinematics/orbital_period.py` — Kepler's third law exact two-body form
- `variable_05_kinematics/obliquity_sampler.py` — isotropic spin axis sampling
- `variable_05_kinematics/atmospheric_escape.py` — energy-limited XUV escape rate
- `variable_05_kinematics/variable_05_kinematics.py` — entry point; no physics directly

### Files modified
- `main.py` — Variable 05 wired into cascade; v05 print block added

### Physics implemented
| Quantity | Formula / model | Source |
|---|---|---|
| a_Roche | 2.44 R★ (ρ★/ρ_planet)^(1/3) | Roche (1849); universal |
| a_max | 100 AU × (M★/M☉)^0.5 | Andrews et al. (2018) ALMA; Flag 31 |
| a | Broken power-law inverse-CDF, regime-conditioned | Fernandes et al. (2019); Hsu et al. (2019) |
| e | Beta(0.867, 3.03) with tidal and Roche floors | Kipping (2013); Flag 37 |
| obliquity | cos(obliquity) uniform [-1,1] | Agnor et al. (1999); Flag 36 |
| T_orb | 2π √(a³/(μ★+μ_planet)) | Newton (Principia); universal |
| ⟨F⟩ | L★ / (4π a² √(1-e²)) | Murray & Dermott (1999); universal |
| F_XUV | L_XUV / (4π a² √(1-e²)) | Same derivation; universal |
| T_eq | ((1-A)⟨F⟩ / 4σ)^(1/4) | Selsis et al. (2007); universal |
| R_H | a (M / 3M★)^(1/3) | Hill (1878); universal |
| Ṁ | ε π R_XUV³ F_XUV / GM | Watson et al. (1981); Flags 34, 35 |

### Research path
Three Gemini research prompts required for this variable:
1. Initial Variable 05 prompt — established all formulas and sampling distributions
2. Follow-up prompt (Gaps 1 and 2) — resolved outer disk boundary and semimajor
   axis distribution functional form
3. Second follow-up prompt — resolved calibration failures in Toomre and
   photoevaporation formulas; established Candidate A (ALMA scaling) as a_max.
   Candidate C (internal photoevaporation, a_max = 9.2 AU for 1 M☉) rejected
   because it excludes outer solar system analogues.

### Calibration verified numerically (pre-implementation)
- ⟨F⟩ at Earth: 1361.3 W/m² (target 1361) ✓
- T_eq at Earth, A=0.30: 254.6 K (target 255 K) ✓
- R_H at Earth: 1.496×10⁹ m (target 1.496×10⁹ m) ✓
- T_orb at Earth: 365.3 days (target 365.25 days) ✓
- a_Roche Earth/Sun: 0.0072 AU (Earth orbit at 1 AU well outside) ✓

### Seed outputs verified numerically (post-implementation)
- Seed 1: a=0.1108 AU, e=0.094, T_eq=215.1 K, T_orb=28.8 days — all verified ✓
- Seed 42: a=0.5450 AU, e=0.229, T_eq=168.7 K — all verified ✓
- Periapsis > Roche limit confirmed both seeds ✓
- M_dot timescale for seed 1 (~13 Myr) correctly signals rapid atmospheric
  stripping for a dwarf body at 0.11 AU — physically consistent ✓

### Flags opened this session
- Flag 31: a_max ALMA scaling — single-survey approximation; varies between
  star-forming regions. Candidate C rejected (see research path above).
- Flag 32: Rocky and dwarf semimajor axes use sub-Neptune distribution.
  No separate rocky-only demographic fit exists at required precision.
- Flag 33: Hot Jupiter 1% Bernoulli override — Kepler/RV surveys of Sun-like
  stars only. Not confirmed across all stellar mass ranges.
- Flag 34: ε = 0.15 XUV heating efficiency — Solar System calibrated only.
- Flag 35: R_XUV multipliers (1.0 rocky, 1.1 giant) — empirical, not derived.
- Flag 36: Isotropic obliquity distribution — theoretically motivated,
  unconfirmed observationally for exoplanets.
- Flag 37: Beta eccentricity parameters — Kipping (2013) RV survey; confirmed
  across multiple surveys but with scatter.
- Flag 38: Bond albedo placeholders (rocky 0.30, giant 0.50, dwarf 0.10) —
  Solar System calibrated. Must be revised when Variable 04 runs.

### Flags resolved this session
- Flag 02: Hill radius — resolved; implemented in hill_radius.py

### Variable 04 unblocked
Variable 04 (atmosphere) now has all required orbital inputs:
F_mean, F_XUV, T_eq, M_dot, a, e, R_H. Implementation can proceed.

### Flags still open
02 (resolved this session), 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14,
16, 20, 22, 23, 25, 26, 27, 28, 29, 30, 31–38.

### Next step
Variable 04: Atmosphere — now unblocked. Research was already completed
in the prior session. Implementation prompt to be written.

---
## Scaffold 005a — Flag Record Recovery
**Date:** 2026-04-12
**Type:** Correction

### What was corrected
Scaffold 005 close-out listed Flags 26–30 as open but provided no definitions.
Flag 14 was opened in Scaffold 004 but its definition was not recorded in the
changelog. Both omissions were Rule 9 violations — work existed in the research
record that was not captured in the changelog. This entry corrects the record.

### No code was changed
This entry is a changelog correction only. No implementation files were created
or modified.

### Flag 14 — defined and recorded
**File:** No implementation exists. Deferred.
**What it is:** Eker et al. (2020) BC polynomial coefficients as reproduced in
the V03 research response fail numerical solar calibration by 1.4 magnitudes
(research claimed −0.016; independent validation returned +1.4). The polynomial
is numerically ill-conditioned — large coefficients, high degree, near-total
cancellation at the solar T_eff value. The BC polynomial was never authorised
for implementation as a result.
**Resolution path:** Confirm coefficients directly from Eker et al. (2020)
paper source and re-validate numerically before any implementation is authorised.

### Flags 26–30 — defined and recorded
These flags were opened in the V04 research analysis session and marked as
pre-registered — to be formally entered when V04 is implemented. They exist
in the research record but not yet in the codebase.

**Flag 26** — Duplicate of Flag 34. ε (XUV heating efficiency) empirical,
non-universal. Earth/Venus/Mars suggest 0.1–0.3. Solar System only.
When V04 is implemented, Flags 26 and 34 should be merged into a single entry.

**Flag 27** — λ_crit threshold of 15–20 for Jeans escape is kinetic-theory
derived but the specific value encodes assumptions about geological timescales.
Confirmed empirically across Solar System atmospheres only. Not yet in codebase.

**Flag 28** — c_p for rocky planet atmospheres is composition-dependent and
not derivable from mass alone without volatile inventory and mantle chemistry.
Not yet in codebase.

**Flag 29** — Rocky planet atmospheric composition underdetermined without
mantle oxygen fugacity. Deferred to a future disk chemistry or geochemistry
variable. Not yet in codebase.

**Flag 30** — M_atm (atmospheric column mass) for rocky planets requires
orbital-dependent escape history. Deferred to post-Variable 05. Not yet in codebase.

### Source
Flag 14: V03 research analysis session, numerical validation block.
Flags 26–30: V04 research analysis session, "Flags to open when V04 is
eventually implemented" section.

### Flags still open (complete list as of this entry)
Inherent to model: 05, 08, 11, 12, 20, 22, 37
Earth fallbacks: 04, 09, 13, 23
Deferred — upstream dependency: 06, 07, 10, 16, 25, 28, 29, 30
Deferred — implementation not yet authorised: 14, 27
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 38
Pre-registered duplicates: 26 (= Flag 34)

### Next step
V04 implementation. All flags are now defined and the record is complete.
The research for V04 was completed prior to Scaffold 005 and established
that V05 must run before V04 can produce complete outputs. V05 is complete.
V04 is now fully unblocked.

## Scaffold 006 — Variable 04: Atmosphere
**Date:** 2026-04-12
**Type:** Implementation

### What was implemented
Variable 04 maps planetary regime and orbital inputs to an atmospheric
classification and structure. It runs after Variable 05 in the cascade,
consuming orbital flux inputs that were unavailable during the original
V04 research session. A two-pass architecture resolves the circularity
between T_exo and atmospheric composition.

### Files created
- `variable_04_atmosphere/exobase_temperature.py` — corrected conduction
  model T_exo = T_eq + (ε F_XUV α H_0) / K_c with H_0 = k_B T_eq / (m_mean g).
  Pass-1 m_mean assigned from regime; optional m_mean_kg parameter for
  Pass-2 refinement. Returns None for dwarf and brown_dwarf regimes.
- `variable_04_atmosphere/jeans_parameter.py` — Jeans escape parameter
  lambda per species (H, He, O, H2O, N2, CO2). Returns lambda and
  retained flag per species.
- `variable_04_atmosphere/regime_classifier.py` — atmospheric class and
  dominant composition from regime, Jeans results, and M_dot * age.
  Classes: none, primary_retained, primary_stripped, secondary_possible,
  exosphere_only.
- `variable_04_atmosphere/surface_pressure.py` — P_s = M_atm * g / (4πR²).
  Returns 0.0 for no atmosphere, None for all other cases (M_atm blocked
  by Flag 40 for rocky; no solid surface for giants).
- `variable_04_atmosphere/lapse_rate.py` — Gamma_d = g / c_p per
  composition class. c_p values: H2/He 12,000 J/(kg·K) (Jupiter/Saturn
  confirmed); N2/CO2 rocky 1,004 J/(kg·K) (Earth default, Flag 28).
- `variable_04_atmosphere/scale_height.py` — H = R* T_eq / (mu g).
  Uses T_eq as temperature approximation (Flag 43). Returns None for
  no-atmosphere cases.
- `variable_04_atmosphere/variable_04_atmosphere.py` — entry point.
  Two-pass flow: Pass 1 with regime-default m_mean; Pass 2 if dominant
  species fails Jeans retention (H for giants, N2+CO2 for rocky).
  No physics directly.

### Files modified
- `variable_04_atmosphere/variable_04_atmosphere.py` — stub replaced
  with full implementation (listed above as created)
- `main.py` — Variable 04 import and call added after Variable 05;
  cascade order: v01 → v02 → coordinate_system → v03 → v05 → v04 →
  map_generator; active_variables includes v04; print block added.

### Research path
Three research sessions required for this variable:
1. Initial V04 research — established that V05 must run before V04;
   all major outputs deferred pending orbital inputs.
2. V04 follow-up (post-V05) — supplied full formula set with orbital
   inputs in scope. T_exo formula contained a length-scale error
   (R used instead of α H_0). Formula failed Earth calibration by
   factor ~96.
3. T_exo correction prompt — established correct characteristic length
   as α × H_0 (α = 7 pressure depth scale heights). Corrected formula
   reproduces Earth T_exo ~1,038 K from Earth inputs. ✓

### Physics implemented
| Quantity | Formula | Source |
|---|---|---|
| T_exo | T_eq + (ε F_XUV α H_0) / K_c | Watson et al. 1981; Erkaev et al. 2013 |
| H_0 | k_B T_eq / (m_mean g) | Ideal gas law + hydrostatic equilibrium |
| λ per species | v_e² / v_th² | Chamberlain & Hunten 1987 |
| Γ_d | g / c_p | First Law of Thermodynamics |
| H | R* T_eq / (μ g) | Ideal gas law + hydrostatic equilibrium |
| P_s | M_atm g / (4π R²) | Hydrostatic equilibrium |

### Calibration verified
- T_exo Earth-analog: 1,038 K (target ~1,000–1,200 K) ✓
- λ_H Earth: 7.29 < 15 (H escapes) ✓
- λ_N2 Earth: 202.9 > 15 (N2 retained) ✓
- λ_CO2 Earth: 319 > 15 (CO2 retained) ✓
- Γ_d Earth: 9.77 K/km (target 9.8 K/km) ✓
- Γ_d Jupiter: 2.07 K/km (target ~2.0 K/km) ✓
- H Earth: 7,454 m (T_eq used; lower than 8,500 m surface value,
  expected per Flag 43) ✓

### Seed outputs verified (post-implementation, python main.py)
- Seeds 1, 7, 42: all dwarf regime. T_exo = None, P_s = 0.0,
  atm_class = none, notes correct. No NaN, no crashes. ✓
- Rocky/gas giant/sub-Neptune branches verified via targeted diagnostic
  script with Earth-analog, Jupiter-analog, and sub-Neptune inputs.

### Known behaviour note
T_exo for dwarf bodies is not computed (returns None). In prior
implementation T_exo was computed for dwarfs and returned physically
meaningless extreme values (~4,000–95,000 K) because the conduction
model requires a continuum atmosphere. The corrected implementation
correctly short-circuits at the dwarf check.

### Flags opened this session
- Flag 39: K_c (thermospheric thermal conductivity) is gas-dependent,
  lab-measured. O/N2: 0.05 W/m/K; H2/He: 0.30 W/m/K.
  Source: Banks & Kockarts (1973).
- Flag 40: X_vol (mantle volatile fraction) has no cascade origin.
  M_atm for rocky planets blocked. P_s = None for rocky until disk
  chemistry variable added.
- Flag 41: τ_degas (degassing timescale) Earth-calibrated empirical
  coefficient. Not yet implemented — recorded for when outgassing model
  is added.
- Flag 42: Sub-Neptune envelope stripping boundary uses placeholder
  envelope mass fraction (5% of M). Initial envelope mass requires
  protoplanetary disk accretion variable.
- Flag 43: τ_IR greenhouse correction not applied. Scale height and
  surface T use T_eq as approximation. Surface values underestimated
  for planets with significant greenhouse warming.
- Flag 44: Tidal locking atmospheric collapse — confirmed via 3D GCMs,
  no closed-form correction. Deferred to Variable 06.
- Flag 45: Mass sampler draws from galactic demographic PDF. Rocky or
  larger bodies occur with probability ~10⁻¹¹. Engine cannot generate
  habitable worlds in normal operation. Requires design decision:
  conditioned draw or two-stage architecture. Research prompt required
  before any implementation.
- Flag 46: α = 7 (pressure depth factor) theoretically universal from
  ln(P_meso/P_XUV) ≈ ln(10³). Empirically confirmed on Earth and Mars
  only.
- Flag 47: Gas giant T_exo is a lower bound only. Giant Planet Energy
  Crisis — internal Joule/auroral heating dominates on stable giants.
  No cascade variable represents this contribution.

### Flags resolved this session
- Flag 10: Water phase state — resolved via Jeans retention logic in
  regime_classifier.py. Phase state follows from T_eq (V05) and
  atmospheric class.
- Flag 27: λ_crit = 15–20 — implemented with Flag 27 documentation.
  Chamberlain & Hunten (1987) threshold applied.
- Flag 28: c_p for rocky atmospheres — implemented with Earth-mix
  default and Flag 28 documentation. Known values applied per regime.
- Flag 30: M_atm deferred — formally stubbed. P_s returns None for
  rocky with Flag 40 documentation.

### Flags still open
Inherent to model: 05, 08, 11, 12, 20, 22, 37
Earth fallbacks: 04, 09, 13, 23, 39, 41
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44
Deferred — design decision required: 45
Deferred — implementation not yet authorised: 14
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 38, 46
Model lower bound only: 47
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Flag 45 requires a design decision before Variable 06 can be built on
a functional engine. The mass sampler must be addressed — either via a
conditioned draw for game world generation or a two-stage architecture.
Research prompt to be written before any implementation proceeds.

## Scaffold 006 — Variable 04: Atmosphere
**Date:** 2026-04-12
**Type:** Implementation

### What was implemented
Variable 04 maps planetary regime and orbital inputs to an atmospheric
classification and structure. It runs after Variable 05 in the cascade,
consuming orbital flux inputs that were unavailable during the original
V04 research session. A two-pass architecture resolves the circularity
between T_exo and atmospheric composition.

### Files created
- `variable_04_atmosphere/exobase_temperature.py` — corrected conduction
  model T_exo = T_eq + (ε F_XUV α H_0) / K_c with H_0 = k_B T_eq / (m_mean g).
  Pass-1 m_mean assigned from regime; optional m_mean_kg parameter for
  Pass-2 refinement. Returns None for dwarf and brown_dwarf regimes.
- `variable_04_atmosphere/jeans_parameter.py` — Jeans escape parameter
  lambda per species (H, He, O, H2O, N2, CO2). Returns lambda and
  retained flag per species.
- `variable_04_atmosphere/regime_classifier.py` — atmospheric class and
  dominant composition from regime, Jeans results, and M_dot * age.
  Classes: none, primary_retained, primary_stripped, secondary_possible,
  exosphere_only.
- `variable_04_atmosphere/surface_pressure.py` — P_s = M_atm * g / (4πR²).
  Returns 0.0 for no atmosphere, None for all other cases (M_atm blocked
  by Flag 40 for rocky; no solid surface for giants).
- `variable_04_atmosphere/lapse_rate.py` — Gamma_d = g / c_p per
  composition class. c_p values: H2/He 12,000 J/(kg·K) (Jupiter/Saturn
  confirmed); N2/CO2 rocky 1,004 J/(kg·K) (Earth default, Flag 28).
- `variable_04_atmosphere/scale_height.py` — H = R* T_eq / (mu g).
  Uses T_eq as temperature approximation (Flag 43). Returns None for
  no-atmosphere cases.
- `variable_04_atmosphere/variable_04_atmosphere.py` — entry point.
  Two-pass flow: Pass 1 with regime-default m_mean; Pass 2 if dominant
  species fails Jeans retention. No physics directly.

### Files modified
- `variable_04_atmosphere/variable_04_atmosphere.py` — stub replaced
  with full implementation (listed above as created)
- `main.py` — Variable 04 import and call added after Variable 05;
  cascade order: v01 → v02 → coordinate_system → v03 → v05 → v04 →
  map_generator; active_variables includes v04; print block added.

### Research path
Three research sessions required for this variable:
1. Initial V04 research — established that V05 must run before V04;
   all major outputs deferred pending orbital inputs.
2. V04 follow-up (post-V05) — supplied full formula set with orbital
   inputs in scope. T_exo formula contained a length-scale error
   (R used instead of α H_0). Formula failed Earth calibration by
   factor ~96.
3. T_exo correction prompt — established correct characteristic length
   as α × H_0 (α = 7 pressure depth scale heights). Corrected formula
   reproduces Earth T_exo ~1,038 K from Earth inputs. ✓

### Physics implemented
| Quantity | Formula | Source |
|---|---|---|
| T_exo | T_eq + (ε F_XUV α H_0) / K_c | Watson et al. 1981; Erkaev et al. 2013 |
| H_0 | k_B T_eq / (m_mean g) | Ideal gas law + hydrostatic equilibrium |
| λ per species | v_e² / v_th² | Chamberlain & Hunten 1987 |
| Γ_d | g / c_p | First Law of Thermodynamics |
| H | R* T_eq / (μ g) | Ideal gas law + hydrostatic equilibrium |
| P_s | M_atm g / (4π R²) | Hydrostatic equilibrium |

### Calibration verified
- T_exo Earth-analog: 1,038 K (target ~1,000–1,200 K) ✓
- λ_H Earth: 7.29 < 15 (H escapes) ✓
- λ_N2 Earth: 202.9 > 15 (N2 retained) ✓
- λ_CO2 Earth: 319 > 15 (CO2 retained) ✓
- Γ_d Earth: 9.77 K/km (target 9.8 K/km) ✓
- Γ_d Jupiter: 2.07 K/km (target ~2.0 K/km) ✓
- H Earth: 7,454 m (T_eq used; lower than 8,500 m surface value,
  expected per Flag 43) ✓

### Seed outputs verified
- Seeds 1, 7, 42: all dwarf regime. T_exo = None, P_s = 0.0,
  atm_class = none, notes correct. No NaN, no crashes. ✓
- Rocky/gas giant/sub-Neptune branches verified via targeted diagnostic
  script with Earth-analog, Jupiter-analog, and sub-Neptune inputs.

### Known behaviour note
T_exo for dwarf bodies returns None. Prior implementation computed T_exo
for dwarfs and returned physically meaningless extreme values (~4,000–95,000 K)
because the conduction model requires a continuum atmosphere. The corrected
implementation correctly short-circuits at the dwarf check.

### Flags opened this session
- Flag 39: K_c (thermospheric thermal conductivity) is gas-dependent,
  lab-measured. O/N2: 0.05 W/m/K; H2/He: 0.30 W/m/K.
  Source: Banks & Kockarts (1973).
- Flag 40: X_vol (mantle volatile fraction) has no cascade origin.
  M_atm for rocky planets blocked. P_s = None for rocky until disk
  chemistry variable added.
- Flag 41: τ_degas (degassing timescale) Earth-calibrated empirical
  coefficient. Not yet implemented — recorded for when outgassing model
  is added.
- Flag 42: Sub-Neptune envelope stripping boundary uses placeholder
  envelope mass fraction (5% of M). Initial envelope mass requires
  protoplanetary disk accretion variable.
- Flag 43: τ_IR greenhouse correction not applied. Scale height and
  surface T use T_eq as approximation. Surface values underestimated
  for planets with significant greenhouse warming.
- Flag 44: Tidal locking atmospheric collapse — confirmed via 3D GCMs,
  no closed-form correction. Deferred to Variable 06.
- Flag 45: Mass sampler draws from galactic demographic PDF. Rocky or
  larger bodies occur with probability ~10⁻¹¹. Engine cannot generate
  habitable worlds in normal operation. Requires design decision.
  Resolved in Scaffold 007.
- Flag 46: α = 7 (pressure depth factor) theoretically universal from
  ln(P_meso/P_XUV) ≈ ln(10³). Empirically confirmed on Earth and Mars
  only.
- Flag 47: Gas giant T_exo is a lower bound only. Giant Planet Energy
  Crisis — internal Joule/auroral heating dominates on stable giants.
  No cascade variable represents this contribution.

### Flags resolved this session
- Flag 10: Water phase state — resolved via Jeans retention logic in
  regime_classifier.py. Phase state follows from T_eq (V05) and
  atmospheric class.
- Flag 27: λ_crit = 15–20 — implemented with Flag 27 documentation.
  Chamberlain & Hunten (1987) threshold applied.
- Flag 28: c_p for rocky atmospheres — implemented with Earth-mix
  default and Flag 28 documentation. Known values applied per regime.
- Flag 30: M_atm deferred — formally stubbed. P_s returns None for
  rocky with Flag 40 documentation.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37
Earth fallbacks: 04, 09, 13, 23, 39, 41
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44
Deferred — design decision required: 45 (resolved Scaffold 007)
Deferred — implementation not yet authorised: 14
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 38, 46
Model lower bound only: 47
Pre-registered duplicate: 26 (= Flag 34)

---

## Scaffold 007 — World Config: User Input Layer and Mass Sampler Conditioning
**Date:** 2026-04-12
**Type:** Implementation

### What was implemented
Flag 45 identified that the mass sampler draws from the full galactic
demographic PDF, making habitable world generation effectively impossible
in normal operation (probability ~10⁻¹¹ for rocky or larger). The
resolution is a user input layer that conditions the mass sampler on a
user-selected world type without modifying any physics.

The world_config module is the sole channel between user selections and
the simulation. main.py passes a config dict into the cascade. Variable
sub-functions never see user inputs directly. This pattern is established
here for all future user-facing parameters (stellar preference, fantasy
distortion level, race requirements, etc.).

### Architectural note — GUI
CLI args are the current interface. A GUI will be built later that
supplies the same parameters to world_config at the backend. The
world_config module does not need to change when the interface changes —
it accepts parameters regardless of their source. main.py is not the
permanent interface; it is the current interface.

### Files created
- `world_config/__init__.py` — empty package marker
- `world_config/world_type.py` — valid world types, WORLD_TYPE_TO_REGIME
  mapping, validate_world_type(). Valid types: rocky, sub_neptune,
  gas_giant, dwarf. brown_dwarf excluded (outside atmospheric domain).
  None = unrestricted galactic draw (default).
- `world_config/world_config.py` — build_config() entry point. Accepts
  world_type, validates it, returns config dict with world_type and
  regime keys. No physics. No imports from variable folders.

### Files modified
- `variable_01_mass/mass_sampler.py` — optional regime parameter added
  to sample_mass(). When supplied, m_min and m_max are clamped to that
  regime's mass boundaries using constants imported from
  regime_classifier.py. _REGIME_BOUNDS dict maps regime strings to
  (lo, hi) boundary pairs. Unrestricted behaviour unchanged when
  regime=None.
- `variable_03_stellar/stellar_mass_sampler.py` — optional stability
  parameter added to sample_stellar_mass(). _STABILITY_BOUNDS dict maps
  stability strings to (lo, hi) M☉ pairs. _build_truncated_segments()
  and _build_cdf_tables() refactored to accept draw_lo and draw_hi as
  parameters. Module-level CDF cache used when stability=None (no
  performance regression on unrestricted draws). 5,000-seed validation
  confirmed all conditioned draws stay within [0.5, 1.5] M☉ for
  stability='stable'.
- `variable_01_mass/variable_01_mass.py` — run() accepts regime=None;
  passes through to sample_mass().
- `variable_03_stellar/variable_03_stellar.py` — run() accepts
  stability=None; passes through to sample_stellar_mass().
- `main.py` — build_config imported; --world-type CLI argument parsed;
  config dict assembled before cascade; regime passed to v01 run;
  stability passed to v03 run via config.get('stability') (always None
  until stellar conditioning is wired to a CLI arg); world config print
  block added.

### Known gap — stellar stability not yet CLI-wired
config.get('stability') is always None at this stage. The conditioning
infrastructure in stellar_mass_sampler is complete and validated, but
build_config does not yet accept or expose a stellar stability input and
no --stellar-type CLI argument exists. This is intentional — stellar
conditioning was not in scope for this scaffold. It is the next
user-input parameter to be added to world_config when required.

### Verified runs
- python main.py 42 — unrestricted galactic draw, all variables execute
  cleanly. ✓
- python main.py 42 --world-type rocky — mass conditioned to rocky
  regime, all variables execute cleanly. ✓
- Invalid --world-type raises ValueError with descriptive message. ✓
- 5,000 seeds with stability='stable' confirmed in [0.5, 1.5] M☉. ✓

### Flags resolved this session
- Flag 45: Mass sampler architectural problem — resolved. Conditioned
  draw implemented via world_config user input layer. Unrestricted
  galactic draw remains the default and is preserved for diagnostic and
  research use.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37
Earth fallbacks: 04, 09, 13, 23, 39, 41
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44
Deferred — implementation not yet authorised: 14
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 38, 46
Model lower bound only: 47
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Stellar stability conditioning needs a --stellar-type CLI argument and
a corresponding key in build_config. This is a small addition to
world_config and main.py — no variable sub-function changes required.
After that, Variable 06: Tectonics is the next simulation variable.
A Gemini research prompt is required before any Variable 06 scope is
defined.

## Scaffold 007a — Argument Parser Fix and Stellar Conditioning Design Decision
**Date:** 2026-04-12
**Type:** Patch + Design Decision

### What was fixed
The manual argv parser in main.py assumed the first argument was always
an integer seed. Passing --world-type as the first argument without a
seed caused a ValueError on int() conversion. Replaced manual argv
handling with argparse.

### Files modified
- `main.py` — replaced manual sys.argv parsing with argparse.
  seed is now an optional positional argument (type=int, nargs='?',
  default=None). --world-type is a named optional argument. When seed
  is omitted, a random seed is generated via random.randint(0, 2**31-1).
  import sys removed as it was no longer needed.

### New valid call signatures
- `python main.py` — random seed, unrestricted galactic draw
- `python main.py 42` — fixed seed, unrestricted galactic draw
- `python main.py --world-type rocky` — random seed, rocky regime
- `python main.py 42 --world-type rocky` — fixed seed, rocky regime

### Verified runs
Three seedless conditioned draws executed with --world-type rocky:
- Seed 42 (prior fixed run): M_star = 0.530 M☉, stable ✓
- Seed 1090036121: M_star = 0.742 M☉, stable ✓
- Seed 1973543832: M_star = 1.852 M☉, unstable_high. T_exo = 7.2×10⁶ K.
  Atmosphere fully stripped. atm_class = exosphere_only. Engine
  reported this correctly and without error.

### Design decision — stellar draw not conditioned on world type
The third run produced an A-type star (1.85 M☉, unstable_high) paired
with a user-selected rocky world. The engine processed this without
complaint and correctly identified the consequence: extreme XUV, total
atmospheric stripping, exosphere only.

The decision was made to leave the stellar draw unconstrained for all
world types. Reasons:

1. MORTALIS worlds are not required to be habitable in the Earth sense.
   The fantasy distortion layer will push parameters beyond realistic
   ranges regardless. An A-type star with a stripped rocky world is a
   physically valid and characterful starting point — white-blue sky,
   extreme radiation, scorched surface. Constraining the stellar draw
   would silently remove this entire class of world from the possibility
   space.

2. The engine already handles the consequence correctly. The simulation
   identifies the star as unstable, computes the XUV flux accurately,
   strips the atmosphere via Jeans and hydrodynamic escape, and reports
   the result honestly. The physical consistency is present regardless
   of stellar type.

3. Stellar type variation produces meaningfully different world
   characters — different sky colours, stellar spectra, XUV
   environments, atmospheric outcomes — all of which are desirable
   inputs for fantasy world generation.

The infrastructure for stellar stability conditioning (stability
parameter in sample_stellar_mass, _STABILITY_BOUNDS, build_config
stability key) remains in the codebase and is fully functional. It
is available if a future use case requires it — for example, a
'habitable' world type preset that constrains both regime and stellar
stability simultaneously. That use case does not exist yet and is not
implemented.

### Flags
No new flags opened. No flags resolved.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37
Earth fallbacks: 04, 09, 13, 23, 39, 41
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44
Deferred — implementation not yet authorised: 14
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 38, 46
Model lower bound only: 47
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 06: Tectonics. Gemini research prompt to be written before
any scope is defined.

## Scaffold 008 — Flag 38: Bond Albedo Two-Pass Architecture
**Date:** 2026-04-12
**Type:** Implementation

### What was implemented
Replaced three fixed Solar System placeholder albedos (rocky 0.30, giant 0.50,
dwarf 0.10) in equilibrium_temperature.py with a physically derived two-pass
Bond albedo framework. Pass 1 runs before Variable 04 and produces a
pre-atmospheric proxy albedo from cascade inputs alone. Pass 2 runs after
Variable 04 and refines the albedo using atmospheric class and stellar spectrum.
T_eq is recomputed after both passes. The calibration target is corrected from
the legacy pairing (A=0.30, T_eq=254.6 K) to the CERES-accurate pairing
(A=0.306, T_eq=254.0 K).

### Files created
- `variable_05_kinematics/bond_albedo.py` — Pass 1 and Pass 2 albedo functions.
  Pass 1: Sudarsky (2000) piecewise condensate classification for gas_giant /
  sub_neptune / brown_dwarf; rock-ice surface mix for rocky / dwarf.
  Pass 2: Del Genio et al. (2019) segmented linear model for rocky planets with
  retained atmosphere; Pass 1 held for all other regimes.

### Files modified
- `variable_05_kinematics/equilibrium_temperature.py` — regime-to-albedo lookup
  removed; function now accepts A_proxy as direct input; Earth calibration note
  updated to Pass 1 values (A=0.15, T_eq^(0)=266.7 K).
- `variable_05_kinematics/variable_05_kinematics.py` — Pass 1 call added after
  stellar flux, before equilibrium temperature. Output dict updated: albedo_proxy,
  T_eq_proxy_K added; T_eq_K is Pass 1 at V05 stage.
- `main.py` — Pass 2 call added after V04, before map generator. albedo_final and
  T_eq_K (Pass 2 final) written back to v05 dict. Print block updated.

### Physics implemented

Pass 1 — Gas giant / sub-Neptune / brown_dwarf (Sudarsky 2000):
  Piecewise A_proxy by zero-albedo blackbody baseline T0 = (⟨F⟩/4σ)^0.25.
  Source: Sudarsky et al. 2000, ApJ 538:885. Multi-body confirmed.

Pass 1 — Rocky / dwarf:
  A_proxy = A_rock × (1-f_ice) + A_ice × f_ice
  A_rock = 0.15 (bare silicate-iron regolith baseline)
  ⚠️ EARTH FALLBACK — Solar System calibrated only.
  A_ice(T_eff) = 0.40 + 0.25 × clamp((T_eff-3000)/4000, 0, 1)
  Source: Shields et al. 2013, Astrobiology 13:715. Multi-body confirmed.

Pass 2 — Rocky with retained atmosphere (Del Genio et al. 2019):
  S_ox ≥ 1.0: A_B = 0.283 + 0.165(S_ox-1) + 0.119(T_eff/5780-1)
  S_ox < 1.0: A_B = 0.283 - 0.211(S_ox-1) + 0.164(T_eff/5780-1)
  Source: Del Genio et al. 2019, ApJ 884:75. 29 ROCKE-3D GCM simulations.
  ⚠️ Flag 38B: empirical GCM calibration. Residual vs Earth: 0.023.

Pass 2 — Gas giant / sub-Neptune: Roman (2023) deferral confirmed;
  requires T_surf not available without greenhouse correction (Flag 43).

### Calibration verified
- Pass 1 Earth: A_proxy=0.15, T_eq^(0)=266.7 K ✓
- Pass 2 Earth: S_ox=1.0, T_eff=5778K → A_B=0.283, T_eq=268.9 K ✓
- Sudarsky piecewise: continuous at all five transition boundaries ✓
- Del Genio sign confirmed after targeted follow-up correcting sign error
  in initial research response.

### Seed 42 verified (python main.py 42 --world-type rocky)
- albedo_proxy: 0.1500 (Pass 1 — silicate-iron, f_ice forced to 0)
- T_eq^(0): 167.47 K
- albedo_final: 0.4086 (Pass 2 — Del Genio, low instellation branch)
- T_eq: 152.95 K
- Pass 2 arithmetic verified: 0.283 - 0.211×(-0.846) + 0.164×(-0.322) = 0.4086 ✓

### Research path
Four Gemini research sessions: initial Flag 38 prompt; Pass 2 follow-up;
sign correction prompt; V06 unblocked after Pass 2 confirmed.

### Flags opened this session
- Flag 48: Sudarsky albedo applied to brown_dwarf regime — internal
  luminosity not represented. Category: inherent model limitation.
- Flag 49: Del Genio (2019) extrapolation at S_ox < 0.3. Category:
  survey-scope limitation.

### Flags resolved this session
- Flag 38: Bond albedo placeholders — resolved. Residual recorded as Flag 38B.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48
Earth fallbacks: 04, 09, 13, 23, 39, 41
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44
Deferred — implementation not yet authorised: 14
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Flag 45 (mass sampler) to be resolved before Variable 06.

---

## Scaffold 008a — Variable 06: Tectonics (with viscosity, Nu–Ra, and solidus corrections)
**Date:** 2026-04-12
**Type:** Implementation + Correction

### What was implemented
Variable 06 maps planetary regime and cascade inputs to internal thermal state,
tectonic regime, tidal locking status, tidal heating, and volcanic melt rate.
Implementation required four Gemini research sessions and two correction cycles
before calibration was confirmed. The correction cycle (Scaffold 008a) resolved
three errors present in the initial implementation.

### Files created
- `variable_06_tectonics/__init__.py` — empty package marker
- `variable_06_tectonics/accretional_energy.py` — E_acc = (3/5)GM²/R and
  dE_core = 0.04 GM²/R
- `variable_06_tectonics/core_geometry.py` — two-layer density contrast model.
  R_core = R×(CMF/(CMF+χ(1-CMF)))^(1/3), χ=2.44 (Earth fallback, Flag 50).
- `variable_06_tectonics/cmb_pressure.py` — hydrostatic integration across
  uniform-density mantle layer. Formula reconstructed from truncated research
  response and validated numerically. 9.5% underestimate inherent to uniform-
  density assumption (Flag 51).
- `variable_06_tectonics/radiogenic_heating.py` — H_rad = M_m × Σ Cᵢhᵢexp(-t/τᵢ)
  for ⁴⁰K, ²³²Th, ²³⁵U, ²³⁸U. hᵢ and τᵢ universal (nuclear physics). Cᵢ
  BSE-calibrated (Flag 55).
- `variable_06_tectonics/mantle_viscosity.py` — Arrhenius viscosity with
  corrected pre-exponential η_0 = η_ref × exp(-E_a/(R_g×T_ref)) = 1.606×10¹¹
  Pa·s; Frank-Kamenetskii parameter θ; Simon-Glatzel solidus T_solidus(P).
- `variable_06_tectonics/rayleigh_number.py` — Ra from Boussinesq
  non-dimensionalisation. α and κ Earth-calibrated silicate constants.
- `variable_06_tectonics/tectonic_regime.py` — stagnant_lid / mobile_lid /
  sluggish_lid classification from Ra vs Ra_c and Ra_sluggish thresholds.
- `variable_06_tectonics/surface_heat_flux.py` — regime-dependent Nu–Ra scaling.
  Stagnant lid: Solomatov (1995), A_p=0.50. Mobile/sluggish: isoviscous scaling,
  A_mob=0.122 (Earth-calibrated, Flag 62).
- `variable_06_tectonics/mantle_temperature.py` — forward Euler ODE integration
  with solidus ceiling. T_m(0)=1700 K canonical cool-start (Flag 57). Q_core=0
  (Flag 53).
- `variable_06_tectonics/tidal_locking.py` — t_lock from Peale (1977). Q=100,
  k₂=0.3, ω₀ = 2π/(10h) — all Earth/Solar System calibrated.
- `variable_06_tectonics/tidal_heating.py` — P_tidal from orbital eccentricity
  dissipation. Watson et al. (1981).
- `variable_06_tectonics/volcanic_melt_rate.py` — R_melt from Kite et al. (2009)
  decompression melting parameterisation. Currently returns 0 due to dimensional
  inconsistency in melt fraction denominator (Flag 66). Stub treatment in place.
- `variable_06_tectonics/variable_06_tectonics.py` — entry point; regime routing;
  no physics directly.

### Files modified
- `constants.py` — new root-level file; G and R_GAS as Category A constants.
- `main.py` — V06 import, call, and print block added. V06 runs after V04 and
  before map generator.

### Errors identified and corrected during implementation

**Error 1 — Arrhenius pre-exponential (Scaffold 008 → 008a):**
Initial implementation placed η_ref = 10²¹ Pa·s directly as the Arrhenius
pre-exponential. This is incorrect — η_ref is the observed viscosity at T_ref,
not the pre-exponential. Correct value: η_0 = η_ref × exp(-E_a/(R_g×T_ref))
= 1.606×10¹¹ Pa·s. Error produced η(1,650 K) ≈ 3×10³⁰ Pa·s (nine orders of
magnitude too high), Ra = 310 (three orders too low), and T_m = 2,889 K (above
solidus). All corrected in 008a.

**Error 2 — Nu–Ra formula gives Nu < 1 at Earth conditions (Scaffold 008 → 008a):**
Stagnant lid formula Nu = A_p × Ra^(1/3) × θ^(-4/3) gave Nu = 0.36 for Earth
inputs — physically impossible. Root cause: Earth is a mobile lid planet; the
stagnant lid formula cannot calibrate to Earth. Correct scaling for mobile lid
is Nu = A_mob × Ra^(1/3) with A_mob = 0.122 (Earth-calibrated). Three-regime
implementation (stagnant / mobile / sluggish) implemented in 008a.

**Error 3 — P_cmb formula truncated in research response:**
Research response for P_cmb was cut off mid-formula. Formula reconstructed from
derivation steps provided in the same response, validated numerically against
Earth (123 GPa, 9.5% below 136 GPa due to uniform-density assumption — confirmed).

### Calibration correction — Q_core = 0 targets

Earth calibration targets were initially set for a full model including Q_core.
The Q_core = 0 ODE produces different but physically correct values. Earth's
47 TW surface heat flow includes ~15 TW core heat flux and ~12 TW secular mantle
cooling that the Q_core = 0 model does not capture. The correct Q_core = 0
calibration expectations — confirmed by numerical integration — are:

| Quantity | Q_core = 0 result | Full-model Earth | Discrepancy source |
|---|---|---|---|
| T_m(4.5 Gyr) | ~1,540 K | ~1,650 K | Q_core raises equilibrium T_m |
| q_s total | ~24.85 TW | ~47 TW | Q_core + secular excluded |
| Ra | ~1.67×10⁷ | ~10⁸ | Lower T_m → higher η → lower Ra |
| Regime | mobile_lid | mobile_lid | ✓ |

All Q_core = 0 outputs are physically self-consistent. Flag 53 updated to
record quantified consequences.

### Physics implemented

| Quantity | Formula | Source |
|---|---|---|
| E_acc | (3/5)GM²/R | Gravitational binding energy |
| dE_core | 0.04 GM²/R | Analytic differentiation estimate |
| R_core | R×(CMF/(CMF+χ(1-CMF)))^(1/3) | Two-layer mass-volume conservation |
| P_cmb | Hydrostatic integral, two uniform layers | Hydrostatic equilibrium |
| H_rad | M_m × Σ Cᵢhᵢexp(-t/τᵢ) | Nuclear physics + BSE concentrations |
| η | η_0 exp(E_a/(R_g T_m)) | Arrhenius; η_0 = 1.606×10¹¹ Pa·s |
| θ | E_a ΔT / (R_g T_m²) | Frank-Kamenetskii linearisation |
| T_solidus | 1400×(P_GPa/24+1)^0.57 | Simon-Glatzel fit (Fiquet 2010) |
| Ra | ρ g α ΔT D³ / (κ η) | Boussinesq non-dimensionalisation |
| Nu (stagnant) | 0.50×(Ra/Ra_c)^(1/3)×θ^(-4/3) | Solomatov (1995) |
| Nu (mobile) | 0.122×Ra^(1/3) | Isoviscous boundary layer theory |
| t_lock | ω₀ a⁶ I Q / (3G M★² k₂ R⁵) | Peale (1977); Gladman (1996) |
| P_tidal | (21/2)(k₂/Q) G M★² R⁵ n e² / a⁶ | Watson et al. (1981) |
| R_melt | Stub — returns 0. Flag 66. | Kite et al. (2009) — blocked |

### Calibration verified (Earth diagnostic, python diagnostic_v06_earth.py)
- R_core: 3,493 km (target ~3,480 km, +0.4%) ✓
- P_cmb: 122.9 GPa (target ~123 GPa) ✓
- H_rad: 19.82 TW (target 20–24 TW) ✓
- T_m(4.5 Gyr): 1,540 K (Q_core=0 target ~1,500–1,600 K) ✓
- Ra: 1.669×10⁷ (target 1×10⁷–1×10⁸) ✓
- q_s total: 24.85 TW (Q_core=0 target 20–27 TW) ✓
- tectonic_regime: mobile_lid ✓
- solidus_reached: False ✓
- t_lock: 201.8 Gyr (target >50 Gyr) ✓

### Seed 42 verified (python main.py 42 --world-type rocky)
- T_m: 1,349 K < solidus 2,398.6 K ✓
- Ra: 8.699×10⁴ > Ra_c = 1,000, mobile_lid ✓
- solidus_reached: False ✓
- H_rad: 2.38 TW (physically expected at 11.6 Gyr for 0.279 M_Earth) ✓
- q_s total: 2.84 TW (physically expected — small planet, low radiogenics) ✓
- t_lock: 13.49 Gyr, is_locked: False (age 11.63 Gyr < 13.49 Gyr) ✓

### Flags opened this session
- Flag 50: χ = 2.44 core-mantle density contrast. Earth-calibrated.
- Flag 51: P_cmb uniform-density assumption. 9.5% underestimate. Inherent.
- Flag 52: C_p = 1200 J/(kg·K). Earth silicate calibration.
- Flag 53 (updated): Q_core = 0. Effect quantified: T_m ~110 K lower,
  q_s ~22 TW lower than observed Earth values. Physically self-consistent
  at Q_core = 0. Deferred — upstream dependency.
- Flag 54: E_a = 300,000 J/mol dry peridotite. Earth-calibrated. Assumes
  dry rheology.
- Flag 55: Cᵢ BSE-calibrated isotope concentrations. Not universal.
- Flag 56: ρ_crust, Z_crust, P_f, P_o stagnant lid melt constants.
  Earth/Venus analogue calibration.
- Flag 57: T_m(0) = 1,700 K canonical cool-start. Not derivable from
  cascade without accretion timescale.
- Flag 58: T_solidus = 1,500 K sub-Neptune magma ocean gate. Earth
  silicate calibration.
- Flag 59: Constant T_m(0) across rocky mass range. Inherent to model.
- Flag 60: ODE self-regulation fails below Ra_c throughout thermal
  history. Inherent to model for low-mass rocky planets.
- Flag 61: No solidus ceiling (superseded — ceiling implemented in 008a).
- Flag 62: A_mob = 0.122 mobile lid prefactor. Earth-calibrated.
- Flag 63: A_p = 0.50 stagnant lid prefactor. Numerical simulation value.
  No independent planetary calibration available.
- Flag 64: Sluggish lid uses mobile lid formula approximation. Inherent.
- Flag 65: T_solidus Simon-Glatzel fit. Earth peridotite DAC calibration.
- Flag 66: R_melt = 0. Dimensional inconsistency in Kite et al. melt
  fraction denominator. Research prompt required. Category: incomplete
  research — formula transcription error.

### Flags resolved this session
- Flag 45: Mass sampler architectural problem — resolved (Scaffold 007).

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60, 63, 64
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57, 58, 62, 65
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44, 53
Deferred — implementation not yet authorised: 14
Incomplete research — formula error: 66
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Flag 66: R_melt formula dimensional error. Gemini research prompt to be
written before any R_melt correction is implemented.
Variable 07: Hydrology is the next simulation variable after Flag 66 is
resolved or deferred. Gemini research prompt required before any V07
scope is defined.

---
## Scaffold 009 — Flag 66: Volcanic Melt Rate Formula Correction
**Date:** 2026-04-13
**Type:** Correction

### What was corrected
Two formula errors in variable_06_tectonics/volcanic_melt_rate.py,
both confirmed by research (Kite et al. 2009 source analysis) and
validated numerically.

**Error 1 — u denominator dimensionally invalid:**
Prior implementation: denom_T = T_m - P_c / (rho_mean × g)
P_c / (rho_mean × g) has units Pa / (kg/m³ × m/s²) = metres.
Subtracting metres from Kelvin is dimensionally invalid. The function
collapsed to R_melt = 0 via the denom_T <= 0 guard.

Correct: denominator is a thermal boundary temperature T_c,
regime-dependent per Kite et al. (2009) Eq. 24:
  Mobile lid:   T_c = T_s → ratio = (T_m - T_s)/(T_m - T_c) = 1.0 exactly.
  Stagnant lid: T_c = T_m - 2.23 × (T_m² / A_0)
                denominator = 2.23 × T_m² / A_0
                where A_0 = E_a / R_g = 300,000 / 8.314 = 36,083 K
                Source: Grasset and Parmentier (1998).

**Error 2 — /M_planet division produced wrong units:**
Prior implementation divided by M (planetary mass, kg), yielding 1/s.
Kite et al. (2009) Eq. 25 is a normalized rate in yr⁻¹. The /M term
is the Kite normalization. To obtain kg/s directly, the un-normalized
form must be used:
  R_melt = 4πR² × u × rho_mantle × melt_fraction
Dimensional check: m² × m/s × kg/m³ × [–] = kg/s ✓
Division by M discarded entirely.

### Files modified
- variable_06_tectonics/volcanic_melt_rate.py — full rewrite.
  Function signature: (Nu, T_m, T_eq, R, g, D, rho_mantle,
  tectonic_regime). Parameters P_c, M, rho_mean removed (fed the
  invalid prior denominator). tectonic_regime added for T_c branch
  selection.
- variable_06_tectonics/variable_06_tectonics.py — call site updated
  to match new signature.

### Physics implemented (corrected)

| Quantity | Formula | Source |
|---|---|---|
| u (mobile) | 2(Nu-1) × κ/D × 1.0 | Kite et al. (2009) Eq. 24 |
| u (stagnant) | 2(Nu-1) × κ/D × (T_m-T_eq) / (2.23 T_m²/A_0) | Kite (2009) + Grasset & Parmentier (1998) |
| R_melt | 4πR² × u × rho_mantle × (rho_crust × Z_crust × g / ΔP) | Kite et al. (2009) Eq. 25, un-normalized |

### Numerical validation — Earth (mobile lid, Kite constants)
Nu=31.2, T_m=1540 K, k=4.18, c=914, rho=3400, D=2.891e6 m,
R=6.371e6 m, Z_crust=7000 m, P_f=0, P_o=3e9 Pa:
→ u = 2.81e-11 m/s, melt_fraction = 0.0655, R_melt = 3.19e6 kg/s
Target: ~3.2e6 kg/s (Kite et al. 2009). ✓

### Calibration note — code constants vs Kite
Code uses k=3.5 (Flag 67) and C_p=1200 (Flag 52) vs Kite's k=4.18,
c=914. With code constants, mobile-lid Earth gives R_melt ≈ 2.03e6
kg/s, ~36% below Kite target. Discrepancy is entirely from differing
Earth-fallback constants, not from formula error.

### Seed 42 verified (python main.py 42 --world-type rocky)
- R_melt: 1.275e6 kg/s ✓
- Arithmetic verified independently: Nu=5.40, rho_mantle=3483 kg/m³,
  D=2.0414e6 m, u=3.610e-12 m/s, melt_fraction=0.3945 →
  R_melt = 1.273e6 kg/s. Terminal/manual agree to 0.2%. ✓

### Physical observation — melt_fraction elevated for mobile lid
melt_fraction = 0.395 for Seed 42 is physically high. Cause: Z_crust
= 50,000 m (stagnant lid analogue, Flag 56) applied to a mobile_lid
planet where oceanic crustal thickness should be ~7,000 m. This
inflates R_melt by ~7× for mobile lid planets. Pre-existing Flag 56
issue — not introduced by this fix.

### Stagnant lid calibration target
~1.1e6 kg/s for stagnant lid Earth at 4.5 Gyr. Research notes this
is an upper-bound total crustal production estimate (including
intrusive magmatism). Strict one-order-of-magnitude suppression
relative to mobile lid would give ~3.2e5 kg/s. The 1.1e6 target
remains geophysically plausible within acknowledged uncertainty.

### Flags opened this session
- Flag 67: k = 3.5 W/(m·K) thermal conductivity. Kite et al. use
  4.18. Our value produces R_melt ~36% below Kite calibration target.
  Earth silicate fallback. Category: Earth fallback.
- Flag 68: Kite (2009) parameterization invalid above ~3 M_Earth.
  Dorn et al. (2018), Noack et al. (2017): pressure suppression
  nonlinearly truncates melting column and raises lower-mantle
  viscosity. One-dimensional Kite model overestimates melt on massive
  super-Earths. Flag for review if M_planet > 3 M_Earth and
  R_melt_kgs used as output. Category: model applicability limit.
- Flag 69: A_0 = E_a/R_g = 36,083 K activation temperature. Inherits
  Flag 54 (E_a Earth-calibrated dry peridotite). Category: Earth
  fallback (derived).

### Flags resolved this session
- Flag 66: R_melt = 0 dimensional error — resolved.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60, 63, 64
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57, 58,
                 62, 65, 67, 69
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44, 53
Deferred — implementation not yet authorised: 14
Model applicability limit: 68
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 07: Hydrology. Gemini research prompt required before any
scope is defined.

---
## Scaffold 010 — Flag 14: Eker et al. (2020) Bolometric Correction
**Date:** 2026-04-13
**Type:** Correction / Implementation

### What was resolved
Flag 14 was opened during the V03 research session when the Eker et al.
(2020) bolometric correction polynomial failed numerical validation by
1.4 magnitudes and was pulled before implementation. This scaffold
resolves that flag through a targeted research cycle that identified
two distinct failure modes — neither of which was an error in the
polynomial itself.

### Failure mode 1 — Catastrophic cancellation (original 1.4 mag error)
At solar temperatures the polynomial's positive and negative terms
inflate to opposing values of approximately ±13,000 before cancelling
to a residual near zero. Single-precision floating point (7 significant
digits) cannot preserve this residual and produces garbage output. The
1.4 mag error was entirely an implementation failure, not a physics
failure. The polynomial was always correct.

### Failure mode 2 — Wrong calibration target (convention mismatch)
The engine's original calibration target of BC☉ = −0.07 ± 0.05 mag at
5778 K belongs to the pre-IAU 2015 arbitrary zero-point convention,
under which bolometric corrections were artificially forced negative by
shifting the zero-point. Eker et al. (2020) was built explicitly to
conform to the IAU 2015 Resolution B2 absolute bolometric magnitude
scale (zero-point constant = 71.197425). Under IAU 2015 the solar BC
is not −0.07. The discrepancy was entirely attributable to comparing
incompatible standards.

### Correct IAU 2015 calibration derived
M_Bol,☉ = −2.5 × log₁₀(3.828×10²⁶) + 71.197425 = 4.7400 mag
BC☉ = M_Bol,☉ − M_V,☉ = 4.7400 − 4.756 = −0.0160 mag
Source: IAU 2015 Resolutions B2 and B3. M_V,☉ = 4.756 from Eker
et al. (2020) — empirically adopted (Flag 70).

### Zero-point shift confirmed numerically
Pre-IAU shift: −0.016 − (−0.07) = +0.054 mag
Temperature input shift (5778 K vs 5772 K): +0.004 − (−0.016) = +0.020
Total: +0.074 mag. Check: −0.07 + 0.074 = +0.004 mag ✓
The discrepancy is fully and exactly explained. No polynomial error.

### Calibration verified
Polynomial at T_eff = 5772 K (Horner, double precision): −0.01619 mag
IAU 2015 target: −0.0160 mag
Deviation: 0.000 mag ✓

### Implementation
- Double precision mandatory throughout — catastrophic cancellation
  occurs with single precision at solar temperatures
- Evaluation variable is log₁₀(T_eff) — natural log produces
  catastrophic divergence (x ≈ 8.66 at solar temperature)
- Horner's method mandatory — prevents cancellation by accumulating
  from the inside out

### Files created
- `variable_03_stellar/bolometric_correction.py` — Eker et al. (2020)
  fourth-degree polynomial. Coefficients from Table 5 to full five
  decimal precision. Domain guard [3100, 36000] K with ValueError
  outside bounds. Horner evaluation. Full documentation block.

### Files modified
- `variable_03_stellar/variable_03_stellar.py` — BC_V computed after
  T_eff; ValueError caught for domain exceedance; BC_V and BC_V_note
  added to output dict.
- `main.py` — BC_V printed in V03 block; "domain exceeded" if None.

### Verified run (python main.py 1 --world-type rocky)
- T_eff = 3398.96 K → BC_V = −1.8507 mag ✓
  (Large negative correction expected for late M-dwarf;
  flux peaks in near-IR, almost nothing in visual band)
- All downstream variables execute cleanly. No NaN, no crashes. ✓

### Flags opened this session
- Flag 70: M_V,☉ = 4.756 mag — empirically adopted solar visual
  magnitude used to anchor the IAU 2015 calibration target.
  Not derivable from Category A constants.
  Category: Earth/Solar System fallback.

### Flags resolved this session
- Flag 14: Eker et al. (2020) BC polynomial — resolved.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60, 63, 64
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57, 58,
                 62, 65, 67, 69, 70
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44, 53
Model applicability limit: 68
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 08+ as authorised.

---

## Scaffold 009 — Variable 07: Hydrology
**Date:** 2026-04-13
**Type:** Implementation

### Rule 9 correction note
The initial Scaffold 009 entry was written by Cursor as part of the same
implement pass, before terminal output was verified and before a changelog
prompt was issued. This violates Rule 9. This entry replaces that premature
entry. No code was changed as part of this correction.

### What was implemented
Variable 07 maps cascade inputs from V01–V06 to a set of hydrological
outputs: volatile phase states, subsurface liquid horizon depth, crustal
porosity profile, energy-limited precipitation ceiling, Budyko partitioning
ratio (blocked pending M_vol), fluvial and glacial gravity scaling
multipliers, and latent heat transport ceiling.

### Files created
- `variable_07_hydrology/__init__.py` — exports run_variable_07
- `variable_07_hydrology/volatile_phase_state.py` — SPECIES_DATA dict
  (H2O, CO2, SO2, CH4, NH3, H2); Antoine vapor pressure evaluation;
  Clausius-Clapeyron fallback below Antoine lower bound; phase state
  logic returning solid/liquid/gas/supercritical_fluid/gas_permanent/
  liquid_possible; evaluate_all_species assembles per-species dict
- `variable_07_hydrology/subsurface_liquid_horizon.py` — Fourier
  conduction T(z) = T_s + (q_s/k)*z; lithostatic P(z) = P_s + rho*g*z;
  Ice Ih Clapeyron melt curve T_melt(P); analytic linear solve for z*
- `variable_07_hydrology/crustal_porosity.py` — Athy's Law
  phi(z) = phi_0 * exp(-c*z), c = rho_b*g/K_comp; e-folding depth z_e
- `variable_07_hydrology/precipitation_energy_limit.py` — net surface
  radiation R_n = F_mean*(1-albedo); PET = R_n/lambda; lambda from
  dH_vap/M_mol
- `variable_07_hydrology/budyko_partitioning.py` — MCY equation
  ET/P = DI/(1+DI^n)^(1/n); returns None when P unavailable (M_vol
  blocked, Flag 90)
- `variable_07_hydrology/fluvial_gravity_scaling.py` — U_scaling =
  sqrt(g/g_Earth); Darcy-Weisbach derivation
- `variable_07_hydrology/glacial_gravity_scaling.py` — U_ice_scaling =
  (g/g_Earth)^3; Glen's Flow Law SIA derivation
- `variable_07_hydrology/latent_heat_transport.py` — Q_latent_max =
  lambda * PET * 4*pi*R^2
- `variable_07_hydrology/variable_07_hydrology.py` — regime routing;
  gas_giant/brown_dwarf return null; dwarf runs phase state only;
  rocky/sub_neptune run full V07 treatment

### Files modified
- `main.py` — run_variable_07 called after run_variable_06; v07 added
  to active_variables; V07 output block printed with None-safe formatting

### Physics implemented

**Antoine equation — volatile phase state**
log10(P_sat / bar) = A - B / (T + C)
Source: Giauque & Egan (1937) CO2; Stull (1947) SO2; standard NIST for
H2O, CH4, NH3; van Itterbeek et al. via Yaws/NIST for H2.
All coefficients are intrinsic molecular properties.

**Clausius-Clapeyron fallback (below Antoine lower bound)**
ln(P / P_ref) = -(dH_sub / R) * (1/T - 1/T_ref)
Source: Clausius-Clapeyron integration, constant dH_sub approximation.
R = 8.314 J/mol/K (Category A). dH_sub values from NIST (flagged).

**Fourier conduction + lithostatic pressure (subsurface horizon)**
T(z) = T_s + (q_s / k_crust) * z
P(z) = P_s + rho_crust * g * z
T_melt(P) = 273.16 * (1 - (P - 611.7) / 1.35e8)   [Ice Ih, linearised]
z* solved analytically by equating T(z*) = T_melt(P(z*))
Sources: Fourier (1822); Wagner et al. (1994) Ice Ih melting curve.

**Athy's Law (crustal porosity)**
phi(z) = phi_0 * exp(-c * z),  c = rho_b * g / K_comp
Source: Athy (1930). Gravitational scaling c ∝ g is planet-general.

**Precipitation energy limit**
R_n = F_mean * (1 - albedo_final)
PET = R_n / lambda,  lambda = dH_vap / M_mol
Source: energy balance, Clausius-Clapeyron. Planet-general.

**Budyko MCY partitioning**
ET/P = DI / (1 + DI^n)^(1/n),  DI = PET / P
Source: Mezentsev (1955), Choudhury (1999), Yang et al. (2008).

**Fluvial gravity scaling**
U_scaling = sqrt(g / g_Earth)
Source: Darcy-Weisbach equation, Navier-Stokes derived. Planet-general.
Validated: Earth, Mars, Titan.

**Glacial gravity scaling**
U_ice_scaling = (g / g_Earth)^3
Source: Glen (1955), Paterson (1994) SIA. Stress exponent n=3 universal
for dislocation creep in crystalline solids.

**Latent heat transport ceiling**
Q_latent_max = lambda * PET * 4*pi*R^2
Source: energy balance. Planet-general upper bound.

### Verified runs

**python main.py 1 --world-type rocky**
- Subsurface liquid horizon: 1304.45 m
  Verified: z* = (273.161 - 213.14) / (0.02082 + 0.02521) = 1303.8 m ✓
- Crustal compaction depth: 2786.5 m
  Verified: 31e6 / (2500 × 4.4501) = 2786.5 m ✓
- Net surface radiation: 468.03 W/m²
  Verified: 550.62 × (1 - 0.15) = 468.03 W/m² ✓
- PET ceiling: 6,547,945 mm/yr
  Verified: 468.03 / 2,255,827 × 1000 × 3.156e7 = 6,547,800 mm/yr ✓
- Fluvial scaling: 0.6735 × Earth
  Verified: sqrt(4.4501 / 9.81) = 0.6735 ✓
- Glacial scaling: 0.0933 × Earth
  Verified: (4.4501 / 9.81)^3 = 0.0933 ✓
- Latent heat ceiling: 9.480e16 W
  Verified: 468.03 × 4π × (4.0149e6)^2 / lambda = 9.475e16 W ✓
- Phase states: deferred (speciation None — see known behaviour)
- Budyko ET/P: None (blocked — correct behaviour)
- No NaN, no crashes ✓

**python main.py 42 --world-type rocky**
- Subsurface liquid horizon: 3409.05 m
  Verified: z* = (273.161 - 152.95) / (0.004431 + 0.030830) = 3409.2 m ✓
- Crustal compaction depth: 2278.8 m
  Verified: 31e6 / (2500 × 5.4414) = 2278.8 m ✓
- Net surface radiation: 124.12 W/m²
  Verified: 209.88 × (1 - 0.4086) = 124.12 W/m² ✓
- PET ceiling: 1,736,484 mm/yr
  Verified: 124.12 / 2,255,827 × 1000 × 3.156e7 = 1,736,747 mm/yr ✓
- Fluvial scaling: 0.7448 × Earth
  Verified: sqrt(5.4414 / 9.81) = 0.7448 ✓
- Glacial scaling: 0.1707 × Earth
  Verified: (5.4414 / 9.81)^3 = 0.1707 ✓
- Latent heat ceiling: 3.185e16 W
  Verified: 124.12 × 4π × (4.5191e6)^2 / lambda = 3.183e16 W ✓
- Phase states: deferred (speciation None — see known behaviour)
- Budyko ET/P: None (blocked — correct behaviour)
- No NaN, no crashes ✓

### Known behaviour — phase state evaluation deferred on all seeds
V06 speciation returns None for all seeds because fO2 and volatile
inventory are absent from the cascade (existing blocked output).
V07 correctly handles this with a deferred note rather than crashing.
Consequence: the primary V07 output — which volatile condenses at the
surface — is deferred for all seeds until a mantle chemistry / volatile
inventory variable supplies the speciation dict. This is the most
consequential blocked path in the current cascade and will remain so
until that upstream variable is implemented.

### Known behaviour — PET on atmosphere-stripped worlds
Seed 1 reports PET = 6.5 million mm/yr. This is arithmetically correct
— it is the energy-limited ceiling on evaporation given 468 W/m² net
surface flux. However, seed 1 has atm_class = exosphere_only and no
surface liquid. On such worlds PET is physically vacuous: there is
nothing to evaporate. The correct gate — skip PET output when phase
states confirm no surface liquid — cannot be applied until speciation
is resolved and phase state evaluation runs. Recorded as Flag 93.
Not patched. The value is honest physics; the regime routing is
incomplete pending the upstream volatile inventory variable.

### Obliquity now in cascade — ice-line latitude unblocked upstream
The ice-line latitude was deferred in the V07 research session on the
grounds that obliquity was absent from the cascade. V05 output for both
benchmark seeds confirms obliquity is now a cascade output (seed 1:
75.77°; seed 42: 39.06°). The upstream dependency is therefore
satisfied. Ice-line latitude remains unimplemented — the EBM formula
has not been researched or numerically validated for this project.
A targeted Gemini research prompt is the remaining gate before
implementation. This is not authorised in the current scaffold.
Flag 92 (ice-line latitude blocked — obliquity missing) status updated:
upstream dependency resolved; research prompt outstanding.

### Flags opened this session
Flag 71: H2O Antoine coefficients — Earth-measured molecular constant,
  intrinsic molecular physics, universal.
Flag 72: CO2 Antoine coefficients (sublimation) — Giauque & Egan (1937)
  via NIST. Earth-measured, universal molecular physics.
Flag 73: SO2 Antoine coefficients — Stull (1947) via NIST. 4.7%
  discontinuity at 263 K handoff documented; not patched.
  SO2 triple point pressure: NIST value 1670 Pa used; Antoine-derived
  value gives 1440 Pa (14% deviation at boundary — known Antoine limit).
Flag 74: CH4, NH3 Antoine coefficients — standard NIST.
  Earth-measured molecular constants, universal.
Flag 75: dH_sub H2O 51,000 J/mol — NIST. Earth-measured molecular constant.
Flag 76: dH_sub CO2 26,100 J/mol — NIST. Earth-measured molecular constant.
Flag 77: dH_sub SO2 24,900 J/mol — NIST. Not returned by research;
  sourced directly from NIST thermochemical tables.
Flag 78: dH_vap H2O 40,650 J/mol at 373 K — NIST.
  Earth-measured molecular constant.
Flag 79: Ice Ih Clapeyron slope 1.35e8 Pa — Wagner et al. (1994).
  Intrinsic to H2O crystal structure; Earth-measured, universal.
Flag 80: k_crust = 2.5 W/m/K — terrestrial silicate rock. Earth fallback.
  Universal applicability not confirmed.
Flag 81: rho_crust = 2800 kg/m³ — terrestrial continental crust.
  Earth fallback.
Flag 82: phi_0 = 0.4 — Athy's Law initial porosity, Earth shale/
  sedimentary baseline. Earth fallback.
Flag 83: K_comp = 31 MPa — Athy's Law compaction modulus, Earth shale/
  sedimentary baseline. Earth fallback.
Flag 84: rho_b = 2500 kg/m³ — Athy's Law bulk crustal density.
  Earth fallback.
Flag 85: N_BUDYKO = 2.0 — MCY shape parameter. Earth-fitted; varies
  1.5–3.0 with biology. Abiotic bare-rock default used. Earth fallback.
Flag 86: f_Darcy = 0.05 — Darcy-Weisbach friction factor. Validated
  rocky channels: Earth, Mars, Titan. Earth fallback with multi-body
  partial confirmation.
Flag 87: A_GLEN = 2.4e-15 kPa⁻³ s⁻¹ — Glen's flow parameter, Earth
  H2O ice (Paterson 1994). Different values required for CO2/CH4 ice.
  Earth fallback.
Flag 88: CO2 liquid-vapor window (216.58–304.18 K, P_s > 5.185 bar):
  Span-Wagner EOS deferred; engine returns liquid_possible.
  Model limitation.
Flag 89: CO2 Antoine lower bound 154.26 K; Clausius-Clapeyron fallback
  below this. ~20% overshoot confirmed at 149 K extrapolation.
  Model limitation.
Flag 90: M_vol total volatile inventory blocked — primordial accretion
  fraction / snow-line variable missing. Budyko absolute rates deferred.
  Deferred — upstream dependency.
Flag 91: Ocean volume and depth blocked — topographic variance sigma_h
  missing. Deferred — upstream dependency.
Flag 92: Ice-line latitude — obliquity now confirmed in cascade (V05).
  Upstream dependency resolved. Research prompt outstanding.
  Status updated from deferred-upstream to research-outstanding.
Flag 93: PET output on atmosphere-stripped worlds is physically vacuous
  when phase state evaluation is deferred. Correct gate cannot be applied
  until speciation is resolved. Model limitation — not patched.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60, 63, 64
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57, 58,
                 62, 65, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                 79, 80, 81, 82, 83, 84, 85, 86, 87
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44,
                                  53, 90, 91
Research outstanding: 92
Model applicability limit: 68
Model limitation: 88, 89, 93
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 08: Sediment Transport — partial prior work exists (Flags 1–8
documented; Weertman sliding law and gravity multiplier correction were
the focus of the most recent V08 session). Review prior research before
determining whether a new Gemini prompt is required or whether
implementation can proceed from existing validated formulas.

---
## Scaffold 010b — Flag 92: Ice-Line Latitude (Variable 07)
**Date:** 2026-04-13
**Type:** Implementation + Correction

### What was implemented
A new sub-function computing the annual-mean ice-line latitude via a
one-dimensional analytical Energy Balance Model with Legendre polynomial
decomposition. Resolves Flag 92.

### Files created
- `variable_07_hydrology/ice_line_latitude.py` — analytical P2 EBM
  ice-line solver. Inputs: F_mean_W_m2, T_eq_K, obliquity_deg,
  albedo_final, atm_class, phase_states. Outputs: ice_line_lat_deg,
  ice_line_state, T0_C, T2_C, T_f_K, s2, ice_line_notes.

### Files modified
- `variable_07_hydrology/variable_07_hydrology.py` — import added;
  compute_ice_line_latitude called in rocky/sub_neptune path after
  latent heat transport; six ice_line keys added to rocky/sub_neptune
  return dict, _null_hydrology dict, and dwarf return dict.
- `main.py` — V07 print block extended with ice_line_state,
  ice_line_lat_deg, and truncated ice_line_notes.

### Physics implemented
**Budyko-Sellers-North analytical EBM (North et al. 1981)**

Insolation distribution expanded in Legendre polynomials:
  S(x, β) = Q [1 + s2(β) P2(x)]
  s2(β) = -(5/8)(3cos²β - 1)/2
  Q = F_mean / 4

OLR linearisation (Budyko 1969):
  OLR(x) = A + B·T(x)

Meridional diffusion (Sellers 1969):
  ∇·F_heat = -D d/dx[(1-x²) dT/dx]

Analytical P2 solution:
  T(x) = T0 + T2·P2(x)
  T0 = (σ T_eq⁴ - A) / B
  T2 = Q(1-α)s2 / (B + 6D)
  P2(x_ice) = (T_f - T0) / T2
  x_ice = sqrt((2·P2 + 1) / 3)
  φ_ice = arcsin(x_ice)

Ice-line states returned: polar_caps | tropical_belt | ice_free |
full_glaciation | no_condensable.

High-obliquity inversion (β > 54.74°) handled correctly: s2 > 0,
T2 > 0, poles warmer than equator, formula returns tropical ice belt
boundary rather than polar cap boundary.

### Calibration verified numerically (pre-implementation, by Claude)
- Earth case (β=23.44°, T_eq=255 K, F=1361, α=0.30):
  s2=-0.477, T0=14.85°C, T2=-20.28°C, φ_ice=65.0° (target ~70°) ✓
- High obliquity (β=90°): p2_ice=-1.117 → ice_free ✓
- Zero obliquity (β=0°): φ_ice=57.1° ✓

### Runtime correction — domain check sign error
First run against seed 42 returned ice_line_state=ice_free when
full_glaciation was correct (T_eq=152.95 K, T0=-89.5°C, T_f=0.01°C).

Root cause: the out-of-domain p2_ice guards were sign-independent.
The physical meaning of p2_ice < -0.5 and p2_ice > 1.0 inverts with
the sign of T2 (equivalently, the sign of s2):

  s2 < 0 (β < 54.74°): equator warmest
    p2_ice < -0.5 → full_glaciation
    p2_ice > 1.0  → ice_free

  s2 > 0 (β > 54.74°): poles warmest
    p2_ice < -0.5 → ice_free
    p2_ice > 1.0  → full_glaciation

Corrected in ice_line_latitude.py before changelog was written per
Rule 9. Re-run confirmed correct output on both benchmark seeds.

### Verified runs
- python main.py 1 --world-type rocky:
  atm_class=exosphere_only → ice_line_state=no_condensable,
  ice_line_lat_deg=None. Correct — no condensable volatile on a
  stripped atmosphere world. ✓
- python main.py 42 --world-type rocky:
  T_eq=152.95 K, obliquity=39.06°, atm_class=secondary_possible
  → ice_line_state=full_glaciation, ice_line_lat_deg=None.
  T0=-89.5°C, T_f=0.01°C — entire surface below freezing. ✓

### Flags opened this session
Flag 94: A = 210 W/m² — OLR linear intercept. Budyko (1969).
  Earth-calibrated empirical coefficient. Fails for dense CO2 or
  H2/He atmospheres. Universal applicability not confirmed.
  Category: Earth fallback.
Flag 95: B = 2.0 W/m²/K — OLR temperature sensitivity. Earth-
  calibrated. Encodes water-vapour feedback; wrong for non-H2O
  atmospheres. Category: Earth fallback.
Flag 96: D = 0.6 W/m²/K — meridional thermal diffusion coefficient.
  Earth-calibrated. Must scale with rotation rate (∝ Ω⁻²) and
  atmospheric column mass. Rotation rate absent from cascade entirely.
  Two resolution gates: (1) rotation rate research + V05 extension;
  (2) D scaling law derivation and numerical validation.
  Category: Earth fallback + deferred upstream dependency.
Flag 97: β = 54.74° singularity — s2 = 0, T2 = 0, formula undefined.
  Handled via explicit branch: if T0 > T_f → ice_free; else →
  full_glaciation. Category: model limitation.
Flag 98: P2 Legendre truncation — 3–7% error on φ_ice as function
  of obliquity. Not patchable without spatial grid.
  Category: model limitation.
Flag 99: Ice-albedo feedback absent. Global mean albedo used at
  ice-edge; local albedo step not modelled. Underestimates ice extent
  near runaway glaciation. Category: model limitation.
Flag 100: EBM annual-mean assumption breaks down at e > 0.3.
  Apoastron winters may drive volatile condensation or atmospheric
  collapse. Formula underestimates maximum glaciation extent on highly
  eccentric worlds. Category: model limitation.

### Flags resolved this session
- Flag 92: Ice-line latitude — resolved and implemented.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60, 63, 64,
                   97, 98, 99, 100
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57, 58,
                 62, 65, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                 79, 80, 81, 82, 83, 84, 85, 86, 87, 94, 95
Deferred — upstream dependency: 06, 07, 16, 25, 29, 40, 42, 43, 44,
                                  53, 90, 91, 96
Model applicability limit: 68
Model limitation: 88, 89, 93
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 08: Sediment Transport. Prior research exists (FLAGS 1–8
documented; Weertman sliding law and gravity multiplier correction
were the focus of the most recent V08 session). Review prior research
record before determining whether a new Gemini prompt is required or
whether implementation can proceed from validated formulas.

---
## Scaffold 011 — Variable 08: Volatile Inventory
**Date:** 2026-04-14
**Type:** Implementation

### What was implemented
Variable 08 maps cascade inputs from V01–V06 to a complete volatile
inventory: snow line positions, bulk volatile mass fraction, elemental
partitioning, core-mantle stripping, late veneer delivery, nebular
hydrogen ingassing, mantle oxygen fugacity, Gibbs free energy outgassing
speciation, melt fraction, time-integrated outgassing, atmospheric
column mass, and surface pressure. This variable resolves the
speciation: None block that has prevented V07 phase state evaluation
since Scaffold 009.

Sediment transport, previously designated Variable 08, is renumbered
Variable 09. No V09 files exist yet. This renaming has no code
consequence at this time.

### Cascade insertion
V08 runs between V06 and V07.
New execution order: v01 → v02 → v03 → v05 → v04 → v06 → v08 → v07

### Files created
variable_08_volatile_inventory/__init__.py
variable_08_volatile_inventory/snow_lines.py
  — R_snow,H2O = 2.7×(M_star/M_☉)² AU; R_snow,i = R_snow,H2O×(170/T_cond,i)²
  — Sources: viscously-heated disk power-law; solar system architecture calibration
  — Calibrated: H2O=2.7 AU, CO2=10.08 AU, CO/CH4/N2=38.5 AU at 1 M_☉ ✓

variable_08_volatile_inventory/bulk_volatile_fraction.py
  — X_vol = X_dry + Σ X_max,i / (1 + exp(−0.44×(a_m−R_snow,i)/R_H))
  — Source: logistic snow-line model; k=0.44 from 10 R_H oligarchic
    feeding zone (Kokubo & Ida 1998)
  — X_dry=1e-3, X_max: H2O=0.45, CO2=0.10, N2=0.02

variable_08_volatile_inventory/elemental_partitioning.py
  — X_bulk,i = X_dry×f_i,dry + X_ice,i(a_m)
  — EH3 fractions: f_S=0.916, f_C=0.067, f_H=0.008, f_N=0.008, f_Ar=2e-7
  — Source: EH3 unequilibrated enstatite chondrites

variable_08_volatile_inventory/core_mantle_partitioning.py
  — D_i = (K_D−1)/[1+CMF×(K_D−1)]; X_mantle,i = X_bulk,i×(1−D_i×CMF)
  — K_D Earth (135 GPa): H=29, C=107, N=14, S=100
  — K_D Mars (14 GPa): H=1, C=500, N=14 (fallback), S=100 (fallback)
  — Log-linear interpolation in P_cmb between anchors
  — Sources: Armstrong et al. (2019), Deng et al. (2020)
  — Earth calibration: C=1.89 ppm, N=1.53 ppm, S=27.66 ppm, H=0.79 ppm ✓

variable_08_volatile_inventory/late_veneer.py
  — M_LV = M_kg × 10^(−2.3 + 0.3×N(seed+8_000_000))
  — 80% EH3 / 20% CI chondrite mixing
  — Mixed fractions: H=0.004006, C=0.006494, N=0.000626, S=0.01155
  — Sources: N-body Monte Carlo simulations; Ru isotopic constraints
    (Wasson & Kallemeyn 1988; Lodders 2003)
  — Earth calibration: post-veneer C≈50 ppm ✓, N≈6.17 ppm (see Flag 133)

variable_08_volatile_inventory/nebular_ingassing.py
  — t_disk = 5×(M_star/M_☉)^−0.5 Myr
  — f_env = 1.06e-5×(M/M_⊕)³×t_disk
  — P_env = f_env×M×g/(4πR²)
  — ΔX_H = 0.419×(P_env/1e5) ppm; ΔX_H2O = ΔX_H×8.936
  — Sources: Ikoma & Genda (2006); Mamajek (2009); Ribas et al. (2015)
  — Earth calibration: ΔX_H2O=228 ppm → closes 272+228=500 ppm ✓
  — Mars calibration: ΔX_H2O=0.04 ppm (negligible) ✓

variable_08_volatile_inventory/oxygen_fugacity.py
  — ΔIW = 2.54×log10(P_cmb/1e9) − 1.91
  — IW buffer: log10(fO2,IW) = 6.776 − 27215/T (O'Neill 1987)
  — Sources: Armstrong et al. (2019), Deng et al. (2020)
  — Calibration: Vesta ΔIW=−1.91 ✓, Mars ΔIW=+1.00 ✓, Earth ΔIW=+3.50 ✓

variable_08_volatile_inventory/equilibrium_speciation.py
  — log10(K_i) = A_i + B_i/T; NIST-JANAF, valid 1200–2500 K
  — K1 H2O/H2: A=−2.324, B=12628
  — K2 CO2/CO: A=−4.517, B=14780
  — K3 CH4: A=−0.277, B=41912
  — K4 SO2: A=−3.713, B=15501
  — K5 H2S: A=−0.287, B=11552
  — K6 NH3: A=−5.173, B=2397
  — Earth calibration (T=1600K, ΔIW=+3.5): H2O/H2=159 ✓, CO2/CO=22.6 ✓
  — Mars calibration (T=1500K, ΔIW=+1.0): H2O/H2=8.14 ✓, CO2/CO=1.42 ✓

variable_08_volatile_inventory/melt_fraction.py
  — P_i=(T_m−1400)/(100−10) GPa; ΔT_rh=2.2×T_m²×R/E_a (E_a=300,000 J/mol)
  — D_lid=k×(T_m−ΔT_rh−T_eq)/q_s (stagnant lid only)
  — F̄=0.5×0.12×(P_i−P_f); ε_mobile=1.0; ε_stagnant Gaussian (Dorn 2018)
  — Sources: Langmuir (1992); Katz et al. (2003); Solomatov & Moresi (2000)
  — Earth calibration: F̄=12.7% ✓
  — Mars calibration: P_f=1.818 GPa > P_i=1.111 GPa → F̄=0 ✓

variable_08_volatile_inventory/outgassing_integral.py
  — M_outgassed,i = R_melt×X_melt,i×ε×age×3.154e16; X_melt,i=X_mantle,i/F_bar
  — Mass partitioning via molar mass weighting of speciation fractions
  — Earth calibration: M_outgassed,N2=3.83e18 kg ✓, M_outgassed,H2O=1.37e21 kg ✓

variable_08_volatile_inventory/atmospheric_mass.py
  — M_atm = M_outgassed − M_escaped − M_sequestered
  — H2O sequestration: Clausius-Clapeyron condensation at T_eq
  — CO2 sequestration: Walker (1981) weathering (Earth-empirical, flagged)
  — P_s = M_atm×g/(4πR²)
  — Earth calibration (abiotic): M_atm=3.88e18 kg, P_s=74,780 Pa ✓

variable_08_volatile_inventory/giant_planet_composition.py
  — E_Z = 6.3×(M/M_J)^−0.71; Z_planet = E_Z×Z_star; X_H=0.711, Y_He=0.274
  — Sources: Thorngren et al. (2016); Welbanks et al. (2019)
  — Jupiter: E_Z=6.3 ✓; Saturn: E_Z=14.9 ✓; Uranus/Neptune: E_Z~56 ✓

variable_08_volatile_inventory/variable_08_volatile_inventory.py
  — Entry point; regime routing; no physics; assembles outputs
  — Signature: run_variable_08(seed, v01, v02, v03, v04, v05, v06)
    Note: v04 added to original prompt spec — required for atm_class
    to drive sub-Neptune primary_retained routing and atmospheric logic.
    Architecturally justified; recorded here as unlisted deviation.

### Files modified
main.py
  — run_variable_08 imported
  — "v08" added to active_variables
  — v08 = run_variable_08(seed, v01, v02, v03, v04, v05, v06) called
    after v06 and before v07
  — run_variable_07 call updated to receive v08
  — V08 print block added
  — "v08" added to return dict

variable_07_hydrology/variable_07_hydrology.py
  — run_variable_07 signature updated to accept v08
  — speciation_dict argument to evaluate_all_species replaced with
    v08.get("speciation")
  — P_s fallback added: if v04["P_s_Pa"] is None, V07 uses
    v08.get("P_s_Pa") so phase states can evaluate against the
    computed secondary atmosphere pressure.
    Note: this V07 modification was not in the original implement
    prompt. It is physically correct — V08 is the authoritative source
    of P_s for rocky planets (Flag 40 blocked V04 from computing it).
    Recorded here as unlisted deviation.

### Verified runs
python main.py 1 --world-type rocky
  — Delta_IW = 1.6508 (target: 2.54×log10(25.2)−1.91 = 1.650) ✓
  — F_bar = 0.1326 (target: 0.5×0.12×(2.309−0.1) = 0.1325) ✓
  — X_vol = 0.001108 (inside H2O snow line at 0.1097 AU) ✓
  — Speciation: non-null dict with H2O, CO2, CO, H2, N2, SO2, H2S ✓
  — Phase states: H2O solid, CO2 solid, H2 gas_permanent, SO2 liquid ✓
  — Deferred speciation note: absent ✓

python main.py 42 --world-type rocky
  — T_m = 1349 K < T_sol,0 = 1400 K → P_i < 0 → F_bar = 0 ✓
  — M_atm = 0, P_s = 0 (no melt, no outgassing) ✓
  — Speciation: non-null dict produced from fO2 at T_m ✓
  — Phase states: all species "gas — no atmosphere" ✓
  — Deferred speciation note: absent ✓

### Known behaviour — M_atm on exosphere_only worlds (Flag 134)
Seed 1 has atm_class = exosphere_only (V04: heavy species do not meet
Jeans retention threshold) but V08 computes M_atm = 1.648e20 kg and
P_s = 3.62 MPa. This is a model coupling limitation: V08's escape term
strips only H2 and H2O; non-hydrogen species (CO2, CO, N2, H2S) are
not stripped. V04's exosphere_only classification implies all species
escape, but V08 does not gate on atm_class when computing M_atm. The
secondary atmosphere on exosphere_only worlds is therefore unphysical.
Recorded as Flag 134. Not patched — correction requires a research
prompt establishing the coupling between atm_class, M_dot, and
secondary atmosphere survival timescale.

### Known behaviour — N post-veneer overshoot (Flag 133)
Late veneer delivers ~6 ppm N to the mantle vs 1–2 ppm MORB-source
target. Known tension with Ru isotopic constraints on the NC/CC mixing
ratio. Atmosphere will be slightly N2-richer than modern Earth.
Recorded as Flag 133. Not patched.

### Flags opened this session
Flag 101: X_dry = 1e-3 — EH3 enstatite chondrite hydration.
  Solar System meteoritic measurement. Earth fallback.
  File: bulk_volatile_fraction.py
Flag 102: R_snow,H2O 2.7 AU coefficient — solar system snow line
  calibration. Solar System specific. Earth fallback.
  File: snow_lines.py
Flag 103: T_cond values (170 K, 88 K, 45 K) — nebular-pressure
  condensation temperatures. Solar System calibrated.
  File: snow_lines.py
Flag 104: M² scaling breaks down above ~5 M_☉.
  Model applicability limit.
  File: snow_lines.py
Flag 105: k = 0.44 — oligarchic feeding zone width (Kokubo & Ida 1998).
  Solar System calibrated. Earth fallback.
  File: bulk_volatile_fraction.py
Flag 106: X_max values from Lodders (2003) protosolar abundances.
  Solar-metallicity calibration.
  File: bulk_volatile_fraction.py
Flag 107: EH3 fractions f_i — Solar System meteoritic measurements.
  Earth fallback.
  File: elemental_partitioning.py
Flag 108: K_D,H = 29 at Earth P_cmb — diamond anvil cell + SIMS.
  Lab measurement. Earth fallback.
  File: core_mantle_partitioning.py
Flag 109: K_D,C = 107 at Earth P_cmb — experimental petrology.
  Earth fallback.
  File: core_mantle_partitioning.py
Flag 110: K_D,N = 14 at Earth P_cmb — experimental petrology.
  Earth fallback.
  File: core_mantle_partitioning.py
Flag 111: K_D,S = 100 at Earth P_cmb — thermodynamic models.
  Earth fallback.
  File: core_mantle_partitioning.py
Flag 112: K_D,H = 1 at Mars P_cmb (14 GPa) — H approaches neutral
  below 20 GPa. Lab data.
  File: core_mantle_partitioning.py
Flag 113: K_D,C = 500 at Mars P_cmb (14 GPa) — C inversely pressure
  dependent. Lab data.
  File: core_mantle_partitioning.py
Flag 114: K_D,N and K_D,S pressure scaling at Mars P_cmb not resolved.
  Earth anchor values used as fallback. Earth fallback pending
  low-pressure experimental data.
  File: core_mantle_partitioning.py
Flag 115: Late veneer log-normal μ=−2.3, σ=0.3 — N-body Monte Carlo
  calibration. Solar System calibration.
  File: late_veneer.py
Flag 116: 80/20 NC/CC mixing ratio — Ru isotopic anomaly constraint.
  Solar System specific.
  File: late_veneer.py
Flag 117: CI chondrite fractions — Wasson & Kallemeyn (1988), Lodders
  (2003). Multi-meteorite confirmed.
  File: late_veneer.py
Flag 118: k_H = 0.419 ppm/bar — Henry's Law for H2 in peridotitic melt.
  Lab measurement. Earth fallback.
  File: nebular_ingassing.py
Flag 119: f_env coefficient 1.06e-5 — Ikoma & Genda (2006).
  Solar-analog calibration. Earth fallback.
  File: nebular_ingassing.py
Flag 120: t_disk = 5×(M_star/M_☉)^−0.5 Myr — Mamajek (2009),
  Ribas et al. (2015). Multi-stellar empirical fit.
  Model applicability limit at extreme stellar masses.
  File: nebular_ingassing.py
Flag 121: ΔIW coefficients 2.54 and −1.91 — Armstrong et al. (2019),
  Deng et al. (2020). Confirmed Earth, Mars, Vesta. Multi-body confirmed.
  File: oxygen_fugacity.py
Flag 122: No saturation above ~200 GPa — extrapolation beyond
  experimental dataset. Model applicability limit.
  File: oxygen_fugacity.py
Flag 123: K1–K6 A, B coefficients — NIST-JANAF. Universal molecular
  thermodynamics. Valid 1200–2500 K only.
  Model applicability limit outside this range.
  File: equilibrium_speciation.py
Flag 124: T_sol,0 = 1400 K — anhydrous peridotite solidus.
  Lab measurement. Earth fallback.
  File: melt_fraction.py
Flag 125: γ = 100 K/GPa — solidus Clapeyron slope.
  Lab measurement. Earth fallback.
  File: melt_fraction.py
Flag 126: Γ = 10 K/GPa — mantle adiabatic gradient. Earth fallback.
  File: melt_fraction.py
Flag 127: dF/dP = 0.12 GPa^−1 — Katz et al. (2003).
  Anhydrous peridotite. Earth fallback.
  File: melt_fraction.py
Flag 128: ε_stagnant Gaussian — analytical fit to Dorn et al. (2018)
  + Noack et al. (2017). Earth fallback.
  File: melt_fraction.py
Flag 129: ε_mobile = 1.0 — degassing efficiency of melt.
  Idealised upper bound. Earth fallback.
  File: melt_fraction.py
Flag 130: Walker (1981) weathering constants — W_0=3.3e14 mol/yr,
  P_CO2_0=3e-4 bar, T_0=285 K, exponent=0.3, sensitivity=13.7 K.
  Earth-empirical. Not applicable without liquid water. Earth fallback.
  File: atmospheric_mass.py
Flag 131: FeO supply treated as non-limiting — 8 wt% FeO assumed.
  FeO content not a cascade variable. Earth fallback.
  File: nebular_ingassing.py
Flag 132: Equilibrium dissolution assumed — convective mixing
  timescale (days) << disk lifetime (Myr). Model applicability limit
  if magma ocean solidifies before disk dispersal.
  File: nebular_ingassing.py
Flag 133: N post-veneer overshoot — 80/20 mixing delivers ~6 ppm N
  vs 1–2 ppm MORB-source target. Known Ru isotopic tension.
  Model limitation — not patched.
  File: late_veneer.py
Flag 134: M_atm on exosphere_only worlds unphysical — V08 escape
  strips H2 and H2O only; V04 exosphere_only implies all species
  escape. Secondary atmosphere on exosphere_only worlds is not credible.
  Research prompt required to establish coupling between atm_class,
  M_dot, and secondary atmosphere survival. Model limitation — not patched.
  File: atmospheric_mass.py

### Flags resolved this session
Flag 6: Speciation — resolved. Speciation dict now produced by V08
  and passed to V07. Phase states evaluate for all seeds.
Flag 29: Rocky atmospheric composition underdetermined without mantle
  fO2 — resolved. fO2 computed in oxygen_fugacity.py from P_cmb_Pa.
Flag 40: X_vol (mantle volatile fraction) has no cascade origin —
  resolved. X_vol computed in bulk_volatile_fraction.py.
Flag 90: M_vol blocked — resolved. M_vol computable as X_vol × M_kg.

### Flags updated this session
Flag 93: PET on atmosphere-stripped worlds physically vacuous —
  primary blocker (speciation=None) removed. Flag 93 remains open
  as a model limitation for the case where atm_class=exosphere_only
  produces non-zero PET. See also Flag 134 for the related M_atm issue.

### Flags still open after this session
Inherent to model: 05, 08, 11, 12, 20, 22, 37, 48, 51, 59, 60,
                   63, 64, 97, 98, 99, 100
Earth fallbacks: 04, 09, 13, 23, 39, 41, 50, 52, 54, 55, 56, 57,
                 58, 62, 65, 67, 69, 70, 71, 72, 73, 74, 75, 76,
                 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 94,
                 95, 101, 102, 103, 105, 106, 107, 108, 109, 110,
                 111, 112, 113, 114, 115, 116, 118, 119, 124, 125,
                 126, 127, 128, 129, 130, 131
Deferred — upstream dependency: 07, 16, 25, 42, 43, 44, 53, 91, 96
Model applicability limit: 68, 104, 120, 122, 123, 132
Model limitation: 88, 89, 93, 97, 98, 99, 100, 133, 134
Survey-scope limitations: 31, 32, 33, 34, 35, 36, 46, 49
Model lower bound only: 47
Empirical GCM calibration: 38B
Solar System calibration: 117
Pre-registered duplicate: 26 (= Flag 34)

### Next step
Variable 09 (formerly Variable 08): Sediment Transport.
Prior research exists (FLAGS 1–8 documented; Weertman sliding law
and gravity multiplier correction were the focus of the most recent
session). Review prior research before determining whether a new
Gemini prompt is required or whether implementation can proceed from
existing validated formulas.

---
## Scaffold 009a — Flag 134 Resolution: Jeans and Thermostat Escape for Heavy Species on exosphere_only Worlds
**Date:** 2026-04-15
**Type:** Post-implementation physics patch

### What was implemented
Two modules were added and one modified to resolve Flag 134: the unphysical accumulation of a multi-bar secondary atmosphere on exosphere_only worlds, caused by V08's escape term stripping only H₂ and H₂O while leaving CO₂, CO, N₂, H₂S unstripped despite V04 classifying all heavy species as non-retained.

Root cause of Flag 134: V04 and V08 used two physically distinct escape frameworks that were not communicating. V04's Jeans criterion (instantaneous thermodynamic assessment per species) determined that no heavy species could be retained. V08's energy-limited escape (cumulative hydrodynamic mass loss budget) was applied only to H₂ and H₂O. The two modules were not exchanging atm_class information for heavy species stripping.

### Files created
variable_08_volatile_inventory/jeans_escape_heavy.py (original Flag 134 scaffold — see Scaffold 009)
variable_08_volatile_inventory/thermostat_escape_heavy.py — new module implementing the Chatterjee-Pierrehumbert (2024/2026) thermostat-limited hydrodynamic escape for λ < 2.0. Computes thermobase pressure P₀ = g m̄/σ_XUV, thermobase radius r₀ via inverted extended barometric law, thermobase density ρ₀ from ideal gas at T₀ = 6000 K, polytropic sonic radius r_sc, and Ṁ_thermostat = 4π r₀² ρ₀ c₀ × (r_sc/r₀)² × (T_sc/T₀)^(1/(γ−1)) with γ_eff = 1.15.

### Files modified
variable_08_volatile_inventory/jeans_escape_heavy.py updated with:

β_bulk_diatomic: nine-point DSMC lookup table with linear interpolation (Volkov et al. 2011, 2013). A Padé [2/3] closed-form expression was proven mathematically impossible under the all-positive-denominator constraint: back-calculation shows the required polynomial value at λ=15 is ≈ −418, which no combination of c₄,c₅,c₆ > 0 can produce given the fixed numerator. Five research sessions confirmed this structural impossibility. Lookup table used instead — exact at all nine DSMC nodes, positive-definite throughout. Asymptotic extrapolation for λ > 20: β ≈ 1 + 5.0/λ.
β_bulk_monatomic: validated Padé [1/2] with coefficients c₁ = 3.000, c₂ = −5.000, c₃ = −1.900, c₄ = 2.200. Discriminant = −5.19 < 0 (no real roots, no singularities). RMS = 0.0176 < 0.02 against Volkov et al. DSMC data. ✓
β_trace: validated formula β_trace = 1 − 2.40/λ. Calibrated against Earth (λ=6.00 → 0.600 ✓), Earth (λ=8.00 → 0.700 ✓), Mars (λ=5.58 → 0.570 ✓). All residuals = 0.000.
Trace/bulk selection threshold: bulk if X_i ≥ 0.50 (dominant mass constituent rule) or X_i ≥ 0.15 and λ_dominant ≤ 15 (strongly coupled rule). Otherwise trace.
λ < 2.0 branch: now routes to thermostat_escape_heavy.py instead of returning M_atm = M_outgassed conservatively.
jeans_v04 parameter added to compute_jeans_escape_one_species signature for λ_dominant computation; passed through from apply_jeans_escape_exosphere_only.

### Physics implemented
| Quantity | Formula | Source |
|---|---|---|
| β_bulk,diatomic | Nine-point DSMC lookup, linear interpolation | Volkov et al. (2011, 2013) |
| β_bulk,monatomic | 1 + (3.00λ−5.00)/(λ²−1.90λ+2.20) | Volkov et al. (2011, 2013) |
| β_trace | 1 − 2.40/λ | DSMC; Earth/Mars exosphere measurements |
| P₀ | g m̄/σ_XUV | Beer-Lambert + hydrostatic; exact derivation |
| r₀ | [1/R − k_B T̄/(G M m̄)×ln(P₀/P_surf)]⁻¹ | Extended barometric law (inverse-square gravity) |
| ρ₀ | P₀ m̄/(k_B T₀) | Ideal gas law at thermobase |
| r_sc | r₀×[G M m̄/(2γ k_B T₀ r₀)]^(1/(3−2γ)) | Parker wind sonic point condition (Mach=1) |
| Ṁ_thermostat | 4πr₀²ρ₀c₀×(r_sc/r₀)²×(T_sc/T₀)^(1/(γ−1)) | Chatterjee-Pierrehumbert (2024/2026) |

### Calibration verified
Earth T_exo analog (V04): λ_N2 = 9.430, β = 1.530 (bulk_diatomic) ✓
Earth T_exo analog (V04): λ_CO2 = 14.824, β = 1.403 (bulk_diatomic) ✓
β_trace Earth λ=6: 0.600 ✓; λ=8: 0.700 ✓; Mars λ=5.58: 0.570 ✓
β_mono RMS = 0.0176 < 0.02 across all nine Volkov DSMC points ✓
P₀ Earth: 9.81×4.65×10⁻²⁶/2.0×10⁻²¹ = 2.28×10⁻⁴ Pa ✓

### Seed outputs verified
python main.py 1 --world-type rocky

M_atm = 8.517×10¹⁹ kg (prior β=1.0 run: 1.648×10²⁰ kg; 48% reduction) ✓
P_s = 1.871×10⁶ Pa (prior: 3.62×10⁶ Pa) ✓
escape_details: N₂ regime=jeans, beta=1.530 (bulk_diatomic) ✓
escape_details: CO₂ regime=jeans, beta=1.403 (bulk_diatomic) ✓
escape_details: H₂S, CO regime=jeans, bulk_diatomic ✓
No NaN, no crashes ✓

python main.py 42 --world-type rocky

M_atm = 0.0, P_s = 0.0 (unchanged from prior run) ✓

python main.py 7 --world-type rocky (secondary_possible)

atm_class = secondary_possible
M_atm and P_s unmodified by escape module (gate is exosphere_only only) ✓

### Flags resolved this session
Flag 134: M_atm on exosphere_only worlds unphysical — resolved. Heavy species now subject to per-species Jeans escape (λ ≥ 3.6) or thermostat-limited hydrodynamic escape (λ < 2.0). Secondary atmosphere on exosphere_only worlds is now physically consistent with V04 atm_class.
Flag 135: beta_i = 1.0 placeholder — resolved. β now computed from validated DSMC data per species per regime.

### Flags opened this session
Flag 142: Padé [2/3] structural impossibility for diatomic β_bulk. No all-positive-denominator rational function with numerator degree 2 and denominator degree 3 can fit the Volkov et al. diatomic DSMC dataset. Proven by back-calculation: required polynomial value at λ=15 is ≈ −418, incompatible with c₄,c₅,c₆ > 0. Lookup table used as correct implementation. File: jeans_escape_heavy.py.
Flag 143: β_mono Padé [1/2] coefficients fitted to Volkov et al. (2011, 2013) DSMC data. Not Solar System specific. Valid λ ∈ [3.6, 20], monatomic species. File: jeans_escape_heavy.py.
Flag 144: β_trace c₁ = 2.40 calibrated to H escape through N₂/CO₂/O terrestrial backgrounds. Not a universal constant — calibrated to H as the trace species. File: jeans_escape_heavy.py.
Flag 145: σ_XUV values (N₂: 2.0×10⁻²¹ m², CO₂: 2.5×10⁻²¹ m²) are band-integrated resonant peak absorption cross-sections from synchrotron measurements. Species-intrinsic molecular properties; not solar-spectrum specific. File: thermostat_escape_heavy.py.
Flag 146: P₀ formula uses surface gravity g = G M/R². For small planets (M < 0.3 M_Earth), effective g at thermobase altitude is lower, reducing P₀ by factor ~2–3. Error bounded; surface-g approximation used as first-order estimate. File: thermostat_escape_heavy.py.
Flag 147: T₀ = 6000 K composition-averaged representative value for collisional-radiative thermostat clamp (Chatterjee & Pierrehumbert 2026). Range: 4000–8000 K. Valid for strongly ionised outflow above thermostat activation threshold. File: thermostat_escape_heavy.py.
Flag 148: γ_eff = 1.15 path-integrated empirical constant from Chatterjee-Pierrehumbert (2024/2026) hydrodynamic simulations. Valid: 0.1–2.0 M_Earth, XUV 10–500× PEL, CO₂/N₂ atmospheres. File: thermostat_escape_heavy.py.
Flag 149: F_XUV* threshold formula (η_γ-corrected power-law) not reducible to cascade inputs without dedicated thermospheric modelling. Bypassed by λ < 2.0 → thermostat-active logic. File: thermostat_escape_heavy.py.
Flag 150: Binary diffusion parameter b₁₂ temperature scaling (Marrero & Mason 1972). Crossover mass m_c implementation deferred. File: thermostat_escape_heavy.py.

### Known behaviour
H₂S and CO have λ = 999 (fallback): V04's jeans dict does not compute λ for H₂S or CO — these species are not in V04's per-species Jeans calculation. The cascade assigns λ = 999 as a fallback, classifying them as fully retained (Gamma = inf, M_atm = M_outgassed). This is physically conservative — they may escape on exosphere_only worlds. A research prompt is required to establish whether V04's Jeans calculation should be extended to cover H₂S and CO, or whether their λ values can be derived from cascade-available quantities without a new V04 research cycle.

### Flags still open after this session
(Complete list available in prior changelog entry. Additions this session: 142–150.)

### Next step
Rule 9 run complete. Changelog issued. The two queued non-blocking research prompts (β_bulk closed-form expression follow-up; Scaffold 009 sediment transport FLAGS 3–8 continuation) remain. Variable 09 (sediment transport) is the next cascade variable.
