# MORTALIS World Generation Engine

**A physically derived, ontogenetic world simulation. No noise functions. No hardcoded terrain. Everything is caused.**

---

## What This Is

Most procedural world generators work backwards. They generate a heightmap using Perlin noise, then paint biomes on top, then add rivers that flow in plausible-looking directions. The mountain exists because a noise function produced a high value at those coordinates. The desert exists because someone decided deserts go near mountains.

This engine works forward.

A single seed number initialises a cascade of physical first principles. Planetary mass determines gravity. Gravity determines mountain height. A host star determines insolation. Insolation and atmospheric composition determine surface temperature. Temperature determines whether water is ice or ocean. Ocean coverage determines albedo. Albedo feeds back into temperature. Tectonic geometry determines where rain shadows fall. Rain shadows determine aridity. Aridity determines where rivers form. And so on — eight variables deep, each one caused by everything that came before it.

The result is a world that is internally coherent in a way no noise-based generator can produce, because every feature has a physical ancestor traceable back to the first variable. When you attach a rendering script to this output, the map you get isn't decorated — it's *derived*.

---

## Why It Exists

MORTALIS is a permanent-death MMORPG built on a post-2040 full-dive VR platform. The true unit of play is not a character but a soul moving through successive lives. The world is the constant. Characters are temporary. What a character did to the world — factions shifted, things built or destroyed, wills left unfinished — persists after their death and shapes the lives that follow.

A world like that cannot be a noise map. It needs to behave like a real place — to respond consistently to physical laws, to remember what happened to it, to produce geography that exists for reasons. A desert must exist because it lies in the rain shadow of a mountain range. That mountain range must exist because tectonic plates collided. Those plates moved because mantle convection drove them. Mantle convection requires internal heat. Internal heat is a consequence of planetary mass.

The engine is the foundation that makes MORTALIS's central idea physically honest.

---

## Current State — Variables 1 through 8

The engine currently simulates eight abiotic variables in sequence. Each variable receives the outputs of all prior variables, resolves its own physical relationships, and passes a richer state to the next.

| Variable | What It Does |
|---|---|
| **One — Planetary Mass** | The axiomatic root. Establishes gravity, radius, escape velocity, internal heat flux, geologic lifespan, mountain height ceiling |
| **Two — Bulk Composition** | Core mass fraction (CMF) replaces the temporary density constant from Variable One. Triggers a full recalculation cascade — radius compresses or expands, gravity shifts, heat flux corrects for mantle fraction, magnetic dynamo state is established |
| **Three — Stellar Insolation** | Host star generated via IMF (0.50–1.30 M☉, mid-F through early-M). Orbital distance drawn within the physically derived habitable zone. Equilibrium temperature, Jeans escape profile for 7 gases, and the MORTALIS 24-month calendar all emerge from this variable |
| **Four — Atmosphere & Hydrology** | Atmospheric pressure derived from a physical mass balance: outgassed mass minus Jeans escape loss minus stellar wind sputtering. CO₂ generated from heat-flux-anchored baseline. Iterative ice-albedo feedback loop resolves the true surface temperature and world type |
| **Five — Planetary Kinematics** | Rotation rate and axial tilt. Tidal locking check. Coriolis parameter, Hadley cell boundaries, precipitation bands by latitude, diurnal temperature range, cloud fraction update, moon flag for tilt stability. The full MORTALIS time system is locked here |
| **Six — Tectonic Geometry** | Plate count, continental clustering (supercontinent ↔ dispersed), boundary inventory (convergent/divergent/transform), mountain ranges, subduction trenches, rift valleys, hotspot count, rain shadow flags, aridity index, coastline complexity, CO₂ reconciliation against volcanic budget |
| **Seven — Hydrology & River Systems** | Dual-state: current frozen state and latent liquid state. D8 flow routing. Drainage basin delineation (exorheic vs. endorheic). River network via Hack's Law. Navigable river length. Permafrost depth. Subglacial lake detection. Meltwater pulse calculation for ice-to-liquid transition |
| **Eight — Soil & Regolith** | Four weathering mechanisms (glacial grinding, freeze-thaw, Arrhenius chemical weathering, Bagnold aeolian). Source-to-sink sediment budget. 4-level topographic sink cascade (endorheic basins → rift valleys → continental shelves → subduction trenches). Mass conserved at every level. Abiotic nutrient profile. Biological Readiness Index |

---

## Usage

```bash
python mortalis_worldgen.py                  # random seed, prints seed at top
python mortalis_worldgen.py --seed 1810408725  # reproducible world
```

No external libraries. Standard library and `math` only. Python 3.7+.

Optional overrides for direct exploration:
```bash
python mortalis_worldgen.py --seed N --cmf 0.32 --star-mass 1.0 --orbit 1.0
```

---

## What the Output Looks Like

Each run produces a full terminal report stepping through all eight variables. Every number shows its physical derivation. Temporary constants are explicitly flagged and replaced as later variables resolve them. World type is classified at convergence: TEMPERATE OCEAN WORLD, WARM OCEAN WORLD, COLD WORLD, SNOWBALL STATE, GLOBAL WATERWORLD, DESERT WORLD, or RUNAWAY GREENHOUSE.

The seed is always printed — whether passed explicitly or generated randomly — so any world can be reproduced exactly.

---

## Where This Is Going

### Variable Nine — Biology

