---
name: duris-game-knowledge
description: Use whenever working on Duris MUD — connecting to the game, navigating, exploring, fighting, parsing game output, writing commands, understanding zones, combat mechanics, spellcasting, geography, equipment, mobs, recovery, or any other gameplay question. Load this skill for any task involving Duris.
---

# Duris Game Knowledge

Generalized knowledge about **Duris: Land of Bloodlust** (mud.durismud.com, port 7777).

Sources: Duris Wiki, MUDStats, Mud Connector, player guides, and live observations.

---

## Game Overview

**Duris: Land of Bloodlust.** Full-loot PvP racewar MUD founded 1995, forked from Sojourn. Massive world: 162,900+ rooms across 267 zones spanning 6+ continents. Two opposing factions fight an ongoing racewar; there are no safe rooms anywhere.

**Leveling:** 46 mortal levels + 10 epic levels (51-56). Levels 1-46 via XP from zoning, PvP frags, and quests. Levels 51-56 require organized potion-zone groups. Levels 1-25 are "newbie range" on the Good side (zone guardians and high-level mobs protect entrances). Evil races are harder from the start — reduced vision, XP penalties, and aggressive hometown mobs.

**Character progression** is heavily dependent on two things: levels and equipment. Getting either one requires time and risk.

**Information model:** Duris often teaches mechanics through room descriptions, item descriptions, hints, NPC/player dialogue, and combat flavor text. Treat descriptive text as mechanical evidence, not flavor to skim past.

**Full loot:** On death, your corpse and all equipped/carried items can be looted by anyone. This is a core risk mechanic — the corpse of a powerful character is a valuable target.

**Racewar:** Good and Evil factions fight for territory and frags. When you kill an opposing faction player you earn frags and loot their corpse. When you die you lose frags and your corpse is lootable. The faction with the most frags when the cap timer expires advances.

**Multiplaying** is not allowed and is harshly punished.

---

## Races & Factions

### Good races
Human, Mountain Dwarf, Halfling, Gnome, Half-Elf, Grey Elf, Barbarian, Centaur, Storm Giant, Githzerai. Easier to play, some hometown protection, recommended for new players.

### Evil races
Orc, Troll, Ogre, Goblin, Duergar Dwarf, Drow Elf, Githyanki, Orog. Harder: reduced vision, XP penalties, aggressive hometown mobs. For experienced players.

### Neutral races
Minotaur and Thri-kreen. Can align with either faction.

### Classes (race-restricted)
- **Hitters:** Warrior, Mercenary, Paladin, Anti-Paladin, Reaver, Ranger, Monk, Berserker, Dreadlord
- **Rogues:** Assassin, Thief, Bard
- **Clerical:** Cleric, Druid, Shaman, Warlock
- **Casters:** Sorcerer, Necromancer, Conjurer, Illusionist, Alchemist
- **Telepaths:** Psionicist

---

## Geography & World Structure

### Continents & Regions
The world has multiple major landmasses connected by a graphical overhead map system:

- **Goodie Continent:** largest beginner-friendly surface. Connected to Evermeet (subcontinent, walkable terrain). Tharnadia: City of Humans is a major Goodie zone.
- **Evil Continent:** harder. More dangerous zones, fewer safe havens.
- **Underdark:** a massive, dangerous underground zone that serves as the primary connector between most surface continents. Traveling the Underdark at low level is extremely risky. Multiple entrances exist: Ashrumite, Outcast's Tower, Golden Halls, Icecrag Castle, New Cave City, Sarmiz / Sarmiz Worms, Krethik Keep, Faang, Moregeeth, Tunnels of Cyric.
- **Icecrag:** northern region with its own world map nodes and a descent into the Underdark.
- **Islands:** various islands connected by ship or world map.

