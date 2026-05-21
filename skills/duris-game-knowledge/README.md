# Duris Game Knowledge

This skill gives the agent a working map of Duris: the MUD, the world, the combat loop, the danger, and the little rules that matter when commands become real.

Use it for anything involving Duris: navigation, zones, classes, spellcasting, equipment, recovery, fighting, parsing prompts, or writing helper commands. It is the general background skill that keeps the agent from treating Duris like a normal game with safe assumptions.

Duris is old, sharp-edged, and full of risk. A wrong move can mean death, lost gear, wasted prep, or a messy walk back. This skill helps the agent reason with the game's actual texture.

Good fits:

- Understanding live game output
- Planning a route or recovery
- Explaining mechanics
- Designing MUD automation
- Pairing with `duris-group-combat`

Use this before making Duris decisions that touch movement, combat, spells, or equipment. Do not invent commands, exits, or safe paths when live output is ambiguous.
