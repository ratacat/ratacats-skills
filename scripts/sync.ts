import { existsSync, lstatSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

interface SkillMetadata {
  category?: string;
  keywords?: string[];
  blurb?: string;
}

interface SkillFrontmatter {
  name?: string;
  description?: string;
  metadata?: SkillMetadata;
}

interface SkillEntry {
  name: string;
  description: string;
  category: string;
  keywords: string[];
  blurb: string;
}

const root = path.resolve(import.meta.dirname, "..");
const check = process.argv.includes("--check");
const skillsDir = path.join(root, "skills");
const marketplacePath = path.join(root, ".claude-plugin", "marketplace.json");
const readmePath = path.join(root, "README.md");
const errors: string[] = [];

function fail(message: string) {
  errors.push(message);
}

function exitWithErrors() {
  if (errors.length === 0) return;
  console.error(errors.join("\n"));
  process.exit(1);
}

function scalar(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    try {
      return JSON.parse(trimmed);
    } catch {
      return trimmed.slice(1, -1);
    }
  }
  if (trimmed.startsWith("'") && trimmed.endsWith("'")) return trimmed.slice(1, -1);
  return trimmed;
}

function frontmatterFor(skillPath: string): SkillFrontmatter {
  const text = readFileSync(skillPath, "utf8");
  if (!text.startsWith("---\n")) {
    fail(`${path.relative(root, skillPath)} is missing YAML frontmatter`);
    return {};
  }

  const end = text.indexOf("\n---", 4);
  if (end === -1) {
    fail(`${path.relative(root, skillPath)} has unterminated YAML frontmatter`);
    return {};
  }

  const frontmatter: SkillFrontmatter = {};
  const lines = text.slice(4, end).split("\n");
  let activeTopKey: "name" | "description" | undefined;
  let activeMetadataKey: "keywords" | undefined;
  let inMetadata = false;

  for (const line of lines) {
    const top = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (top) {
      const key = top[1];
      const value = top[2];
      inMetadata = key === "metadata";
      activeMetadataKey = undefined;
      activeTopKey = undefined;

      if (key === "name" || key === "description") {
        frontmatter[key] = scalar(value);
        activeTopKey = key;
      } else if (key === "metadata") {
        frontmatter.metadata ??= {};
      }
      continue;
    }

    if (activeTopKey && /^\s+\S/.test(line)) {
      frontmatter[activeTopKey] = `${frontmatter[activeTopKey] ?? ""} ${line.trim()}`.trim();
      continue;
    }

    if (!inMetadata) continue;

    const category = line.match(/^  category:\s*(.*)$/);
    if (category) {
      frontmatter.metadata ??= {};
      frontmatter.metadata.category = scalar(category[1]);
      activeMetadataKey = undefined;
      continue;
    }

    const blurb = line.match(/^  blurb:\s*(.*)$/);
    if (blurb) {
      frontmatter.metadata ??= {};
      frontmatter.metadata.blurb = scalar(blurb[1]);
      activeMetadataKey = undefined;
      continue;
    }

    if (/^  keywords:\s*$/.test(line)) {
      frontmatter.metadata ??= {};
      frontmatter.metadata.keywords = [];
      activeMetadataKey = "keywords";
      continue;
    }

    const keyword = line.match(/^    -\s*(.*)$/);
    if (activeMetadataKey === "keywords" && keyword) {
      frontmatter.metadata ??= {};
      frontmatter.metadata.keywords ??= [];
      frontmatter.metadata.keywords.push(scalar(keyword[1]));
    }
  }

  return frontmatter;
}

function walkForSymlinks(dir: string): string[] {
  if (!existsSync(dir)) return [];
  const found: string[] = [];
  const stat = lstatSync(dir);
  if (stat.isSymbolicLink()) return [dir];
  if (!stat.isDirectory()) return found;

  for (const entry of readdirSync(dir)) {
    found.push(...walkForSymlinks(path.join(dir, entry)));
  }
  return found;
}

