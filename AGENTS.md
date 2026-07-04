# AGENTS.md — Ratacat's Skills

Contributor contract for this repository. A skill is only legitimately "in" the repo when it passes every gate below.

## Naming

One skill has exactly one handle. For a skill named `<name>`, these must be identical strings:

1. The directory name `skills/<name>/`.
2. `name` in `skills/<name>/SKILL.md` YAML frontmatter.
3. `name` of the generated entry in `.claude-plugin/marketplace.json`.
4. The install handle: `/plugin install <name>@ratacats-skills` and `npx skills add … --skill <name>`.

## Gates

Every skill must have:

1. **Canonical skill** — `skills/<name>/SKILL.md` with frontmatter `name`, `description`, `metadata.category`, non-empty `metadata.keywords`, and `metadata.blurb` (one plain-language sentence; it becomes the root README table row). `description` is the agent trigger — write it for skill routing, not for humans; `blurb` is for humans.
2. **README** — `skills/<name>/README.md`: what it does, good fits, install commands, real setup requirements only.
3. **No symlinks** — every file under `skills/` is real.
4. **Generated index** — `.claude-plugin/marketplace.json` and the root `README.md` skills table are generated. Never hand-edit generated blocks.
5. **No plugins tree** — `plugins/` must not exist.

Run `bun scripts/sync.ts` after any skill change. Run `bun scripts/sync.ts --check` before committing.

## Removing a skill

Delete `skills/<name>/`, then run `bun scripts/sync.ts`.

## CI

`.github/workflows/check.yml` runs `bun scripts/sync.ts --check` on every push and PR.