### Zones vs. World Map
- A **zone** is a connected cluster of rooms written as a unit (e.g., "Tharnadia: City of Humans", "The Underdark", "Myrabolus").
- The **world map** connects zones to each other. Some zones connect directly to the world map (you enter the zone from the map); other zones connect through other zones (you walk from Zone A into Zone B).
- "Zone boundary" rooms — like **"The Gates of Myrabolus"** — mark the edge of a zone. Crossing from these rooms outward typically enters the world map.
- "A **Well Worn Path**" is a world map transition room.
- The **Underdark** is unique because it spans enormous space and links most continents, functioning as the game's main highway.

### Room Structure
Standard room output:
```
<Room Title>

<Description text...>

Obvious exits: -North -East# -South -West
```

The room title appears before the description. Exit lists appear after. Be careful not to confuse descriptive text or transient mob movements ("A pigeon leaves north.") with the room title or exit list.

Some exits are **hidden** — not shown in "Obvious exits." These may be revealed by examining objects, killing mobs, or quest progress. The game hints with language like "There appears to be something here..." but doesn't explicitly show the exit.

---

## Hometowns

Every race has a hometown. Hometowns provide:
- Basic stores (armor, weapons, food, bandages, potions)
- A doctor (for healing)
- Often a bank or storage

**Crucially:** hometowns are NOT truly safe. PvP can happen anywhere.

---

## Movement & Navigation

### How movement works
The MUD processes one command at a time. You send a direction command (`n`, `s`, `e`, `w`, `u`, `d`, or `open <dir>` for doors), wait for the response, then send the next command. Movement cadence is bounded by network latency and game state.

### Doors
The `#` marker in exit lists indicates a door:
```
Obvious exits: -North -South# -West
```
- `South#` means the south exit is a door.
- To move through a door, you must first `open south`, then `south`.
- "The door seems to be closed." means the door is currently closed — it is not a permanent wall or blocked exit. The door may open or close dynamically.

### Movement failures
| Response | Meaning |
|---|---|
| "The door seems to be closed." | Door, not wall. Open it first. |
| "You are too exhausted." | Movement points depleted. Stop and rest. |
| "You can't go that way." | Hard blocked exit. No passage. |
| "You are asleep." | Cannot move while asleep. Wake first. |
| "You are resting." | Cannot move while resting. Stand first. |
| "You are sitting." | Cannot move while sitting. Stand first. |
| "You are on your ass." | Cannot move. Stand first. |

### Hidden exits
Some exits are not listed in "Obvious exits." Discovering them requires examining objects, killing mobs, quest triggers, or special commands. There is no universal syntax — pay attention to description text.

### World map transitions
Walking off the edge of a zone typically places you on the world map. World map rooms are often named "A Well Worn Path" or similar generic overland descriptions. The map is ANSI-colored overhead graphics visible via the game's map command.

### Scan
`scan` is a scouting command. It reports mobs/players by direction and approximate distance bands ("close by", "not far off", "in the distance", "a brief walk away", "rather far off"). Use it for hunting and map inference before walking into unknown rooms. Scan output is directional evidence, not proof of room contents.

### Terrain
World-map terrain affects travel. Hills and mountains increase fatigue; flying reduces fatigue. Use `terrain` to identify terrain type. Some classes get terrain-specific benefits (Druids benefit from Forest and Field terrain).

---

## Combat

### Prompt
The combat prompt shows your position:
```
< 331h/331H 112v/112V Pos: standing >
```
HP/MV/Position in this format.

### Posture states
`standing` — ready for combat and movement.
`sitting`, `kneeling`, `resting` — cannot move. Stand first.
`sleeping` — cannot act. Must `wake` first.
`on your ass` — cannot move. Must `stand` first.

After combat ends you may be in any posture. Recovery requires checking what posture you're actually in.

### Flee mechanics
- `flee` attempts to escape combat by moving randomly.
- Each flee attempt **costs movement points**. At 0 movement, flee fails repeatedly.
- Fleeing repeatedly into a corner can trap you in combat. At 0 movement, you are helpless.
- **Loaded movement burst:** With full movement points, you can sometimes move past an aggressive mob before they trigger aggro — timing matters.
- **Flee cooldown:** Do not spam flee. After 1-2 attempts with no result, assess the situation. Immediately retrying flee at 0 movement is wasted.
- After fleeing, you often land in a random nearby room — you may still be near the enemy that was fighting you.

