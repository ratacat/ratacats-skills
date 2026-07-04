# Duris Game Knowledge

This skill gives an agent a working map of Duris: Land of Bloodlust, a full-loot PvP racewar MUD at `mud.durismud.com:7777`. Duris has old-school command parsing, dangerous travel, corpse looting, spell memorization, and no truly safe rooms.

Use it for anything involving Duris: navigation, zones, classes, spellcasting, equipment, recovery, fighting, parsing prompts, or writing helper commands. The skill keeps the agent from treating Duris like a modern game with safe assumptions, invented commands, or forgiving retries.

Good fits:

- Understanding live game output and prompt text
- Planning a route, recovery, or exploration pass
- Explaining combat, spells, equipment, racewar, or loot risk
- Designing MUD automation around real parser patterns
- Pairing with `duris-group-combat` for party fights

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill duris-game-knowledge

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install duris-game-knowledge@ratacats-skills
```
