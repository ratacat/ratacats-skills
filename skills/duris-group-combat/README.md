# Duris Group Combat

This skill helps an agent reason about group fights in Duris: Land of Bloodlust, a full-loot PvP racewar MUD where bad combat decisions can cost gear, corpses, and group position. It assumes `duris-game-knowledge` for the game's prompt, posture, spell, flee, aggro, and tracking rules.

Use it when several characters, roles, targets, and risks are moving at once. It binds live names to roles, prioritizes survival interrupts over routine actions, and keeps the agent from spamming commands or inventing unsafe targeted spell syntax.

Good fits:

- Designing group combat behavior
- Parsing a fight log with tanks, enemies, and adds
- Choosing assist, rescue, pet, heal, or caster actions
- Handling caster readiness and spent spell slots
- Preventing duplicate casts, panic flee loops, and chat spam

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill duris-group-combat

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install duris-group-combat@ratacats-skills
```