### Wimpy
`wimpy <hp>` sets auto-flee at a HP threshold. When HP drops below wimpy setting, the character attempts to flee automatically. This is a backup, not a primary survival strategy.

### Combat commands
- `flee` — escape randomly
- `kick`, `bash`, `backstab`, `rescue`, `retreat` — combat skills
- `wimpy` — set auto-flee HP threshold
- `consider <target>` — assess mob danger before engaging
- `look <target>` — inspect a mob's equipment and details
- `vicious` — toggle automatic finishing of incapacitated/bleeding NPCs

### Aggressive mobs
Aggressive mobs enter combat if you are in the room or within range. Some aggressive mobs wander — they may appear and disappear from rooms. A mob being in a room right now doesn't mean it always lives there.

### Assist and room-composition risk
Encounter risk is not just target risk. Guards, allies, and same-room mobs can assist a victim. Ranged pulls can aggro every mob in the target room. Sentinel mobs may refuse to leave. `consider <target>` is useful, but it can understate danger when the room composition is bad.

### Luring
Luring is an explicit tactic: hit or range a mob, retreat/flee, and fight it away from helpers or a dangerous room. It is also dangerous. Some mobs track after a flee, and wounded mobs around `pretty hurt` or worse may be less likely to continue pursuit.

### Incapacitation effects
**Stun**, **bash**, **sleep**, and other combat effects can incapacitate you. Detection:
- Sleep: prompt or text says "sleeping" or "In your dreams"
- Stun: may show as posture or explicit stun message
- Bash: you may be knocked down (check posture)

Recovery requires identifying the state and using the appropriate command (`wake` for sleep, waiting for stun to expire, etc.)

Duris distinguishes incapacitated, mortally wounded, bleeding close to death, and dead. A target may still need finishing after it is incapacitated. `vicious` can automate this for NPCs.

### Experience from combat
You gain XP from killing mobs and from PvP frags. Mob XP scales with mob level and difficulty. Group kills share XP.

### Instrumentation
The `Damage` toggle exposes numeric combat damage, useful for measuring weapon and spell effectiveness. The `Experience` toggle can expose XP gain signals. Check `toggle` when parser or training data quality matters.

---

## Spellcasting

### Spell circle system (NOT mana)
Duris uses AD&D-style spell circles, not a mana pool. Casters must:

1. **Memorize / Pray / Commune / Torpor** specific spells into spell slots
2. Cast the spell (consumes the slot)
3. Re-memorize to cast again

**Spell slots** are limited. Higher level casters have more slots across more circles. The specific method depends on class:
- Mem casters such as Mages, Conjurers, Sorcerers → `memorize`
- Clerics, Paladins → `pray`
- Druids → `commune`
- Some classes → `torpor`

### Mem-caster spellbooks
For spellbook-based mem casters, learning a spell is separate from memorizing it. The usual pipeline is:

1. Hold the spellbook.
2. Buy or obtain the spell page/practice.
3. Scribe/practice the spell into the book.
4. `memorize <spell>` to queue it into a memory slot.
5. Cast the spell, consuming the prepared slot.

The `mem` command reports both prepared spells and queued study with remaining time. Standing or acting can abandon queued memorization. `forget <spell>` removes one prepared instance at a time. Some spell-learning commands require exact or longer spell names; abbreviations that work elsewhere may fail here.

### Spell failure
Spells can fail if the caster is distracted, hit during casting, in combat noise, or otherwise interrupted. Recovery requires re-memorizing.

### Casting and movement
Casting is disrupted by taking damage, moving, or most actions. Some spells require you to be stationary (sitting or resting to memorize).

