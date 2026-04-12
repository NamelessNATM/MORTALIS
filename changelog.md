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
