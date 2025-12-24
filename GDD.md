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
*   **One-Time World Events:** Unique bosses and quests are finite, creating a true history of "firsts."
*   **Democratic World Management:** Players collectively decide the fate of a ruined world: reset or adapt.

---

## 2. Gameplay Mechanics

### 2.1 City Building & Settlement
*   **Founding:** Players choose a specific tile to found a city. Location matters (e.g., building near a volcano is possible but risky).
*   **Growth:** Players do not place individual structures. Instead, they contribute resources to the city, which causes it to generate and grow over time organically.
*   **Architecture:** The city's visual style and architecture evolve based on the species of the players who contribute resources.
*   **Founders:** The highest contributing players are recorded as "Founders". NPCs will remember and recognize these players.
*   **Population:** NPCs will eventually move to these player-founded cities.

### 2.2 Magic System
*   **Hidden Affinity:** Players do not choose a mage class at character creation. Instead, they discover their hidden affinity through exploration and gameplay.
*   **Mage Types:**
    *   **Type A (Material Mage):** The most common type.
        *   **Mechanic:** Spells require physical components (herbs, gems, etc.) to cast.
        *   **Economy:** Directly tied to the economy; running out of items means no casting.
    *   **Type B (Vitality Mage):** Uncommon/Rare.
        *   **Mechanic:** Magic draws from the user's physical stats (HP/Stamina).
        *   **Risk:** Overuse of magic can be fatal to the caster.
    *   **Type C (Arcane Mage):** Extremely Rare.
        *   **Mechanic:** Vancian-style magic. Spells are "memorized" at a campfire.
        *   **Resource:** Uses a dedicated "Mana" pool. When Mana runs out, the player must rest/memorize again to cast.

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
*   **Magic Discovery:** Unlocking hidden magical affinities.
*   **Legendary Status:** Being immortalized in history for unique feats (e.g., boss kills).

### 2.7 Character Creation
*   **Species/Race Freedom:** Players are free to be whatever species or race they desire. This choice directly impacts the architectural style of cities they contribute to.
*   **Hidden Traits:** Players are born with hidden magical affinities that are not revealed immediately.

### 2.8 Combat & PvP
*   **Open PvP:** Player-versus-Player combat is enabled throughout the world.
*   **Justice System:**
    *   **Crime:** Killing a player or NPC within a city is a crime.
    *   **Bounties:**
        *   **Trigger:** Killing a player or stealing their loot (especially carcass hauls) triggers the bounty system.
        *   **Alignment:** Victims are often aligned with a city (usually their starting city).
        *   **Consequence:** The aggressor is declared a criminal by the victim's city *and* all allied cities. A bounty is placed on their head, encouraging other players to hunt them.
        *   **Shifting Alignment:** City alignment is dynamic; players can change allegiance, but crimes carry over until resolved or time passes.
    *   **Guard Response:** NPC guards will attempt to arrest or kill the offender.
    *   **Punishment:**
        *   **Jail:** Players are placed in a jail cell for a specific duration.
        *   **Fines:** Players can pay a fee to be released early.
        *   **Jailbreak:** Other players can break prisoners out of jail.
*   **Death & Rebirth:**
    *   **Loot Drop:** On death, a player drops **all** gear and inventory items.
    *   **Skill Inheritance:** Players retain their learned skills and attributes on their next character, but with diminishing returns to prevent abuse.
        *   **1st Death:** 100% skill carry-over.
        *   **2nd Death:** 75% carry-over.
        *   **3rd Death:** 50% carry-over.
        *   **4th+ Death:** 25% carry-over (hard floor).

### 2.9 Diplomacy & Alliances
*   **City Alliances:** Cities can form alliances with one another.
*   **Reputation Propagation:** Committing a crime (e.g., killing a player/NPC) in one city causes the player to become hostile in that city *and* all allied cities.

### 2.10 Social & Guilds
*   **Formal Guilds:** Players can officially form guilds.
*   **Headquarters:** Guilds do not build their own HQ from scratch. Instead, they must rent existing buildings within cities to serve as their headquarters.
*   **Rental System:** Guild HQs require periodic rent payments, integrating guilds into the local city economy.

### 2.11 Communication
*   **Proximity Voice Chat:** The primary and only form of communication.
    *   **Mechanic:** Players can only hear others who are physically close to them in the game world.
    *   **No Text Chat:** There is no global or local text chat system.

### 2.12 Travel & Mounts
*   **Mounts:** Players can use mounts for transportation.
    *   **Mortality:** Mounts are not immortal; they can die.
*   **Fast Travel:** There is **NO** fast travel. Players must physically traverse the world.

### 2.13 Economy & Trade
*   **Localized Trading:** There is no global auction house or marketplace.
*   **Bulletin Boards:** Players must travel to specific cities and post sell orders on physical bulletin boards.
*   **NPC Trading:** Players can also sell items directly to NPCs in cities.
*   **Banking:**
    *   **Character-Bound:** Bank storage is personal to the character.
    *   **Physical Location:** Items stored in a bank are physically located in that city.
    *   **Risk:** If a city is destroyed, all items stored in its bank are lost permanently.

