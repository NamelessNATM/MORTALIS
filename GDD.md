# Game Design Document (GDD)

## 1. Game Overview
**Game Title:** MORTALIS
**Genre:** Hardcore Multiplayer Simulation RPG / Action RPG
**Platform:** PC, Consoles, Future Tech / Full Dive VR (Target)
**Target Audience:** Hardcore gamers, fans of emergent gameplay, ecosystem simulations, and simulation RPGs.

### 1.1 Concept
A Dark Souls-esque MMORPG set in a fully dynamic, "living" world where players influence the world through city-building and resource contribution. Unlike traditional MMOs where the world is static and resets, this game features a persistent world simulation where player actions have permanent consequences. The world is governed by biological and ecological principles rather than static game logic.

### 1.2 Unique Selling Points (USPs)
*   **True Living World:** The world is not a static backdrop; it evolves based on player interaction and internal biological simulations.
*   **Dynamic City Migration:** Cities are non-permanent entities. When a region becomes "desolated" by high-level player activity, NPCs migrate to safer locations.
*   **Organic City Growth:** Cities grow based on resource contributions rather than direct placement. Architecture reflects the contributing species.
*   **Finite & Biological Ecosystem:** No magical respawns. Mobs and vegetation follow biological lifecycles (birth rates, growth, death).
*   **Impermanence & Agency:** Quests are unique, non-repeatable events that change the state of the world forever.
*   **Democratic World Management:** Players collectively decide the fate of a ruined world: reset or adapt.
*   **Immersive Communication:** Proximity-only voice chat emphasizes realistic social interactions.
*   **Realistic Travel & Trade:** No fast travel and local-only trading create a grounded, immersive world.

---

## 2. Gameplay Mechanics

### 2.1 Core Loop
1.  **Explore & Conquer:** Players explore new lands, fighting mobs and gathering resources.
2.  **Desolate:** As players become powerful, their presence and the escalation of threats desolate the land.
3.  **Migrate:** Players must follow the migrating NPCs to access shops, quests, and services, or stay in desolated lands for high-risk gameplay.
4.  **Rebuild/Defend:** Players participate in securing new locations for migrating NPCs and contributing to new city growth.

### 2.2 Dynamic World Simulation & Ecology
*   **Biological Principles:** Mobs have birth rates and populations. No traditional respawns; new entities are born from existing populations.
*   **Instinctual AI:** Mobs have survival instincts, migration patterns, and social structures.
*   **Ecosystem Cascades:** Removing a species affects the entire ecosystem.
*   **Desolation:** High-level areas become environmentally harsh.
*   **City Abandonment:** NPCs abandon desolated areas, causing civilization to retreat from end-game zones.
*   **Resource Management:** Vegetation grows back over time; resources are finite.
*   **Ore Depletion:** [TBD - Pending decision]

### 2.3 City Building & Settlement
*   **Founding:** Players choose tiles to found cities. Location matters (e.g., hazards).
*   **Growth:** Driven by resource contribution. Players do not place individual structures.
*   **Architecture:** Evolved based on contributor species.
*   **Founders:** Highest contributors are recorded as Founders. NPCs will remember and recognize these players.

### 2.4 Character Progression
*   **Classless System:** No pre-defined classes.
*   **Skill-Based Growth:** Skills improve through usage. No generic XP.
*   **Species/Race Freedom:** Freedom to be any species.
*   **Magic System:** Hidden affinity discovered through gameplay.
    *   **Type A (Material):** Uses physical components.
    *   **Type B (Vitality):** Uses HP/Stamina.
    *   **Type C (Arcane):** Vancian-style, uses Mana, requires memorization.

### 2.5 Combat & Death
*   **Combat Style:** Dark Souls-esque, deliberate and punishing. Stamina management is key.
*   **Permadeath:** Death is permanent. Character is lost.
    *   **Loot Drop:** Drop all gear/inventory.
    *   **Skill Inheritance:** Diminishing returns on next character (100% -> 75% -> 50% -> 25%).
*   **Social Interactions:** Bodies can be buried/funeral rites.
*   **PvP & Justice:** Open PvP, Bounty system for crimes, Jail/Fines.

### 2.6 Economy, Loot & Crafting
*   **Deterministic Loot:** Harvest/carve specific parts (no RNG gear drops).
*   **Carving Skill:** Dedicated skill for harvesting.
*   **Physical Economy:** Items have weight/bulk, must be transported.
*   **Decay:** Items and carcasses rot/rust.
*   **Crafting-Only Gear:** All gear must be crafted.
*   **Localized Trading:** No global auction house. Bulletin boards in cities.
*   **Banking:** Character-bound and location-bound. Risk of loss if city destroyed.

### 2.7 Social, Guilds & Diplomacy
*   **Guilds:** Must rent HQs in existing cities.
*   **City Alliances:** Cities can form alliances. Reputation propagates.
*   **Communication:** Proximity voice chat only. No text chat.

### 2.8 Travel & Survival
*   **No Fast Travel:** Must physically traverse.
*   **Mounts:** Can die.
*   **Survival:** Hunger, Thirst, Temperature.

### 2.9 Quests, Legacy & Enemy Hierarchy
*   **Impermanent Quests:** Unique world events.
*   **Legacy:** NPCs remember player deeds (Founders, Boss kills).
*   **Enemy Hierarchy:**
    *   **Static Power:** No level scaling.
    *   **Dynamic Respawn/Mutation:** Mobs mutate and evolve based on player actions.
    *   **Boss Tiers:** Area, Region, Continental, World Bosses (Calamities).
    *   **World Bosses:** Permanent world alteration, require server-wide coordination.

### 2.10 Server Ecology & Governance
*   **Resource Depletion:** Over-harvesting can ruin the world.
*   **Emergency Meetings:** Vote to Reset or Adapt.
*   **Democratic Voting:** The server population votes on a course of action.

---

## 3. Story and Setting

### 3.1 World Design
*   **Impermanence:** The world evolves and is not static.
*   **Desolation Cycle:** Civilization retreats from power, creating a frontier.
*   **Tile-Based:** For city founding purposes.

### 3.2 Narrative
*   **Emergent Story:** History is defined by player actions.
*   **No "Chosen One":** Collective history of the players and the world.

### 3.3 Characters
*   **NPCs:** Inhabitants who populate cities and remember player actions (specifically Founders and Boogeymen).
*   **Players:** Can be any species, influencing the world's aesthetic.

---

## 4. Art and Audio

### 4.1 Art Style
[Visual style description: Pixel art, Realistic, Low-poly, etc.]

### 4.2 Sound Design
*   **Voice Chat:** High-quality proximity voice implementation (crucial for gameplay).
*   [Music style, Sound effects]

---

## 5. Technical Requirements
*   **Infrastructure:** Quantum Computing Servers (Required for massive complexity of dynamic world simulation).
*   **AI Engine:** Quantum-Powered Neural Networks (For Mobs/NPCs evolutionary and psychological adaptability).
*   **Engine:** Unreal Engine 5 (Suggested).
*   **Networking:** Low-latency voice chat solution.
*   **Platforms:** PC, Future Tech / Full Dive VR.

---

## 6. Development Roadmap
*   **Phase 1:** Core Combat, Movement, City Building Prototype.
*   **Phase 2:** Vertical Slice, Basic AI Biology.
*   **Phase 3:** Alpha (Ecosystem Interaction), Quest Generation.
*   **Phase 4:** Beta.
*   **Phase 5:** Release.
