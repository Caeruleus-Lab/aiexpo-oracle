# Oracle skill `project`: the full skill

> For the AI: /project = clone and track outside repos. In a chat it works partly in a chat: run what the chat can do; files it would write are shown for the person to save, and they are gone in the next chat unless saved. The full version needs Claude Code or Codex.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 14 files.

<!-- file: project/SKILL.md -->
### File: `project/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: project
description: '[core] v26.8.23-alpha.2112 G-SKLL | Clone and track external repos. Use when user shares a GitHub URL to study or develop, or says "search repos", "find repo", "where is [project]". For active development, use /incubate.'
argument-hint: "<github-url> | search <query>"
---

# project-manager

Track and manage external repos: Learn (study) | Incubate (develop)

## Golden Rule

**ghq owns the clone → ψ/ owns the symlink**

Never copy. Always symlink. One source of truth.

## When to Use

Invoke this skill when:
- User shares a GitHub URL and wants to study/clone it
- User mentions wanting to learn from a codebase
- User wants to start developing on an external repo
- Need to find where a previously cloned project lives

## Step 0 — Anchor (date-stamp + root)

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"

# Find oracle root — git toplevel that has CLAUDE.md + ψ/
ORACLE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$ORACLE_ROOT" ] && [ -f "$ORACLE_ROOT/CLAUDE.md" ] && { [ -d "$ORACLE_ROOT/ψ" ] || [ -L "$ORACLE_ROOT/ψ" ]; }; then
  PSI="$ORACLE_ROOT/ψ"
elif [ -f "$(pwd)/CLAUDE.md" ] && { [ -d "$(pwd)/ψ" ] || [ -L "$(pwd)/ψ" ]; }; then
  ORACLE_ROOT="$(pwd)"
  PSI="$ORACLE_ROOT/ψ"
else
  echo "⚠️ Not in oracle repo (no CLAUDE.md + ψ/ at git root). Writing to pwd."
  ORACLE_ROOT="$(pwd)"
  PSI="$ORACLE_ROOT/ψ"
fi
```

## Actions

### learn [url|slug]

Clone repo for **study** (read-only reference).

```bash
# 1. Clone via ghq
ghq get -u https://github.com/owner/repo

# 2. Create org/repo symlink structure
GHQ_ROOT=$(ghq root)
mkdir -p "$PSI/learn/owner"
ln -sf "$GHQ_ROOT/github.com/owner/repo" "$PSI/learn/owner/repo"
```

**Output** (announce-mode — absolute path):

# announce-mode → absolute path (no ψ/, no ~/, no $VAR, no ...).
# Use:  echo "marker: $RESOLVED_PATH"  — bash substitutes. See CONVENTIONS.md.

```bash
LINK="$PSI/learn/owner/repo"
echo "✅ Linked: $LINK"
```

### incubate — REDIRECTS TO /incubate

> **`/project incubate` is now `/incubate`.**
> If the user says `/project incubate [args]`, run `/incubate [args]` instead.
> Do NOT execute incubate logic here — invoke the standalone `/incubate` skill with the same arguments.

### find [query]

Search for project across all locations:

```bash
# Search ghq repos
ghq list | grep -i "query"

# Search learn/incubate symlinks (org/repo structure)
find "$PSI/learn" "$PSI/incubate" -type l 2>/dev/null | grep -i "query"
```

**Output**: List matches with their ghq paths

### list

Show all tracked projects with rich metadata (#227):

```bash
echo "📦 Projects"
echo ""

# Collect all tracked repos (learn + incubate symlinks)
REPOS=()
for link in $(find "$PSI/learn" "$PSI/incubate" -name "origin" -type l 2>/dev/null | sort); do
  dir=$(dirname "$link")
  owner=$(basename "$(dirname "$dir")")
  repo=$(basename "$dir")
  type="learn"
  echo "$link" | grep -q "incubate" && type="incubate"
  REPOS+=("$owner/$repo:$type")
done