### 2.14 Survival Mechanics
*   **Vitals:** Players must manage Hunger and Thirst.
*   **Temperature:** Environmental temperature affects the player.
*   **Clothing:** Players must wear appropriate clothing for the climate to avoid negative effects (e.g., warm clothes for snow, light clothes for desert).

### 2.15 Enemy Hierarchy & PvE
*   **Static Power:**
    *   **No Level Scaling:** Enemies do not scale with the player. A wolf is always a wolf; a dragon is always a dragon.
    *   **Progression Indicator:** The environment itself tells the story of progression. Players naturally move from safe zones to dangerous ones as they grow stronger.
*   **Dynamic Respawn System:**
    *   **No Fixed Timers:** Mobs do not respawn on a set timer (e.g., every 5 minutes).
    *   **Finite Populations:** Clearing a cave of goblins removes them from that location until a new group naturally migrates there.
    *   **Migration:** New mob populations must physically travel or migrate to repopulate an area, making the world feel alive and reactive.
*   **Dynamic Ecology:**
    *   **Mutation:** All mob populations have a chance to mutate. These mutations create unique individuals with distinct stats and abilities.
    *   **Defense Against Extinction:** Active, aggressive hunting of a specific mob population **increases** the likelihood of mutation. The species reacts to the threat by spawning stronger defenders.
    *   **Mutation Acceleration:** High-pressure environments (continuous extermination) can cause mutations to spiral, leading to multiple Area or Region bosses spawning simultaneously. This requires exponentially larger player forces to contain.
    *   **Ecological Triggers:** Mutations can also be triggered by indirect player actions, such as tampering with food sources or altering the local ecology, forcing mobs to adapt to survive.
    *   **Adaptive Evolution:** Mutated mobs do not just get stronger stats; they genetically adapt to specific threats.
        *   *Example:* If a guild of Fire Mages hunts goblins, the goblin bosses will evolve Fire Resistance.
        *   *Iterative Learning:* If players bring more reinforcements to kill an adapted boss, the *next* generation of bosses will evolve to counter those new threats as well.
    *   **Unique Bosses:** Because they are born from mutation, all bosses (even lower tier ones) are unique.
*   **Mob Psychology & Adaptation:**
    *   **Generational Learning (Low Intelligence):** Mobs like wolves learn from interactions over generations.
        *   **Avoidance:** If players hunt them excessively, future generations will instinctively flee upon seeing a player.
        *   **Domestication:** Conversely, positive or neutral interactions over generations can lead to species domestication.
    *   **The Boogeyman Effect (High Intelligence):** Intelligent mobs (e.g., Goblins, Orcs) recognize individual threats.
        *   **Reputation:** A player who kills enough of a specific faction or their leaders becomes a known "Boogeyman" to that species.
        *   **Reaction:** Upon seeing this specific player, intelligent mobs may flee in terror, surrender, or prioritize targeting them above all others.
*   **Tier 0: Area Bosses**
    *   **Origin:** Born from local mob populations via standard mutation.
    *   **Scope:** Local threat (e.g., a specific cave or field).
    *   **Difficulty:** Stronger than average mobs, challenging for solo players but manageable.
*   **Tier 1: Region Bosses**
    *   **Origin:** Born from extreme mutation or prolonged survival of an Area Boss.
    *   **Scope:** Tied to a specific local region (e.g., a forest, a mountain range).
    *   **Impact:** Minor, localized impact on the region. The world largely continues as normal.
    *   **Difficulty:** Impossible for a single player. Requires a full party or a small guild raid to defeat.
    *   **Mechanics:** Standard raid mechanics; does not require the complex server-wide quest chains of higher tiers.
*   **Tier 2: Continental Bosses**
    *   **Scope:** Tied to a specific continent.
    *   **Impact:** Direct impact is localized to the continent (e.g., weather, terrain). Indirect global impact via NPC refugees and trade disruption.
    *   **Mechanics:** Similar to World Bosses (active threat, strategic quests) but scaled down for regional coordination.
*   **Tier 3: World Bosses (The Calamities)**
    *   **Permanent World Alteration:** The world is forever changed after a world boss event. It never reverts to its previous state (e.g., a lush forest becomes a permanent wasteland).
    *   **Active Threat:** World bosses do not wait passively in dungeons. They actively invade the server, altering the environment and impacting quests/NPCs globally.
    *   **Server-Wide Coordination:** Defeating a world boss requires the cooperation of the entire server population, not just a single party.
    *   **Strategic Quest Chains:**
        *   Bosses cannot be defeated by simple damage. Players must complete a series of unique, non-repeatable quests to weaken the boss or buff the players (e.g., "Destroy the Siege Engine" or "Purify the Water Source").
        *   **First-Come, First-Served:** Once a party completes one of these strategic quests, it is completed for the server and disappears. This prevents farming and forces diverse contributions.
    *   **Permadeath:** World bosses are one-time-only events. Once killed, they are gone forever.

