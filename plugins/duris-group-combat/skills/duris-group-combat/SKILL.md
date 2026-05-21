---
name: duris-group-combat
description: Use when designing or operating Duris group combat with tanks, assists, assumed targets, caster memorization readiness, bash risk, tracking enemies, aggro adds, or command spam risk.
---

# Duris Group Combat

## Overview

Duris group combat is role-based. The controlled character may be any class; bind live names to roles, then reason with `self`, `tank`, `leader`, `enemy`, and `add`.

**REQUIRED BACKGROUND:** Use `duris-game-knowledge` for Duris prompt, posture, memorization, flee, aggro, tracking, and spell mechanics.

## Priority Order

1. Survival interrupts: self tanking, tank gone, self disabled, lethal HP, hostile add on self.
2. Command pacing: prevent duplicate casts, repeated offense, flee spam, and chat spam.
3. Role action: assist, targetless cast, rescue, order follower, heal, attack.
4. Communication: concise status the group can act on.

Survival interrupts are not spam. If `T:` becomes `self` during a cast, do not wait for spell resolution; send one survival command now and parse the result.

## Required Output Shape

When designing from named logs, use this structure:

```markdown
# Duris Group Combat Behavior

## Role Bindings
| Role | Binding |
|---|---|
| self | <controlled character> |
| tank | <designated or prompt tank> |
| leader | <caller/mover> |
| enemy | prompt E after assist |

## Priority
survival interrupts > command pacing > role action > communication

## States
...
```

After the binding table, use role names. Do not put character names in headings, state names, or reusable rules.

## Hard Stops

Reject any design that does these:

| Bad pattern | Correct pattern |
|---|---|
| Says `mana`, `OOM`, or `out of mana` for a Duris mem caster | Say `not memmed`, `out of memorized spells`, or `spell slots spent`. |
| Treats queued `mem` study as ready | Ready means memorized and usable now. |
| Uses `cast '<spell>' <enemy>`, `<target>`, or `$target` after assist/prompt target exists | Use a targetless current-target command or configured alias, such as `mm`, when known. |
| Defers flee/retreat/rescue because a cast is in progress | Survival interrupts override `castLock`. |
| Repeats `flee` every prompt | Send one escape command, wait for the result, then reassess. |
| Invents syntax like `flee east` or `grouptell` | Use known commands only, such as `gsay` if grouped, or describe communication intent. |
| Announces every assist, cast, and spell result | Communicate readiness and danger, not routine rotation. |

## Core State Model

| State | Rule |
|---|---|
| `preflight` | Confirm target, tank, route risk, and readiness. Casters must report whether key spells are memorized. |
| `assist` | When tank engages or caller says go, use `assist <tank>` if target acquisition is needed. |
| `engaged` | Prompt shows stable tank and enemy. Role action may proceed. |
| `casting` | A spell has started. Block added offense and chatter, but not survival interrupts. |
| `tank-loss` | Self is tanking, tank is absent/down/sitting at dangerous time, or tank was forced out. Stop offense. |
| `add-danger` | Extra hostile attacks self or destabilizes room. Do not retarget merely because something entered. |
| `escape` | Send one survival command, wait for result, then evaluate movement, enemies, and route. |
| `recover` | Rejoin, heal, mem/med, or report not ready. Do not auto re-engage. |

## Targeting

The tank owns target selection. The controlled character acquires target by assist or by a prompt enemy already tied to the tank. A wandering arrival is just an arrival until it attacks self, attacks the tank, or the tank/caller clearly picks it up.

After assist/current target exists, prefer targetless current-target commands. Store the enemy name as evidence for communication and logs, not as a spell argument.

## Readiness Communication

Before planned combat, clarify:

| Topic | Meaning |
|---|---|
| target | Which enemy the tank will engage first. |
| tank | Who or what should hold aggro: player, pet, follower, charm. |
| readiness | Whether each critical role can act now. |
| caster mem | Which key spells are memorized now, not queued. |

During combat, communicate only actionable changes: `not ready`, `out of spells`, `self tanking`, `tank down`, `separated`, `add on me`, `fled`, `need rescue`.

## Role Notes

Casters: do not cast while sitting, resting, sleeping, or on your ass. Use memorized slots only. If exact targetless syntax is unknown, say `configured targetless spell command`; do not invent a targeted spell command.

Pet handlers: use pets/followers to establish or restore tanking before personal offense.

Tanks/hitters: establish target clearly. If a weaker group member becomes tank, rescue or retank before maximizing damage.

## Fleeability

`fleeable` includes movement points, posture, known exits, doors, route safety, whether flee goes deeper into danger, tank separation, enemy condition, and tracking evidence. Duris `flee` is random; directed movement belongs after flee succeeds and combat state allows movement.
