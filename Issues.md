# MORTALIS Engine — Open Issues & Contribution Areas

These are the genuine unsolved problems in the engine, not polish items. Each one is a real design or physics question with no obvious answer. If you have relevant expertise, pick one and dig in.

The constraint that applies to all of them: **the variable cascade must remain intact.** Every fix or addition must receive the full resolved state of prior variables and pass a coherent state to the next. A change that produces interesting output in isolation but breaks downstream dependencies is not a valid fix.

---

## Issue 1 — Sediment Transport Volume Calibration

**Status:** Known bug. Architecture correct, absolute volumes wrong.

**The problem:** The Bagnold aeolian and glacial transport rates are physically derived but applied to total land area rather than terrain-class-specific areas. This inflates volumetric transport by roughly 100–1000× compared to terrestrial benchmarks. The 4-level sink cascade architecture is correct and mass is conserved — but the numbers flowing through it are too large.

**What correct looks like:** Earth's total sediment flux to the oceans is approximately 20 billion tonnes per year. A world of similar size and tectonic activity should produce comparable numbers. Current outputs are orders of magnitude above this.

**What's needed:** Recalibrate the production rates per terrain class against published terrestrial benchmarks. The glacial erosion rate formula (`W_glac = K_g × U²`) and the Bagnold aeolian formula are correct in form — the problem is in how the effective source areas are estimated, not in the formulae themselves.

**Relevant variables:** Eight (primary), Six (terrain class areas), Five (wind speed proxy).

---

## Issue 2 — Moon Variable

**Status:** Not implemented. Binary flag only.

**The problem:** The engine currently generates a binary Moon Flag (TRUE/FALSE) that affects tidal locking timescale assessment and axial tilt stability. Nothing else. The moon's mass, radius, orbital distance, tidal force, and influence on ocean circulation are entirely absent.

**Why it matters:** Tidal cycles determine coastal ecology rhythms, which the biology variable will need. A moon's gravitational influence on ocean circulation affects heat distribution across latitudes. Tidal locking of the moon itself (synchronous rotation) affects how it appears in the sky — a detail that matters for how civilizations develop calendars and cosmology.

**What's needed:** A moon sub-variable, probably sitting inside Variable Five (Kinematics) or as a Variable Five-B. Inputs: planetary mass, orbital distance, star mass (for stability bounds). Outputs: moon mass, radius, orbital period, tidal force at surface, tidal range estimate, synchronous rotation status.

**Constraint:** Moon formation is stochastic — giant impact hypothesis. The generation should reflect this, producing a wide range of moon sizes including no moon, small moon, Earth-analog moon, and rare large moon cases.

**Relevant variables:** Five (tidal locking, axial tilt stabilisation), Seven (tidal influence on coastal hydrology), Nine/biology (coastal ecology cycles).

---

## Issue 3 — Orbital Eccentricity

**Status:** Hardcoded to 0.00 throughout.