### 2.16 Loot & Crafting System
*   **Deterministic Loot & Carving:**
    *   **Harvesting:** There are **NO RNG drops** for gear or major components. Instead, players must physically carve/harvest specific parts (e.g., dragon scales, head, poison sacs) from defeated enemies.
    *   **Carving Skill:** Carving is a dedicated skill separate from crafting. Harder parts (e.g., intact dragon heart vs. simple hide) require higher skill levels.
    *   **NPC Carvers:** Players can hire NPC specialists to carve corpses for them. These NPCs follow the same hierarchy (Apprentice to Grandmaster) and discovery mechanics as craftsmen.
*   **Logistics & Transport:**
    *   **Physicality:** Loot (especially large carcasses) is physically present in the world and has weight/bulk. It does not magically disappear into an inventory.
    *   **Transport Planning:** Players must plan how to move a kill *before* they hunt.
    *   **Scaling:**
        *   **Small/Medium:** Can be carried by a player's mount.
        *   **Large/Colossal:** Requires multiple players to carry or pre-arranged heavy transport (e.g., wagons, ships, hired transport services).
*   **Decay & Spoilage:**
    *   **Natural Decay:** Dropped items and creature carcasses do not persist indefinitely. They are subject to natural decay mechanics.
        *   **Carcasses:** Will rot and spoil over time, rendering them useless for harvesting high-quality materials.
        *   **Gear:** Dropped weapons and armor left in the world will rust and accumulate damage, eventually becoming scrap.
    *   **Time Pressure:** This adds a layer of urgency to logistics. Players must transport their kills to a city or preservation facility before the resources spoil.
*   **Crafting-Only Gear:**
    *   **No Weapon Drops:** Players do not find finished swords or armor on bodies. All gear must be crafted using harvested materials.
*   **Craftsman Hierarchy:**
    *   **Player Progression:** Players can level up their own Crafting or Carving skills to reach Grandmaster status.
    *   **NPC Hierarchy:** To craft high-tier items without personal skill, players must find a specific NPC craftsman.
    *   **Tiers:**
        1.  **Apprentice**
        2.  **Journeyman**
        3.  **Expert**
        4.  **Master**
        5.  **Grandmaster**
*   **Risk & Failure:**
    *   **No Hard Gate:** The system does not prevent low-level players from attempting to carve or craft high-level resources.
    *   **Consequence:** Attempting to carve or craft above one's skill level results in **failure**, destroying the valuable resources and producing "junk" items instead.
*   **Discovery Quest Chain:**
    *   **Scavenger Hunt:** High-tier NPCs are hidden. Players must ask lower-tier NPCs for information (e.g., an Apprentice points to a Journeyman, who points to an Expert).
    *   **Map Marking:** Once a player successfully locates a Master or Grandmaster, their location is permanently marked on that player's map.
    *   **Exploration:** Finding the right smith or carver is a journey in itself.

### 2.17 Legacy & Remembrance
*   **NPC Recognition:** NPCs will remember the specific players who defeat world bosses or save towns from raids.
*   **Inscriptions:** Heroic deeds are recorded in in-game tomes and history books found in cities.
*   **Monuments:** Statues may be erected in cities to honor players who performed legendary feats.
*   **Immersive Quest Instances:**
    *   **Reactionary World:** High-stakes quests take place in specialized instances to maintain immersion (e.g., NPCs react to the danger rather than idling).
    *   **Area Locking:** During major events or boss raids, specific areas may become disabled or inaccessible to other players until the quest resolves.

### 2.18 Server Ecology & Governance
*   **Resource Depletion:** Over-harvesting by guilds or players can strip the world, turning it into a barren wasteland.
*   **Emergency Meetings:** Players or guilds can call a server-wide meeting to address the ecological crisis.
*   **Democratic Voting:** The server population votes on a course of action:
    1.  **Total Reset:** The server is wiped and reset to a pristine state. All player progress is lost.
        *   *Optional:* The vote can include banning the guilty parties from the fresh server.
    2.  **Adaptation:** The server refuses to reset and continues in the wasteland.
        *   *Consequence:* Flora and fauna adapt to the harsh conditions, making the game significantly more difficult.
*   **Reconvening:** If "Adaptation" is chosen, players can reconvene later to vote again on a reset if the majority opinion shifts.

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
*   **Infrastructure:** Quantum Computing Servers
    *   **Necessity:** Required to handle the massive complexity of dynamic world simulation, ecological decay, and persistent object tracking.
    *   **Persistence Tracking:** Quantum processing allows for the real-time tracking of millions of individual objects (carcasses, dropped items) and their decay states across the entire server.
*   **AI Engine:** Quantum-Powered Neural Networks
    *   **Mobs:** Powers the evolutionary and psychological adaptability of mobs (e.g., generational learning, developing specific resistances).
    *   **NPCs:** Enables complex memory systems for NPCs to remember specific players ("Founders", "Boogeymen") and dynamic historical events.
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