function skillEntries(): SkillEntry[] {
  if (!existsSync(skillsDir)) {
    fail("skills/ directory is missing");
    return [];
  }

  const dirs = readdirSync(skillsDir)
    .filter((name) => lstatSync(path.join(skillsDir, name)).isDirectory())
    .sort((a, b) => a.localeCompare(b));

  const symlinks = walkForSymlinks(skillsDir);
  for (const symlink of symlinks) fail(`${path.relative(root, symlink)} must not be a symlink`);

  if (existsSync(path.join(root, "plugins"))) fail("plugins/ directory must not exist");

  return dirs.flatMap((dirName) => {
    const dir = path.join(skillsDir, dirName);
    const skillPath = path.join(dir, "SKILL.md");
    const readmePath = path.join(dir, "README.md");

    if (!existsSync(skillPath)) fail(`skills/${dirName}/SKILL.md is missing`);
    if (!existsSync(readmePath)) fail(`skills/${dirName}/README.md is missing`);
    if (!existsSync(skillPath)) return [];

    const frontmatter = frontmatterFor(skillPath);
    const name = frontmatter.name?.trim() ?? "";
    const description = frontmatter.description?.trim() ?? "";
    const category = frontmatter.metadata?.category?.trim() ?? "";
    const keywords = frontmatter.metadata?.keywords?.map((keyword) => keyword.trim()).filter(Boolean) ?? [];
    const blurb = frontmatter.metadata?.blurb?.trim() ?? "";

    if (!name) fail(`skills/${dirName}/SKILL.md frontmatter name is required`);
    if (!description) fail(`skills/${dirName}/SKILL.md frontmatter description is required`);
    if (name && name !== dirName) fail(`skills/${dirName}/SKILL.md frontmatter name must equal directory name`);
    if (!category) fail(`skills/${dirName}/SKILL.md metadata.category is required`);
    if (keywords.length === 0) fail(`skills/${dirName}/SKILL.md metadata.keywords is required`);
    if (!blurb) fail(`skills/${dirName}/SKILL.md metadata.blurb is required (one plain-language sentence for the README table)`);

    if (!name || !description || !category || keywords.length === 0 || !blurb) return [];
    return [{ name, description, category, keywords, blurb }];
  });
}

function marketplace(entries: SkillEntry[]): string {
  return `${JSON.stringify({
    name: "ratacats-skills",
    owner: {
      name: "Jared Smith",
      url: "https://github.com/ratacat",
    },
    metadata: {
      description: "Claude and Codex skills authored or locally maintained by Ratacat.",
    },
    renames: {
      tdd: null,
    },
    plugins: entries.map((entry) => ({
      name: entry.name,
      source: `./skills/${entry.name}`,
      strict: false,
      skills: ["./"],
      description: entry.description,
      category: entry.category,
      keywords: entry.keywords,
      author: {
        name: "Jared Smith",
        url: "https://github.com/ratacat",
      },
      license: "MIT",
    })),
  }, null, 2)}\n`;
}

const CATEGORY_ORDER = ["developer tools", "prediction markets", "tools", "writing", "games", "art"];

function skillTable(entries: SkillEntry[]): string {
  const categories = [...new Set(entries.map((entry) => entry.category))].sort((a, b) => {
    const ai = CATEGORY_ORDER.indexOf(a);
    const bi = CATEGORY_ORDER.indexOf(b);
    return (ai === -1 ? CATEGORY_ORDER.length : ai) - (bi === -1 ? CATEGORY_ORDER.length : bi) || a.localeCompare(b);
  });

  const sections = categories.map((category) => {
    const rows = entries
      .filter((entry) => entry.category === category)
      .map((entry) => `| [\`${entry.name}\`](skills/${entry.name}/) | ${entry.blurb.replace(/\|/g, "\\|")} |`);
    const header = category.replace(/\b[a-z]/g, (c) => c.toUpperCase());
    return [`### ${header}`, "", "| Skill | What it does |", "| --- | --- |", ...rows].join("\n");
  });

  return ["<!-- skills:start -->", ...sections.join("\n\n").split("\n"), "<!-- skills:end -->"].join("\n");
}

function readme(entries: SkillEntry[]): string {
  const current = readFileSync(readmePath, "utf8");
  const sectionStart = current.indexOf("## Skills\n");
  if (sectionStart === -1) {
    fail("README.md is missing a ## Skills section");
    return current;
  }

  const nextSection = current.indexOf("\n## ", sectionStart + 1);
  const sectionEnd = nextSection === -1 ? current.length : nextSection;
  const section = `## Skills\n\n${skillTable(entries)}\n`;
  return `${current.slice(0, sectionStart)}${section}${current.slice(sectionEnd)}`;
}

function writeOrCheck(filePath: string, next: string) {
  const current = existsSync(filePath) ? readFileSync(filePath, "utf8") : "";
  if (check) {
    if (current !== next) fail(`${path.relative(root, filePath)} is stale; run bun scripts/sync.ts`);
    return;
  }

  mkdirSync(path.dirname(filePath), { recursive: true });
  if (current !== next) writeFileSync(filePath, next);
}

const entries = skillEntries();
exitWithErrors();

const nextMarketplace = marketplace(entries);
const nextReadme = readme(entries);
exitWithErrors();

writeOrCheck(marketplacePath, nextMarketplace);
writeOrCheck(readmePath, nextReadme);
exitWithErrors();