if [ ${#REPOS[@]} -eq 0 ]; then
  echo "  No tracked projects. Use /learn or /incubate to add."
else
  printf "  %-35s %-6s %-8s %-8s %s\n" "Repo" "Stars" "License" "Type" "Description"
  printf "  %-35s %-6s %-8s %-8s %s\n" "───────────────────────────────────" "──────" "────────" "────────" "──────────────────────"

  for entry in "${REPOS[@]}"; do
    slug="${entry%%:*}"
    type="${entry##*:}"
    # Fetch metadata from GitHub (cached per session)
    meta=$(gh api "repos/$slug" --jq '"\(.stargazers_count)\t\(.license.spdx_id // "none")\t\(.description // "-" | .[0:40])"' 2>/dev/null || echo "?\tnone\t-")
    stars=$(echo "$meta" | cut -f1)
    license=$(echo "$meta" | cut -f2)
    desc=$(echo "$meta" | cut -f3)
    printf "  %-35s %-6s %-8s %-8s %s\n" "$slug" "⭐$stars" "$license" "$type" "$desc"
  done
fi

echo ""
echo "  Total: ${#REPOS[@]} tracked repos"
```

## Directory Structure

```
ψ/
├── learn/owner/repo     → ~/Code/github.com/owner/repo  (symlink)
└── incubate/owner/repo  → ~/Code/github.com/owner/repo  (symlink)

~/Code/               ← ghq root (source of truth)
└── github.com/owner/repo/  (actual clone)
```

## Health Check

When listing, verify symlinks are valid:

```bash
# Check for broken symlinks
find "$PSI/learn" "$PSI/incubate" -type l ! -exec test -e {} \; -print 2>/dev/null
```

If broken: `ghq get -u [url]` to restore source.

## Examples

```
# User shares URL to study
User: "I want to learn from https://github.com/SawyerHood/dev-browser"
→ ghq get -u https://github.com/SawyerHood/dev-browser
→ mkdir -p ψ/learn/SawyerHood
→ ln -sf ~/Code/github.com/SawyerHood/dev-browser ψ/learn/SawyerHood/dev-browser

# User wants to develop → redirect to /incubate
User: "I want to work on claude-mem"
→ /incubate https://github.com/thedotmack/claude-mem

# User says "/project incubate" → redirect to /incubate
User: "/project incubate https://github.com/Soul-Brews-Studio/arra-oracle-v3 --contribute"
→ /incubate https://github.com/Soul-Brews-Studio/arra-oracle-v3 --contribute
```

## Anti-Patterns

| ❌ Wrong | ✅ Right |
|----------|----------|
| `git clone` directly to ψ/ | `ghq get` then symlink |
| Flat: `ψ/learn/repo-name` | Org structure: `ψ/learn/owner/repo` |
| Copy files | Symlink always |
| Manual clone outside ghq | Everything through ghq |

## Quick Reference

```bash
# Add to learn
ghq get -u URL && mkdir -p "$PSI/learn/owner" && ln -sf "$(ghq root)/github.com/owner/repo" "$PSI/learn/owner/repo"

# Incubate (use standalone /incubate skill)
/incubate URL [--flash | --contribute | --status | --offload]

# Update source
ghq get -u URL

# Find repo
ghq list | grep name
```

<!-- file: project/project-manager.md -->
### File: `project/project-manager.md`

---
name: project-manager
description: Manage project lifecycle - learn, incubate, spinoff, reunion, offload, history. Use ghq + symlinks.
---

# Project Manager Skill

Complete project lifecycle management with 8 commands.

## Slug Format (Mixed Lookup)

Supports both formats:
- **Full**: `owner/repo` (priority) — e.g., `thedotmack/claude-mem`
- **Short**: `repo-name` (fallback) — e.g., `claude-mem`

```yaml
# ψ/memory/slugs.yaml
thedotmack/claude-mem: ~/Code/github.com/thedotmack/claude-mem
laris-co/arra-oracle-v3: ~/Code/github.com/laris-co/arra-oracle-v3
```

## Commands

| Command | Action | Script |
|---------|--------|--------|
| `/project search [query]` | Search repos (local→remote) | `scripts/search.sh` |
| `/project learn [url\|slug]` | Read-only study | `scripts/learn.sh` |
| `/project incubate [name]` | Work (auto-create if needed) | `scripts/incubate.sh` |
| `/project spinoff [name]` | Graduate to own repo | `scripts/spinoff.sh` |
| `/project reunion [slug\|all]` | Sync learnings + offload | `scripts/reunion.sh` |
| `/project offload [slug\|all]` | Remove symlinks (keep ghq) | `scripts/offload.sh` |
| `/project index [slug\|all]` | Index manifests to Oracle | `scripts/index.sh` |
| `/project history [slug]` | Git timeline analysis | `scripts/history.sh` |

## Lifecycle

```
/project search    → 🔍 Search repos (local ghq first, then GitHub API)
/project learn     → 📚 Study external repo (ψ/learn/)
/project incubate  → 🌱 Work on project (ψ/incubate/, auto-create if needed)
/project spinoff   → 🎓 Graduate to own repo
/project reunion   → 🤝 Sync learnings + offload
/project offload   → 📤 Just remove symlinks
/project index     → 🔮 Index manifests to Oracle
/project history   → 📊 Git activity analysis
```

## Limits

| Type | Max | Reason |
|------|-----|--------|
| **Incubate** | 5 | Cognitive load — focus over quantity |
| Learn | No limit | Read-only, low overhead |

**Before incubating new project**: Check count, offload if > 5.

## Quick Reference

### Search (find repos)
```bash
.claude/skills/project-manager/scripts/search.sh voice           # local first
.claude/skills/project-manager/scripts/search.sh voice --remote  # force GitHub API
.claude/skills/project-manager/scripts/search.sh --list-orgs     # show all orgs
```

### Learn (read-only)
```bash
.claude/skills/project-manager/scripts/learn.sh thedotmack/claude-mem
.claude/skills/project-manager/scripts/learn.sh claude-mem  # short slug
```

### Incubate (work, auto-create)
```bash
.claude/skills/project-manager/scripts/incubate.sh <name> [--org laris-co]
```

### Spinoff (graduate)
```bash
.claude/skills/project-manager/scripts/spinoff.sh <slug> <target-org/repo>
```

### Reunion (sync + offload)
```bash
.claude/skills/project-manager/scripts/reunion.sh thedotmack/claude-mem
.claude/skills/project-manager/scripts/reunion.sh claude-mem    # short slug
.claude/skills/project-manager/scripts/reunion.sh all           # all loaded
.claude/skills/project-manager/scripts/reunion.sh all --keep    # keep loaded
```

### Offload (remove symlinks)
```bash
.claude/skills/project-manager/scripts/offload.sh laris-co/arra-oracle-v3
.claude/skills/project-manager/scripts/offload.sh arra-oracle-v3  # short slug
.claude/skills/project-manager/scripts/offload.sh all        # clean slate
```

### Index (Oracle)
```bash
.claude/skills/project-manager/scripts/index.sh list              # show manifests
.claude/skills/project-manager/scripts/index.sh all               # index all
.claude/skills/project-manager/scripts/index.sh thedotmack/claude-mem  # specific
.claude/skills/project-manager/scripts/index.sh all --dry-run     # preview
```

### History (git analysis)
```bash
.claude/skills/project-manager/scripts/history.sh thedotmack/claude-mem
.claude/skills/project-manager/scripts/history.sh claude-mem --since="1 year ago"
```

## Reunion Pattern

1. **Connect** → `ghq get -u` (sync via ghq, not git pull)
2. **Scan** → Find `ψ/memory/*.md`, `learnings/`, `retrospectives/`, `docs/`
3. **Manifest** → Write to `ψ/memory/logs/index-YYYY-MM-DD-slug.json`
4. **Log** → Write to `ψ/memory/logs/reunion-YYYY-MM-DD.log`
5. **Offload** → Remove symlink (unless `--keep`)

## Index Pattern

1. **Read** → Load manifest JSON files
2. **Score** → Rank files by type (retrospectives=10, docs=5, CLAUDE.md=0)
3. **Filter** → Skip i18n, CLAUDE.md, low-value files
4. **Extract** → Get key content from high-value files
5. **Learn** → Write to `ψ/memory/learnings/` (two-layer pattern: learning file + auto-memory)

## Offload Pattern

- Remove symlink only (ghq keeps repo)
- Log to `ψ/memory/logs/offload-YYYY-MM-DD.log`
- Can restore: `/project learn [slug]` or `/project incubate [slug]`

## Files

- `scripts/search.sh` - Search repos (local ghq → GitHub API)
- `scripts/resolve-slug.sh` - Shared slug resolution (owner/repo + short)
- `scripts/learn.sh` - Clone + symlink to ψ/learn/
- `scripts/incubate.sh` - Clone (or create) + symlink to ψ/incubate/
- `scripts/spinoff.sh` - Move to external repo
- `scripts/reunion.sh` - Sync learnings + optional offload
- `scripts/offload.sh` - Remove symlinks, keep ghq
- `scripts/index.sh` - Index manifests to Oracle
- `scripts/history.sh` - Git activity analysis
- `templates/slugs.yaml` - Registry template

<!-- file: project/scripts/create.ts -->
### File: `project/scripts/create.ts`

```ts
#!/usr/bin/env bun
// create.ts - Create new GitHub repo, init, commit, push
import { $ } from "bun";
import { existsSync, mkdirSync, unlinkSync, symlinkSync } from "fs";
import { join } from "path";
import { getRoot, getPaths, ghqPath } from "./utils.ts";

const args = process.argv.slice(2);
const name = args.find((a) => !a.startsWith("--"));
if (!name) {
  console.log("Usage: ROOT=/path bun create.ts <name> [--public]");
  process.exit(1);
}

const ROOT = getRoot();
const { incubateDir } = getPaths(ROOT);
const ORG = "laris-co";
const isPublic = args.includes("--public");

const localPath = ghqPath(ORG, name);
const linkPath = join(incubateDir, ORG, name);
const visibility = isPublic ? "public" : "private";

console.log(`Creating: ${ORG}/${name} (${visibility})`);

// 1. Create GitHub repo
await $`gh repo create ${ORG}/${name} --${visibility} --clone=false`.quiet().catch(() => {
  console.log("  Repo may already exist, continuing...");
});

// 2. Clone via ghq
await $`ghq get -u github.com/${ORG}/${name}`.quiet().catch(() => {});

// 3. Init if no .git
if (!existsSync(`${localPath}/.git`)) {
  mkdirSync(localPath, { recursive: true });
  await $`git -C ${localPath} init`;
  await $`git -C ${localPath} remote add origin git@github.com:${ORG}/${name}.git`;
}

// 4. Create README if missing
if (!existsSync(`${localPath}/README.md`)) {
  await Bun.write(`${localPath}/README.md`, `# ${name}\n\nCreated by Oracle Open Framework\n`);
}

// 5. Initial commit if needed
const hasCommits = await $`git -C ${localPath} log --oneline -1`.quiet().then(() => true).catch(() => false);
if (!hasCommits) {
  await $`git -C ${localPath} add -A`;
  await $`git -C ${localPath} commit -m "Initial commit"`;
}

// 6. Push
await $`git -C ${localPath} push -u origin main`.quiet()
  .catch(() => $`git -C ${localPath} push -u origin master`.quiet())
  .catch(() => $`git -C ${localPath} branch -M main && git -C ${localPath} push -u origin main`.quiet());

// 7. Create symlink
mkdirSync(join(incubateDir, ORG), { recursive: true });
if (existsSync(linkPath)) unlinkSync(linkPath);
symlinkSync(localPath, linkPath);

console.log(`\nCreated: ${ORG}/${name} (${visibility})`);
console.log(`  GitHub: https://github.com/${ORG}/${name}`);
console.log(`  Local: ${localPath}`);
```

<!-- file: project/scripts/history.ts -->
### File: `project/scripts/history.ts`

```ts
#!/usr/bin/env bun
// history.ts - Git timeline analysis
import { $ } from "bun";
import { existsSync } from "fs";
import { basename } from "path";
import { resolveSlug } from "./resolve-slug.ts";

const args = process.argv.slice(2);
const sinceArg = args.find((a) => a.startsWith("--since="));
const since = sinceArg?.slice(8) || "6 months ago";
const input = args.find((a) => !a.startsWith("--"));

if (!input) {
  console.log("Usage: ROOT=/path bun history.ts <slug|path> [--since=6months]");
  process.exit(0);
}

const path = await resolveSlug(input);
if (!path || !existsSync(`${path}/.git`)) {
  console.log(`Not a git repo: ${input}`);
  process.exit(1);
}

const name = basename(path);
const git = (cmd: string) => $`git -C ${path} ${cmd.split(" ")}`.text().catch(() => "");

console.log(`# ${name}\nPath: ${path}\nSince: ${since}\n`);

// Stats
const [total, recent, first, last] = await Promise.all([
  git("rev-list --count HEAD"),
  git(`rev-list --count --since=${since} HEAD`),
  git("log --reverse --format=%ad --date=short").then((s) => s.split("\n")[0]),
  git("log -1 --format=%ad --date=short"),
]);

console.log(`## Summary\n| Metric | Value |\n|--------|-------|\n| Total | ${total.trim()} |\n| Recent | ${recent.trim()} |\n| First | ${first} |\n| Last | ${last.trim()} |\n`);

// Recent commits
console.log("## Recent Commits\n```");
console.log((await git(`log --oneline --since=${since} -15`)).trim() || "(none)");
console.log("```\n");

// Top files
const files = (await git(`log --name-only --pretty="" --since=${since}`)).trim().split("\n").filter(Boolean);
const counts: Record<string, number> = {};
files.forEach((f) => (counts[f] = (counts[f] || 0) + 1));
const top = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);

console.log("## Top Changed Files\n```");
top.forEach(([f, c]) => console.log(`  ${c} ${f}`));
console.log("```");
```

<!-- file: project/scripts/incubate.ts -->
### File: `project/scripts/incubate.ts`

```ts
#!/usr/bin/env bun
// incubate.ts - Clone or create repo for active work
import { $ } from "bun";
import { existsSync, mkdirSync, unlinkSync, symlinkSync } from "fs";
import { dirname, join } from "path";
import { getRoot, getPaths, parseRepo, ghqPath, updateSlugsFile } from "./utils.ts";

const args = process.argv.slice(2);
const input = args[0];
if (!input) {
  console.log("Usage: ROOT=/path bun incubate.ts <owner/repo|name> [--org org]");
  process.exit(1);
}

const ROOT = getRoot();
const { slugsFile, incubateDir } = getPaths(ROOT);
const orgFlag = args.indexOf("--org");
const defaultOrg = orgFlag !== -1 ? args[orgFlag + 1] : "laris-co";

const { owner, name, slug } = parseRepo(input, defaultOrg);
const localPath = ghqPath(owner, name);
const linkPath = join(incubateDir, owner, name);

console.log(`Incubating: ${slug}`);

// Check if repo exists on GitHub
const repoExists = await $`gh repo view ${slug}`.quiet().then(() => true).catch(() => false);

if (repoExists) {
  await $`ghq get -u github.com/${slug}`.quiet();
} else {
  console.log("  Creating new repo...");
  await $`gh repo create ${slug} --private --clone=false`;
  await $`ghq get github.com/${slug}`.quiet();

  // Init if empty
  if (!existsSync(join(localPath, "README.md"))) {
    await Bun.write(join(localPath, "README.md"), `# ${name}\n`);
    await $`git -C ${localPath} add README.md && git -C ${localPath} commit -m "Initial commit"`;
    await $`git -C ${localPath} push origin main`.quiet().catch(() => $`git -C ${localPath} push origin master`.quiet());
  }
}

// Create symlink
mkdirSync(dirname(linkPath), { recursive: true });
if (existsSync(linkPath)) unlinkSync(linkPath);
symlinkSync(localPath, linkPath);

// Register slug
await updateSlugsFile(slugsFile, slug, localPath);

console.log(`Ready: ${localPath}`);
console.log(`GitHub: https://github.com/${slug}`);
```

<!-- file: project/scripts/index.ts -->
### File: `project/scripts/index.ts`

```ts
#!/usr/bin/env bun
// index.ts - Index manifest files to Oracle knowledge base
import { $ } from "bun";
import { existsSync, readdirSync } from "fs";
import { join, basename } from "path";
import { getRoot, getPaths, today } from "./utils.ts";

const args = process.argv.slice(2);
const cmd = args[0] || "list";

// Show usage only for help flag (list is default, doesn't need ROOT check first)
if (args.includes("--help") || args.includes("-h")) {
  console.log("Usage: ROOT=/path bun index.ts [list|all|slug] [--dry-run]");
  process.exit(0);
}

const ROOT = getRoot();
const { logDir } = getPaths(ROOT);
const dryRun = args.includes("--dry-run");
const dateArg = args.find((a) => a.match(/^20\d{2}-\d{2}-\d{2}$/) || a === "today");
const date = dateArg === "today" || !dateArg ? today() : dateArg;

// Get our orgs for scoring
const ourOrgs = await $`gh api user/orgs --jq '.[].login'`.text().catch(() => "");
const ourUser = await $`gh api user --jq '.login'`.text().catch(() => "");
const orgPattern = new RegExp(`github.com/(${[...ourOrgs.trim().split("\n"), ourUser.trim()].filter(Boolean).join("|")})/`);

function scoreFile(file: string): number {
  if (file.includes("/ψ/") && file.endsWith(".md")) return 1;
  if (orgPattern.test(file)) {
    if (file.includes("/retrospectives/") || file.includes("/learnings/") || file.includes("/memory/")) return 1;
  }
  return 0;
}

function listManifests() {
  const manifests = readdirSync(logDir).filter((f) => f.startsWith(`index-${date}-`) && f.endsWith(".json"));
  
  console.log(`Manifests for ${date}:`);
  
  let total = 0, indexable = 0;
  
  for (const m of manifests) {
    const data = JSON.parse(Bun.file(join(logDir, m)).toString());
    const files = data.files || [];
    const scored = files.filter((f: string) => scoreFile(f) > 0);
    
    const slug = m.replace(`index-${date}-`, "").replace(".json", "").replace("_", "/");
    console.log(`  ${slug}: ${scored.length}/${files.length} indexable`);
    
    total += files.length;
    indexable += scored.length;
  }
  
  console.log(`\nTotal: ${total} files, ${indexable} indexable`);
}

async function indexManifest(manifestPath: string) {
  const data = JSON.parse(await Bun.file(manifestPath).text());
  const slug = data.project;
  
  console.log(`\nIndexing: ${slug}`);
  console.log(`  Source: ${data.source}`);
  
  let indexed = 0, skipped = 0;
  
  for (const file of data.files || []) {
    const score = scoreFile(file);
    if (!score) { skipped++; continue; }
    if (!existsSync(file)) { console.log(`  Not found: ${basename(file)}`); continue; }
    
    console.log(`  ${dryRun ? "[DRY] " : ""}${basename(file)}`);
    indexed++;
  }
  
  console.log(`  Indexed: ${indexed}, Skipped: ${skipped}`);
}

// Main
if (cmd === "list" || cmd === "--list") {
  listManifests();
} else if (cmd === "all") {
  const manifests = readdirSync(logDir).filter((f) => f.startsWith(`index-${date}-`) && f.endsWith(".json"));
  for (const m of manifests) await indexManifest(join(logDir, m));
} else {
  const safeSlug = cmd.replace("/", "_");
  const manifestPath = join(logDir, `index-${date}-${safeSlug}.json`);
  if (existsSync(manifestPath)) {
    await indexManifest(manifestPath);
  } else {
    console.log(`Not found: ${manifestPath}`);
    listManifests();
  }
}
```

<!-- file: project/scripts/learn.ts -->
### File: `project/scripts/learn.ts`

```ts
#!/usr/bin/env bun
// learn.ts - Clone repo for read-only study
import { $ } from "bun";
import { existsSync, mkdirSync, unlinkSync, symlinkSync } from "fs";
import { dirname, join } from "path";
import { getRoot, getPaths, parseRepo, ghqPath, updateSlugsFile } from "./utils.ts";

const input = process.argv[2];
if (!input) {
  console.log("Usage: ROOT=/path bun learn.ts <owner/repo|url>");
  process.exit(1);
}

const ROOT = getRoot();
const { slugsFile, learnDir } = getPaths(ROOT);

// Parse input (handles URLs, owner/repo, or just repo name)
let repo: string;
if (input.startsWith("http") || input.includes("/")) {
  repo = parseRepo(input).slug;
} else {
  // Search ghq for short name
  const list = await $`ghq list`.text();
  const match = list.split("\n").find((l) => l.toLowerCase().endsWith(`/${input.toLowerCase()}`));
  if (!match) {
    console.error(`Not found: ${input}. Use owner/repo format.`);
    process.exit(1);
  }
  repo = match.replace("github.com/", "");
}

const { owner, name } = parseRepo(repo);
const localPath = ghqPath(owner, name);
const linkPath = join(learnDir, owner, name);

console.log(`Learning: ${owner}/${name}`);

// Clone/update via ghq
await $`ghq get ${existsSync(localPath) ? "-u" : ""} github.com/${repo}`.quiet();

// Create symlink
mkdirSync(dirname(linkPath), { recursive: true });
if (existsSync(linkPath)) unlinkSync(linkPath);
symlinkSync(localPath, linkPath);

// Register slug
await updateSlugsFile(slugsFile, `${owner}/${name}`, localPath);

console.log(`Ready: ${localPath}`);
```

<!-- file: project/scripts/offload.ts -->
### File: `project/scripts/offload.ts`

```ts
#!/usr/bin/env bun
// offload.ts - Remove symlinks, keep ghq + slugs
import { mkdirSync, unlinkSync, appendFileSync } from "fs";
import { join } from "path";
import { getRoot, getPaths, getSymlinks, matchesSlug, today, now, LinkInfo } from "./utils.ts";

const arg = process.argv[2];
if (!arg) {
  console.log("Usage: ROOT=/path bun offload.ts [slug|all]");
  process.exit(1);
}

const ROOT = getRoot();
const { learnDir, incubateDir, logDir } = getPaths(ROOT);
mkdirSync(logDir, { recursive: true });

async function offload(slug?: string) {
  const logFile = join(logDir, `offload-${today()}.log`);
  if (!slug) await Bun.write(logFile, `# Offload ${today()} ${now()}\n`);

  let count = 0;

  for (const [type, dir] of [["learn", learnDir], ["incubate", incubateDir]] as const) {
    for (const link of await getSymlinks(dir)) {
      if (slug && !matchesSlug(link, slug)) continue;

      console.log(`Offloading from ${type}: ${link.slug}`);
      appendFileSync(logFile, `\n## ${link.slug}\n- Type: ${type}\n- Path: ${link.target}\n`);
      unlinkSync(link.path);
      count++;
    }
  }

  if (slug && count === 0) {
    console.log(`Not found: ${slug}`);
  } else {
    console.log(`Offloaded ${count} projects → ${logFile}`);
  }
}

await offload(arg === "all" ? undefined : arg);
```

<!-- file: project/scripts/resolve-slug.ts -->
### File: `project/scripts/resolve-slug.ts`

```ts
#!/usr/bin/env bun
// resolve-slug.ts - Resolve slug to path
import { $ } from "bun";
import { existsSync } from "fs";
import { expandPath, findInSlugs, getSymlinks, getPaths } from "./utils.ts";

const ROOT = process.env.ROOT;
const paths = ROOT ? getPaths(ROOT) : null;

export async function resolveSlug(input: string): Promise<string | null> {
  // 1. Direct path
  const expanded = expandPath(input);
  if (existsSync(expanded)) return expanded;

  // 2. Slugs.yaml
  if (paths) {
    const fromSlugs = await findInSlugs(paths.slugsFile, input);
    if (fromSlugs) return fromSlugs;

    // 3. Learn/incubate symlinks
    for (const dir of [paths.learnDir, paths.incubateDir]) {
      for (const link of await getSymlinks(dir)) {
        if (link.slug === input || link.repo === input) return link.target || link.path;
      }
    }
  }

  // 4. ghq
  try {
    const paths = (await $`ghq list -p`.text()).trim().split("\n");
    return paths.find((p) => p.toLowerCase().endsWith(`/${input.toLowerCase()}`)) || null;
  } catch {
    return null;
  }
}

if (import.meta.main) {
  const input = process.argv[2];
  if (!input) {
    console.log("Usage: ROOT=/path bun resolve-slug.ts <slug>");
    process.exit(1);
  }

  const result = await resolveSlug(input);
  if (result) {
    console.log(`Resolved: ${input} → ${result}`);
  } else {
    console.log(`Not found: ${input}`);
    process.exit(1);
  }
}
```

<!-- file: project/scripts/reunion.ts -->
### File: `project/scripts/reunion.ts`

```ts
#!/usr/bin/env bun
// reunion.ts - Scan project, create manifest, optionally offload
import { $ } from "bun";
import { existsSync, mkdirSync, appendFileSync, readdirSync } from "fs";
import { join, basename } from "path";
import { getRoot, getPaths, getSymlinks, matchesSlug, today, now, LinkInfo } from "./utils.ts";

const args = process.argv.slice(2);
const slug = args.find((a) => !a.startsWith("--"));
if (!slug) {
  console.log("Usage: ROOT=/path bun reunion.ts [slug|all] [--keep]");
  process.exit(1);
}

const ROOT = getRoot();
const { learnDir, incubateDir, logDir } = getPaths(ROOT);
mkdirSync(logDir, { recursive: true });
const keep = args.includes("--keep");

async function findProject(slug: string): Promise<LinkInfo | null> {
  for (const dir of [learnDir, incubateDir]) {
    for (const link of await getSymlinks(dir)) {
      if (matchesSlug(link, slug)) return link;
    }
  }
  return null;
}

async function reunionSingle(slug: string) {
  const link = await findProject(slug);
  if (!link?.target) {
    console.log(`Not loaded: ${slug}. Use: /project learn ${slug}`);
    return;
  }

  console.log(`Reunion: ${link.slug}`);
  console.log(`  Path: ${link.target}`);

  // Sync via ghq
  await $`ghq get -u github.com/${link.slug}`.quiet().catch(() => {});

  // Find knowledge files
  const manifest = join(logDir, `index-${today()}-${link.slug.replace("/", "_")}.json`);
  const files: string[] = [];

  for (const dir of ["ψ/memory", "learnings", "retrospectives", "docs"]) {
    const fullDir = join(link.target, dir);
    if (!existsSync(fullDir)) continue;
    
    const found = readdirSync(fullDir, { recursive: true })
      .filter((f) => String(f).endsWith(".md"))
      .map((f) => join(fullDir, String(f)));
    files.push(...found);
    
    if (found.length) console.log(`  Found ${found.length} files in ${dir}/`);
  }

  // Write manifest
  await Bun.write(manifest, JSON.stringify({
    project: link.slug,
    source: `https://github.com/${link.slug}`,
    local_path: link.target,
    scanned: `${today()} ${now()}`,
    files,
  }, null, 2));

  console.log(`  Manifest: ${manifest}`);
  appendFileSync(join(logDir, `reunion-${today()}.log`), `- ${link.slug}: reunion at ${now()}\n`);

  // Offload unless --keep
  if (!keep) {
    const { unlinkSync } = await import("fs");
    unlinkSync(link.path);
    console.log(`  Offloaded (use --keep to retain)`);
  }
}

async function reunionAll() {
  const allLinks = [
    ...(await getSymlinks(learnDir)),
    ...(await getSymlinks(incubateDir)),
  ];
  
  const unique = [...new Set(allLinks.map((l) => l.slug))];
  console.log(`Found ${unique.length} projects\n`);

  for (const slug of unique) {
    await reunionSingle(slug);
    console.log("---");
  }
}

if (slug === "all") {
  await reunionAll();
} else {
  await reunionSingle(slug);
}
```

<!-- file: project/scripts/search.ts -->
### File: `project/scripts/search.ts`

```ts
#!/usr/bin/env bun
// search.ts - Find repos (local ghq first, GitHub API fallback)
import { $ } from "bun";

const args = process.argv.slice(2);
const query = args[0];
const remote = args.includes("--remote");

if (!query) {
  console.log("Usage: bun search.ts <query> [--remote]");
  process.exit(1);
}

// List orgs mode
if (query === "--list-orgs") {
  console.log("Organizations:");
  const orgs = (await $`gh api user/orgs --jq '.[].login'`.text()).trim().split("\n").filter(Boolean);
  for (const org of orgs) {
    const count = await $`gh repo list ${org} --limit 1000 --json name --jq 'length'`.text().catch(() => "?");
    console.log(`  ${org} (${count.trim()} repos)`);
  }
  process.exit(0);
}

// Local search (ghq)
console.log(`Searching local: ${query}\n`);
const local = (await $`ghq list`.text().catch(() => ""))
  .split("\n")
  .filter((l) => l.toLowerCase().includes(query.toLowerCase()));

if (local.length) {
  console.log(`Found ${local.length} local:`);
  local.forEach((r) => console.log(`  ~/Code/${r}`));
  if (!remote) process.exit(0);
}

// Remote search - fallback or when --remote
if (remote || !local.length) {
  console.log("\nSearching GitHub...\n");

  const user = (await $`gh api user --jq '.login'`.text()).trim();
  console.log(`Personal (${user}):`);
  const personal = await $`gh repo list ${user} --limit 100 --json name --jq '.[].name'`.text().catch(() => "");
  personal.split("\n").filter((n) => n.toLowerCase().includes(query.toLowerCase())).forEach((n) => console.log(`  ${n}`));

  const orgs = (await $`gh api user/orgs --jq '.[].login'`.text()).trim().split("\n").filter(Boolean);
  for (const org of orgs) {
    const repos = await $`gh repo list ${org} --limit 100 --json name --jq '.[].name'`.text().catch(() => "");
    const matches = repos.split("\n").filter((n) => n.toLowerCase().includes(query.toLowerCase()));
    if (matches.length) {
      console.log(`\n${org}:`);
      matches.forEach((n) => console.log(`  ${org}/${n}`));
    }
  }
}

console.log("\nTo clone: /project learn owner/repo");
```

<!-- file: project/scripts/spinoff.ts -->
### File: `project/scripts/spinoff.ts`

```ts
#!/usr/bin/env bun
// spinoff.ts - Graduate project to its own repo
import { $ } from "bun";
import { existsSync, readlinkSync, unlinkSync, symlinkSync } from "fs";
import { join } from "path";
import { getRoot, getPaths, ghqPath, parseRepo } from "./utils.ts";

const [slug, target] = process.argv.slice(2);
if (!slug || !target) {
  console.log("Usage: ROOT=/path bun spinoff.ts <slug> <target-org/repo>");
  process.exit(1);
}

const ROOT = getRoot();
const { incubateDir } = getPaths(ROOT);

const incubatePath = join(ROOT, "ψ/incubate", slug);

if (!existsSync(incubatePath)) {
  console.error(`Not found: ${incubatePath}`);
  process.exit(1);
}

const sourcePath = existsSync(incubatePath) && 
  (await Bun.file(incubatePath).exists() ? incubatePath : readlinkSync(incubatePath));

const { owner, name } = parseRepo(target);
const targetPath = ghqPath(owner, name);

console.log(`Spinoff: ${slug} → ${target}`);
console.log(`  Source: ${sourcePath}`);
console.log(`  Target: ${targetPath}`);

// 1. Create target repo
const exists = await $`gh repo view ${target}`.quiet().then(() => true).catch(() => false);
if (!exists) await $`gh repo create ${target} --private`;

// 2. Clone to ghq
await $`ghq get github.com/${target}`.quiet();

// 3. Copy files
if (existsSync(sourcePath)) {
  await $`cp -r ${sourcePath}/* ${targetPath}/`.quiet().catch(() => {});
  await $`cp -r ${sourcePath}/.[!.]* ${targetPath}/`.quiet().catch(() => {});
}

// 4. Commit and push
await $`git -C ${targetPath} add -A`;
await $`git -C ${targetPath} commit -m "Spinoff from ${slug}"`.quiet().catch(() => {});
await $`git -C ${targetPath} push origin main`.quiet().catch(() => 
  $`git -C ${targetPath} push origin master`.quiet()
);

// 5. Update symlink
if (existsSync(incubatePath)) unlinkSync(incubatePath);
symlinkSync(targetPath, incubatePath);

console.log(`\nSpinoff complete: ${slug} → ${target}`);
console.log(`  GitHub: https://github.com/${target}`);
```

<!-- file: project/scripts/utils.ts -->
### File: `project/scripts/utils.ts`

```ts
// utils.ts - Shared utilities for project scripts
import { Glob } from "bun";
import { existsSync, lstatSync, readlinkSync, realpathSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";

// --- Environment ---
export function getRoot(): string {
  const ROOT = process.env.ROOT;
  if (!ROOT) {
    console.error("Error: ROOT environment variable required");
    process.exit(1);
  }
  return ROOT;
}

export function getPaths(root: string) {
  const psiPath = join(root, "ψ");
  const psi = existsSync(psiPath) ? realpathSync(psiPath) : psiPath;
  return {
    slugsFile: join(psi, "memory", "resonance", "slugs.yaml"),
    learnDir: join(psi, "learn", "repo", "github.com"),
    incubateDir: join(psi, "incubate", "repo", "github.com"),
    logDir: join(psi, "memory", "logs"),
  };
}

// --- Date/Time ---
export const today = () => new Date().toISOString().slice(0, 10);
export const now = () => new Date().toTimeString().slice(0, 5);

// --- Slug parsing ---
export type RepoInfo = { owner: string; name: string; slug: string };

export function parseRepo(input: string, defaultOrg = "laris-co"): RepoInfo {
  if (input.startsWith("http")) {
    const slug = input.replace("https://github.com/", "").replace(".git", "");
    const [owner, name] = slug.split("/");
    return { owner, name, slug };
  }
  if (input.includes("/")) {
    const [owner, name] = input.split("/");
    return { owner, name, slug: input };
  }
  return { owner: defaultOrg, name: input, slug: `${defaultOrg}/${input}` };
}

export function ghqPath(owner: string, name: string): string {
  return join(homedir(), "Code/github.com", owner, name);
}

// --- Symlink operations ---
export type LinkInfo = { path: string; org: string; repo: string; slug: string; target?: string };

export async function getSymlinks(baseDir: string): Promise<LinkInfo[]> {
  if (!existsSync(baseDir)) return [];

  const links: LinkInfo[] = [];
  const glob = new Glob("*/*");

  for await (const match of glob.scan({ cwd: baseDir, onlyFiles: false })) {
    const fullPath = join(baseDir, match);
    try {
      if (lstatSync(fullPath).isSymbolicLink()) {
        const [org, repo] = match.split("/");
        const target = (() => { try { return readlinkSync(fullPath); } catch { return undefined; } })();
        links.push({ path: fullPath, org, repo, slug: `${org}/${repo}`, target });
      }
    } catch {}
  }
  return links;
}

export function matchesSlug(link: LinkInfo, slug: string): boolean {
  return slug.includes("/") ? link.slug === slug : link.repo === slug;
}

// --- Slugs.yaml operations ---
export async function findInSlugs(slugsFile: string, input: string): Promise<string | null> {
  if (!existsSync(slugsFile)) return null;

  const content = await Bun.file(slugsFile).text();
  for (const line of content.split("\n")) {
    const matches =
      line.startsWith(`${input}:`) ||
      line.includes(`/${input}:`) ||
      (!input.includes("/") && line.startsWith(`${input}:`));

    if (matches) {
      const path = line.split(":").slice(1).join(":").trim().replace(/^~/, homedir());
      if (existsSync(path)) return path;
    }
  }
  return null;
}

export async function updateSlugsFile(slugsFile: string, slug: string, path: string) {
  const dir = dirname(slugsFile);
  const { mkdirSync } = await import("fs");
  mkdirSync(dir, { recursive: true });

  if (!existsSync(slugsFile)) {
    await Bun.write(slugsFile, "# Slug Registry (owner/repo: path)\n");
  }

  const content = await Bun.file(slugsFile).text();
  const filtered = content.split("\n").filter((l) => !l.startsWith(`${slug}:`)).join("\n");
  await Bun.write(slugsFile, `${filtered}\n${slug}: ${path}\n`);
}

// --- Path expansion ---
export function expandPath(input: string): string {
  return input.replace(/^~/, homedir());
}
```

<!-- file: project/templates/slugs.yaml -->
### File: `project/templates/slugs.yaml`

```
# Slug Registry
# Auto-generated by project-manager skill
# Format:
#   slug-name:
#     path: ψ/learn/repo/slug-name OR ψ/incubate/slug-name
#     ghq: ~/Code/github.com/org/repo
#     github: github.com/org/repo
#     type: learn | incubate | spinoff
#     last_reunion: YYYY-MM-DD HH:MM | null
#     status: linked | unlinked

# Example:
# arra-oracle-v3:
#   path: ψ/learn/repo/arra-oracle-v3
#   ghq: ~/Code/github.com/laris-co/arra-oracle-v3
#   github: github.com/laris-co/arra-oracle-v3
#   type: learn
#   last_reunion: null
#   status: linked
```