### Circle progression
At level 1 you have access to circle 1 spells with 1 slot. Higher levels unlock more circles and more slots per circle. Spell choice (which spells to have memorized) is strategic — you can't have everything ready at once.

### Spell effects
Spell output can resolve in packets: one cast may show damage and also resistance/no-harm text. Cold effects can include secondary weaken/slow messages beyond raw damage. Parse spell outcomes from all lines around the cast, not a single line.

---

## Equipment & Loot

### Random equipment drops
Most mobs can drop randomly generated equipment. This equipment is often better than standard zone EQ or worse, depending on RNG. Inspect dropped items with `exam <item>`.

### Named / zone-named equipment
Some random drops have the zone name attached to the item (e.g., "Tharnadian Plate"). When you wear **3 or more pieces from the same zone**, you get zone-named set bonuses (extra HP, sometimes spell protections). Removing the items removes the bonus immediately (except if a spell was cast on you while the set was active).

**Named sets:** Wearing multiple named sets of 3+ pieces causes the bonus to cycle erratically. Don't mix incompatible named sets.

### Equipment persistence
When a mob dies and is looted, its equipment may not respawn until the MUD reboots. Equipment seen on a mob today may not be there tomorrow. Conversely, if a mob usually carries an item but currently doesn't, the mob may have been looted recently — the item will return after reboot.

### Full loot PvP
On death, your entire corpse and everything you were carrying/wearing is lootable. This applies to all items — potions, scrolls, gold, equipment, everything.

### Inventory limits and item decay
Inventory has an item-count cap as well as weight/load. Corpse recovery and loot sweeps can fail because the character cannot carry more items. Dropped ground items can decay or crumble quickly; dropping loot is not reliable storage.

### Exam and attributes
`exam <item>` can reveal type, source/zone text, abilities, flags, armor class, stat effects, value, material, and quality. Equipment value is multidimensional; shop value alone is not a safe proxy for usefulness.

`attribute` exposes derived stats beyond base attributes: armor damage reduction, saving throws, spell damage modifier, spell damage reduction, carry capacity, regeneration, and related effects. Charisma affects store prices and pet obedience.

---

## Mobs & Profiling

### Consider
`consider <target>` returns a danger assessment — typically text like "easy", "hard", "impossible" or similar language. This is the primary way to evaluate whether a mob is worth fighting.

### Look
`look <target>` shows what a mob is wearing, wielding, and carrying. This tells you:
- Equipment value (can they drop good loot?)
- Class indicators (a mob with a shield + mace may be a cleric-type)
- Any quest-relevant items

### Mob wandering
Many mobs move between rooms. A mob being in a room right now is a **sighting**, not proof it lives there. Mob locations change over time.

### Mob identity
A mob's visible name (e.g., "a myrabolan guard") can refer to multiple distinct mobs at different levels within the same zone. The same visible name can have different power levels. Consider results help distinguish.

### Mob equipment as evidence
- **CarriedNow:** this mob instance currently shows this item (from `look`)
- **KnownLoadout:** this mob type has carried this item in the past
- **Absence:** if a mob usually carries an item but currently doesn't, it was likely looted — absence is evidence, not proof the item is gone permanently

---

## Recovery & Survival

### When low on HP
- **Sleep / rest** until HP regenerates
- Find a **healing fountain, basin, or temple** in the zone
- Visit a **doctor** in a hometown
- Use **potions, bandages**, or healing spells if available

### When low on movement
Movement points regenerate faster when stationary. Stop moving and wait. Sitting and resting both regen movement (but prevent movement until you stand).

### Death recovery
Death is a workflow, not just a failure state. After death, the character may return to the menu; re-entering can resume at very low HP while the corpse remains lootable. A recovery protocol must handle menu entry, low-HP safety, corpse looting, item-count limits, dropped-item decay, and disrupted group/follow state.

### Rent and camping
Camping is location-dependent; some town/road locations direct you to an inn instead. Renting at an inn stores carried possessions, disbands group state, and returns to the menu.

