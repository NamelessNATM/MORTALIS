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