**The problem:** Every world the engine currently produces has a perfectly circular orbit. Non-zero eccentricity changes time-averaged insolation flux, produces asymmetric seasonal intensity (shorter hotter summers vs. longer cooler winters or vice versa depending on which apse aligns with which hemisphere's summer), and can push borderline worlds in and out of habitability on an orbital timescale.

**Why it matters:** Eccentricity is one of the Milankovitch cycles — a primary driver of ice age timing on Earth. A world with high eccentricity has a fundamentally different climate character than a circular-orbit world at the same semi-major axis.

**What's needed:** Eccentricity generation (Beta distribution, 0.0–0.5 for habitable worlds), time-averaged flux correction, seasonal insolation asymmetry fed into Variable Five's seasonal ice status calculation. Requires an N-body stability check — high eccentricity is often incompatible with the habitable zone over geological timescales if perturbing gas giants are present.

**Relevant variables:** Three (orbital mechanics), Five (seasonality, ice status), Four (climate stability over orbital cycle).

---

## Issue 4 — Variable Nine: Biology (The Biosphere)

**Status:** Not implemented. This is the most open and most important problem.

**The problem:** Variables One through Eight produce a physically coherent abiotic world. Variable Nine needs to introduce life — and life changes everything it touches. O₂ produced by photosynthesis alters atmospheric chemistry, which alters greenhouse forcing, which alters temperature, which alters biome distribution, which alters the life that can exist. Variable Nine must iterate.

**What it needs to produce:**
- Atmospheric O₂ and CH₄ from photosynthesis and microbial metabolism (feeds back into Variable Four's greenhouse calculation)
- Biome distribution across the climate-terrain grid established by Variables Five and Six
- Primary productivity estimates per biome
- The abiotic-to-biotic soil transition: regolith from Variable Eight becomes true soil through microbial activity and organic matter accumulation
- Nitrogen fixation — the primary limiting nutrient identified in Variable Eight becomes biologically available through symbiotic and microbial cycling
- Biosphere complexity index — a measure of how much evolutionary time and ecological diversity the world has accumulated

**The constraint that matters most:** Biology must emerge from the physical conditions the prior variables established. A world with 2.273 atm atmospheric pressure and a specific stellar spectrum should produce different photosynthetic chemistry than an Earth-analog world. The biosphere cannot be painted on — it must be caused by the physics.

**The fantastical extension:** Once baseline biology is established, the variable needs to support exotic biosphere configurations. High O₂ environments supporting larger flying organisms. Bioluminescent mineral substrates producing underground light ecosystems. Chemosynthetic food webs around geothermal oases. These are not fantasy additions — they are physically legal outcomes of specific planetary conditions that Earth never produced.

**Relevant variables:** All of them. Biology touches everything.

---

## Issue 5 — Rendering Script

**Status:** Not implemented.

**The problem:** The engine produces structured numerical output — plate boundaries, clustering parameters, river basin counts, biome distributions, mountain range statistics. A rendering script should read this output and produce a visual map where every feature has a physical cause.

**What correct looks like:**
- Coastlines derived from isostatic freeboard and ocean coverage fraction
- Continental outlines shaped by the clustering parameter and plate count
- Mountain ranges placed at convergent boundaries
- Deserts in rain shadows leeward of mountain ranges
- River networks following the D8 basin delineation
- Biomes from the Variable Nine distribution, intersected with terrain
- Tectonic features — rift valleys, volcanic arcs, hotspot chains — placed at their respective boundary types

**The goal:** A map that is unique per seed, internally coherent, and where every feature can be traced back to a physical cause in the engine output. Not a map that looks like a fantasy world map. A map that *is* the world the engine produced.

**Relevant output fields:** clustering, plate count, boundary inventory, freeboard, ocean/land/ice fractions, river basin delineation, aridity index, rain shadow flags, mountain range statistics, hotspot count.

---

## Issue 6 — Biological Readiness Index Calibration

**Status:** Functional but heuristic. Weights set by judgment, not calibration.

**The problem:** The Biological Readiness Index (BRI) is a composite 0–1 score assembled from substrate depth, pH, nutrient availability (nitrogen-weighted), surface temperature, and liquid water access. The weights were set by judgment. There is no calibration against known habitability research or against worlds where we know biology did or did not emerge.

**What's needed:** A principled weighting scheme grounded in astrobiology research. Published habitability indices provide starting points. The BRI should be able to distinguish not just between habitable and uninhabitable but between a world where simple microbial life is plausible and a world where complex multicellular life is plausible.

**Relevant variables:** Eight (primary), Four (temperature, pressure), Seven (liquid water access).

---

## Issue 7 — CO₂ Full Two-Pass Architecture

**Status:** Partially fixed. Root cause remains.

**The problem:** CO₂ is generated in Variable Four before tectonic boundary geometry is known (Variable Six). A two-pass reconciliation now runs in Variable Six — adjusting CO₂ toward the volcanic budget after boundaries are calculated. But the initial draw in Variable Four is still anchored to heat flux alone rather than a proper physical derivation of outgassing rate. The tension flag should fire on perhaps 1 in 20 worlds as a genuine geological anomaly. Currently it fires on approximately 1 in 30, which is close but not yet physically motivated from first principles.

**What full resolution looks like:** Variable Four generates a provisional CO₂ from heat flux, simulation age, and tectonic regime. Variable Six computes the actual volcanic outgassing budget from boundary inventory, spreading rates, and arc lengths. Variable Six then confirms, reconciles, or flags tension. The flag should be rare and meaningful when it appears.

**Relevant variables:** Four (CO₂ generation), Six (volcanic budget, reconciliation).

---

## General Contribution Notes

The engine is a single Python file with no external dependencies. Every function is documented with its physical basis. The variable sequence is the architecture — read it top to bottom and the physics tells you what each function is doing and why.

If you find a formula that is wrong, cite the source you're correcting it against. If you propose a new sub-variable, document what prior variable outputs it requires and what it passes forward. If you change a distribution parameter, explain the physical justification.

The engine is a framework. Almost everything except the variable cascade order is negotiable.