### Posture recovery
| Current state | Action needed |
|---|---|
| `sleeping` | `wake` first, then `stand` |
| `sitting`, `kneeling`, `on your ass` | `stand` directly |
| `resting` | `stand` directly |
| `standing` | ready for action |

### Finding safe spots
Each zone typically has one or more rooms with healing mechanisms (fountains, basins, temples). These are valuable recovery locations and worth noting when exploring a new zone.

---

## Zones & Exploration

### Zone classification by level
- **Newbie zones** (1-15ish): Goodie Continent surface zones near hometowns. Zone guardians protect entrances.
- **Mid zones** (15-30ish): More dangerous, better XP and loot.
- **High zones** (30+): Dangerous solo play. Grouping strongly recommended.
- **Epic zones** (47+): Require organized groups for potion attempts.

### Zone boundaries
Some zones are isolated; others connect through shared rooms or world map nodes. The Underdark is the primary connector between continents.

### Zone types
- **City zones:** Shops, banks, doctors, guildhalls. Generally safe for leveling.
- **Dungeon zones:** Combat-focused, mob-dense, risk/reward.
- **Epic zones:** Hard group content for epic level progression.
- **World map:** Overland travel between continents. Mostly empty but PvP can happen.

### Credits command
`credits` shows a (semi-complete) list of zones on the MUD. Useful for finding new areas to explore.

### Boons
Boons are timed global reward windows: zone XP bonuses, kill bounties, epic rewards, or similar server-wide incentives. Check active boon state before choosing a grind target; optimal XP/reward play can shift while a boon is active.

### Quest tracking
Quest tracking is often manual. Durable state must be reconstructed from NPC dialogue, proof items, corpse/room search results, and remembered objectives rather than relying on a modern quest journal.

---

## Grouping & Social Play

### Follow and groups
Group formation requires follow plus consent, often abbreviated by players as `f/c`. `gsay` only works while grouped. Death and renting can disband or disrupt group/follow state.

### Social learning
Player advice is a major information channel. Duris veterans often teach terse command idioms and tactics in-character. Ask concise, human-like questions when stuck, and capture the answer as high-value game knowledge.

---

## Parser Patterns (from live observation)

These are concrete text patterns useful for building parsers:

| Pattern | Meaning |
|---|---|
| `< 331h/331H 112v/112V Pos: standing >` | HP/MV/Position prompt |
| `Obvious exits: -North -East# -South` | Room with door marker (`#`) on East |
| `A guard is here.` | Mob actor/sighting line |
| `You are already awake...` | Wake attempted while not asleep |
| `In your dreams` | Cannot act — character is asleep |
| `The door seems to be closed.` | Door, not wall — open it |
| `You are too exhausted.` | 0 movement — stop and rest |
| `You can't go that way.` | Hard blocked exit |
| `The Gates of Myrabolus` | Zone boundary marker |
| `A Well Worn Path` | World map transition |
| `A Bend in the Wall Road` | Normal road room (Tharnadia example) |
| `Reconnecting.` | Session reconnect |
| `q` warning requiring `quit` | Accidental one-letter quit is protected |
| `mem` with seconds remaining | Spell is queued for memorization |
| `You abandon your studies.` | Memorization queue was interrupted |
| `gsay` reports not grouped | Character is not currently in a group |
| `scan` direction + distance text | Scouting evidence, not current room contents |

### Command timing
The MUD processes commands through stateful, interruptible workflows. Memorization, camping/renting, recovery, following, and combat can all be disrupted by poorly timed actions. For automation, avoid spammy command queues and wait for state-confirming output before the next risky command.

---

## Sources

- Duris Wiki: duris.fandom.com
- MUDStats.com / TopWebGames Duris listings
- Duris Fandom pages: Spell System, Racewar, Guides, FAQ
- Mud Connector Duris guides and newbie context
- Player guides: Experience Strategy, River Navigation, Understanding Magic Shields
