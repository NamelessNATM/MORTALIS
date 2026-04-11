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

