# AGENTS.md — Ratacat's Skills

Contributor contract for this repository. A skill is only legitimately "in" the repo when it passes every gate below. These are enforced by review (no script yet).

## Naming

One skill has exactly one handle. For a skill named `<name>`, these four must be identical strings:

1. The directory name `plugins/<name>/` and `skills/<name>/`.
2. `name` in `plugins/<name>/.claude-plugin/plugin.json`.
3. `name` of the entry in `.claude-plugin/marketplace.json`.
4. `name` in the `SKILL.md` YAML frontmatter.

The frontmatter `name` is the handle a user installs (`npx skills add … --skill <name>`) and the name the agent invokes. Drift here means the skill installs under a name nobody can predict.

## Gates

Every skill must have:

1. **Plugin manifest** — `plugins/<name>/.claude-plugin/plugin.json` with `name`, `description`, and `author`.
2. **Canonical SKILL.md** — `plugins/<name>/skills/<name>/SKILL.md` with YAML frontmatter containing `name` (per Naming) and `description`. This is the single source of truth for the skill body.
3. **GitHub page** — `skills/<name>/` containing:
   - `README.md` — a real file: the human-facing landing page.
   - `SKILL.md` and every helper file/dir — symlinks into `../../plugins/<name>/skills/<name>/`. No duplicated real files.
4. **Marketplace entry** — registered in `.claude-plugin/marketplace.json` with `source: ./plugins/<name>`, plus `description`, `version`, `category`, `keywords`.
5. **README row** — a row in the `## Skills` table of the root `README.md`, linking to `skills/<name>/`.
6. **Installable two ways** — resolves via `/plugin install <name>` (marketplace) and `npx skills add ratacat/ratacats-skills --skill <name>` (skills.sh).
7. **Bijection** — exactly one `plugins/<name>` for each `skills/<name>` and vice versa. No orphan pages, no unlisted plugins.

## Removing a skill

Delete all four surfaces together: `plugins/<name>/`, `skills/<name>/`, its `marketplace.json` entry, and its `README.md` row. Leaving any one behind breaks the bijection (gate 7).

## Adding the gates to CI later

When this is automated, write the validator in Bun / TypeScript (zero npm deps, single file). It should fail on any gate violation and regenerate the `README.md` skills table from each `SKILL.md` frontmatter so the index cannot drift.