The biosphere variable is not yet implemented. This is the next major step. Biology needs to produce: atmospheric O₂ and CH₄ from photosynthesis and metabolism, biome distribution across the climate-terrain grid established by Variables Five and Six, primary productivity estimates, and the abiotic-to-biotic soil transition begun in Variable Eight.

Biology also closes the feedback loop — O₂ changes atmospheric chemistry, which changes greenhouse forcing, which changes temperature, which changes biome distribution. Variable Nine will need to iterate.

### The Rendering Script

The numerical output of Variables 1–9 is structured data. A rendering script should read this output and produce a visual map where every feature has a physical cause. Coastlines derived from isostatic freeboard and ocean coverage. Mountain ranges at convergent boundaries. Deserts in rain shadows. River networks from the D8 basin delineation. Biomes from the Variable Nine distribution. This map will be unique per seed and internally coherent in ways no current procedural game map is.

### Fantastical Parameter Space

The engine currently enforces physical realism calibrated to rocky terrestrial planets in our observable range. The formulae in Variables 1–8 can be adjusted — within the constraint of internal consistency — to produce worlds whose physics are legal but exotic. Higher atmospheric pressure enables large flying creatures. Different stellar spectra produce different photosynthetic chemistry and flora pigmentation. Altered mantle compositions produce different cave geometries and underground hydrology.

The goal is not fantasy as decoration. The goal is fantasy as a consequence of physical conditions. Dragons are not placed in the world — they emerge from a world where atmospheric pressure, gravity, and biosphere chemistry make a flying apex predator of that mass physically possible. Every creature is an evolutionary answer to the world the engine produced.

---

## Known Issues and Open Questions

The following are honest unresolved problems, not polish items:

**Sediment volume calibration.** The Bagnold aeolian and glacial transport rates are derived correctly but applied to total land area rather than terrain-class-specific areas. This inflates volumetric transport by 100–1000×. The cascade architecture and relative depths are correct; absolute volumes need recalibration against terrestrial benchmarks.

**CO₂ sequencing.** CO₂ is generated in Variable Four before tectonic boundary geometry is known (Variable Six). The engine now runs a two-pass reconciliation — adjusting CO₂ toward the volcanic budget after boundaries are known — but the initial draw is still somewhat decoupled from physical first principles. A proper fix would derive baseline CO₂ from heat flux and simulation age in Variable Four, then refine against actual boundary count in Variable Six.

**Atmospheric pressure.** Currently derived from a physical mass balance (outgassing minus Jeans escape minus sputtering). The outgassing model is calibrated to Earth but the volatile delivery stochastic term (cometary bombardment) is still a lognormal with sigma=0.25. A more principled treatment of volatile delivery would connect to the protoplanetary disk chemistry, which is outside the current scope.

**Orbital eccentricity.** Hardcoded to 0.00 throughout. A non-zero eccentricity changes time-averaged insolation flux and produces asymmetric seasonal intensity. Implementing this requires an N-body orbital dynamics module that accounts for perturbing gas giants. Deferred.

**Moon physics.** The engine currently generates a binary Moon Flag (TRUE/FALSE) that affects tidal locking timescale and axial tilt stability. The moon's actual mass, radius, orbital distance, and tidal influence on ocean circulation are not yet modelled. A moon variable — with its own physical derivation — would feed directly into tidal cycle length, which affects coastal ecology in the biology variable.

**Biological Readiness Index.** The BRI is a reasonable composite heuristic but its weights were set by judgment rather than calibration against known habitability research. Community input on a more principled weighting scheme would be valuable.

---

## The Design Constraint That Cannot Move

Every variable must cascade properly. Variable N+1 must receive the full resolved state of Variables 1 through N and build on it. No variable can introduce a property that contradicts a prior variable's physics. The chain of causality is what produces the map quality. A change that breaks the cascade — even if it produces a more interesting individual output — undermines the engine's core value.

Within that constraint, almost everything else is negotiable. The distributions can be widened. The formulae can be adapted for exotic physics. Entirely new variables can be inserted between existing ones. The engine is a framework, not a fixed simulation.

---

## Contributing

Issues and discussion are open. The most valuable contributions right now are:

- Sediment transport recalibration against published terrestrial benchmarks
- Moon variable design and physical derivation
- Orbital eccentricity implementation
- Variable Nine (Biology) architecture — this is the most open and most important problem
- Rendering script — reading the engine output and producing a coherent visual map
- Fantastical parameter space — which formulae can be adjusted, and how far, while maintaining internal consistency

If you have a background in planetary science, atmospheric physics, hydrology, ecology, or procedural generation, there is probably a variable that could use your expertise.

---

## Proof of Concept Seed

Seed `1810408725` is the current primary candidate world — the one the engine was hunting for across hundreds of runs under a five-filter search (temperate world, dispersed or semi-clustered continents, no tidal locking, confirmed moon, 282–298 K mean temperature).

It produces: K-class star, 1.083g surface gravity, 2.273 atm atmospheric pressure, 294.2 K mean surface temperature, VIGOROUS tectonic regime, 25 plates, 13 mountain ranges, 7 rift valleys, 167,139 km of active navigable rivers, 53 geothermal oases, moon confirmed, biological readiness 0.85.

Run it. Read the cascade. That is what physical first principles produce when you let them run without interference.

---

*MORTALIS is a permanent-death MMORPG built on a post-2040 full-dive VR platform. The world is the constant. This engine is how the world is made.*
