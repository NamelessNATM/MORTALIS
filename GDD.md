# Game Design Document (GDD)

## 1. Game Overview
**Game Title:** [Title Placeholder]
**Genre:** Multiplayer Simulation RPG
**Platform:** [e.g., PC]
**Target Audience:** [e.g., Simulation fans, RPG players]

### 1.1 Concept
A dynamic world simulation where players influence the world through city-building and resource contribution.

### 1.2 Unique Selling Points (USPs)
*   **Organic City Growth:** Cities grow based on resource contributions rather than direct placement.
*   **Species-Dependent Architecture:** City appearance reflects the species contributing resources.
*   **Legacy System:** Players are remembered by NPCs as founders of cities.
*   **Immersive Communication:** Proximity-only voice chat emphasizes realistic social interactions.
*   **Realistic Travel & Trade:** No fast travel and local-only trading create a grounded, immersive world.
*   **High-Stakes Economy:** Physical banking means local disasters have real consequences.

---

## 2. Gameplay Mechanics

### 2.1 City Building & Settlement
*   **Founding:** Players choose a specific tile to found a city. Location matters (e.g., building near a volcano is possible but risky).
*   **Growth:** Players do not place individual structures. Instead, they contribute resources to the city, which causes it to generate and grow over time organically.
*   **Architecture:** The city's visual style and architecture evolve based on the species of the players who contribute resources.
*   **Founders:** The highest contributing players are recorded as "Founders". NPCs will remember and recognize these players.
*   **Population:** NPCs will eventually move to these player-founded cities.

### 2.2 Magic System
*   **Status:** Magic exists in the world.
*   **Mechanics:** TBD (System currently under design).

### 2.3 Player Session Management
*   **Logout:** When a player logs off, their character vanishes safely from the world. There are no harsh penalties for logging off (e.g., sleeping bodies remaining in danger).

### 2.4 Core Loop
[Describe the primary gameplay loop: Gather Resources -> Contribute to City -> Unlock Status/Lore -> Repeat]

### 2.5 Controls
*   **Move:** [Key/Input]
*   **Action:** [Key/Input]
*   **Menu:** [Key/Input]
*   **Push-to-Talk:** [Key/Input]

### 2.6 Progression System
*   **Founder Status:** Gaining recognition from NPCs.
*   **City Development:** Watching the city grow and change based on contributions.

### 2.7 Character Creation
*   **Species/Race Freedom:** Players are free to be whatever species or race they desire. This choice directly impacts the architectural style of cities they contribute to.

### 2.8 Combat & PvP
*   **Open PvP:** Player-versus-Player combat is enabled throughout the world.
*   **Justice System:**
    *   **Crime:** Killing a player or NPC within a city is a crime.
    *   **Guard Response:** NPC guards will attempt to arrest or kill the offender.
    *   **Punishment:**
        *   **Jail:** Players are placed in a jail cell for a specific duration.
        *   **Fines:** Players can pay a fee to be released early.
        *   **Jailbreak:** Other players can break prisoners out of jail.

### 2.9 Diplomacy & Alliances
*   **City Alliances:** Cities can form alliances with one another.
*   **Reputation Propagation:** Committing a crime (e.g., killing a player/NPC) in one city causes the player to become hostile in that city *and* all allied cities.

### 2.10 Communication
*   **Proximity Voice Chat:** The primary and only form of communication.
    *   **Mechanic:** Players can only hear others who are physically close to them in the game world.
    *   **No Text Chat:** There is no global or local text chat system.

### 2.11 Travel & Mounts
*   **Mounts:** Players can use mounts for transportation.
    *   **Mortality:** Mounts are not immortal; they can die.
*   **Fast Travel:** There is **NO** fast travel. Players must physically traverse the world.

### 2.12 Economy & Trade
*   **Localized Trading:** There is no global auction house or marketplace.
*   **Bulletin Boards:** Players must travel to specific cities and post sell orders on physical bulletin boards.
*   **NPC Trading:** Players can also sell items directly to NPCs in cities.
*   **Banking:**
    *   **Character-Bound:** Bank storage is personal to the character.
    *   **Physical Location:** Items stored in a bank are physically located in that city.
    *   **Risk:** If a city is destroyed, all items stored in its bank are lost permanently.

### 2.13 Survival Mechanics
*   **Vitals:** Players must manage Hunger and Thirst.
*   **Temperature:** Environmental temperature affects the player.
*   **Clothing:** Players must wear appropriate clothing for the climate to avoid negative effects (e.g., warm clothes for snow, light clothes for desert).

---

## 3. Story and Setting

### 3.1 Story Synopsis
[Summary of the plot]

### 3.2 Characters
*   **NPCs:** Inhabitants who populate cities and remember player actions (specifically Founders).
*   **Players:** Can be any species, influencing the world's aesthetic.

### 3.3 World Design
*   **Tile-Based World:** The world is divided into tiles where players can choose locations for cities.
*   **Environmental Hazards:** Locations vary in suitability (e.g., volcanoes).
*   **Climate Zones:** Different regions have distinct temperatures requiring specific preparation.

---

## 4. Art and Audio

### 4.1 Art Style
[Visual style description: Pixel art, Realistic, Low-poly, etc.]

### 4.2 Sound Design
*   **Voice Chat:** High-quality proximity voice implementation (crucial for gameplay).
*   [Music style, Sound effects]

---

## 5. Technical Requirements
*   **Engine:** [e.g., Unity, Unreal, Godot, Custom]
*   **Language:** [e.g., C#, C++, Python]
*   **Platforms:** [List supported platforms]
*   **Networking:** Low-latency voice chat solution required.

---

## 6. Development Roadmap
*   **Phase 1:** Prototype (City Building Mechanics)
*   **Phase 2:** Vertical Slice
*   **Phase 3:** Alpha
*   **Phase 4:** Beta
*   **Phase 5:** Release
