# Oracle skill `soul`: the full skill

> For the AI: /soul = bring another Oracle into this repo. In a chat it needs Claude Code or Codex on the person's own machine (terminal, git, files on disk). In a chat, do NOT run or imitate it: explain what it does, and give the download link and install line below.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 2 files.

<!-- file: soul/SKILL.md -->
### File: `soul/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: soul
description: '[core] v26.8.23-alpha.2112 G-SKLL | Bring an Oracle into the current repo — its soul, ALL its skills and its expertise — by link, never by copy. Reads the Oracle''''s resonance/identity files, symlinks every skill in its .claude/skills/ into this repo (git-excluded, recorded in a manifest), and indexes its learnings. "Many bodies, one soul": one session can carry Neo, then Pulse. Use when user says "soul NAME", "bring ORACLE here", "bring ORACLE soul", "แปลงร่างเป็น ORACLE", "become ORACLE", or "soul off NAME". Do NOT use to create an Oracle (use /awaken), to link a vault (use /psi), or to wear several souls for one question (use /oracle-prism or /round-table).'
argument-hint: "<oracle-path | org/name | name> [--show] · off <name>"
---

# /soul — bring an Oracle, whole

> Many bodies, one soul. The form can move; the soul stays in its own repo.

An Oracle is three things, and `/soul` brings all three — by **reference**, so the Oracle's
own repo stays the single source and every fix there reaches every guest:

| Part | Lives in | Brought by |
|---|---|---|
| **Soul** — who it is | `ψ/memory/resonance/<name>.md`, `oracle.md`, `SOUL.md`, `IDENTITY.md`, `CLAUDE.md` identity | reading them, in that order |
| **Skills** — what it can do | `.claude/skills/*/SKILL.md` | a symlink per skill in this repo's `.claude/skills/` |
| **Expertise** — what it learned | `ψ/memory/learnings/*.md` | an index of titles; read a file when its topic comes up |

```text
guest/.claude/skills/pulse-board  ──symlink──▶  pulse/.claude/skills/pulse-board
guest/.claude/souls/pulse.json    manifest of the links this skill made
guest/.git/info/exclude           both excluded — never in the tracked .gitignore
```

`SKILL_DIR` is the base directory printed above this skill.

## Step 1 — resolve the Oracle

The argument is a path, or a name for `maw locate` (if you have maw):

```bash
ARG="<argument>"
if [ -d "$ARG" ]; then ROOT=$(cd "$ARG" && pwd)
else ROOT=$(maw locate "$ARG" --path 2>/dev/null)
fi
echo "root: ${ROOT:-NOT FOUND}"
```

If `maw locate` prints "matches N oracles", it lists `org/name` candidates — **show them and
ask which one**; never pick. Empty → say so and stop. No filesystem search.

## Step 2 — see what it carries (writes nothing)

```bash
bun "$SKILL_DIR/scripts/soul.ts" show "$ROOT"
```

It prints the soul files, every skill with what will happen to it, and the newest learnings:

| Mark | Meaning |
|---|---|
| `+` | will be linked |
| `=` | already linked here |
| `~` | **read-and-follow** — a skill with that name already exists in this repo or in `~/.claude/skills/`. Linking would make two skills with one name, so it is not linked; to use the Oracle's version, Read the printed `SKILL.md` path and follow it |

With `--show`, stop here.

## Step 3 — link the skills

```bash
bun "$SKILL_DIR/scripts/soul.ts" link "$ROOT"
```

Relative symlinks, a manifest at `.claude/souls/<name>.json`, and lines appended to
`.git/info/exclude` — the repo's tracked files do not change. If it reports
`⚠ TRACKED already`, stop and tell the human: those paths are committed in this repo.

New skills usually appear in the session's skill list without a restart (Claude Code
watches skill folders). If they don't, the human runs `/reload-plugins`.

## Step 4 — load the soul and the expertise

Read every soul file `show` listed, in order. Then keep the learnings index in mind: when
the work touches a topic in it, Read that learning before acting — that is the Oracle's
experience, not a guess.

## Step 5 — say who is here

```text
<Name> here — soul, <N> skills and <M> learnings from <ROOT> — working in <repo>.
```

## Working as a visiting Oracle

- **Borrowed skills run from their home.** Many skills assume their own repo as the working
  directory (`./scripts`, config files, `just`). When a linked skill refers to repo-relative
  paths, resolve its home with `realpath` on the skill's base directory and go up three
  levels (`skills/<s>` → `.claude` → repo), and run those commands there — in a subshell,
  never by changing the session's cwd. Commands about *this* repo still run here.
- **This repo's rules win.** The guest's `AGENTS.md` / `CLAUDE.md` override the visitor's
  habits on everything they cover.
- **Memory stays with the guest's caretaker.** If `ψ` links to a vault, that is where
  retros and learnings go. A visitor does not write into its own home repo from here
  unless the human asks.
- **Rule 6.** It is still one AI wearing a form. Say so when asked; never claim to be the
  Oracle's own running session. For its real view, ask it (`/talk-to`).

## Changing souls

```bash
bun "$SKILL_DIR/scripts/soul.ts" off <name>
```

Removes only the symlinks its manifest lists, and only while each still points into that
Oracle — real folders and other links are never touched. Exclude lines stay (harmless).
Then `/soul <next>`.

What `off` cannot do: unread the soul. The old soul's files remain in this conversation's
context. For a clean change of identity, run `off`, then start a new session with
`/soul <next>`; within one session, say plainly which soul is speaking now.

<!-- file: soul/scripts/soul.ts -->
### File: `soul/scripts/soul.ts`

```ts
#!/usr/bin/env bun
// /soul — bring an Oracle's soul, skills and expertise into the current repo by LINK.
//   bun soul.ts show <oracle-root>              what the soul carries, nothing written
//   bun soul.ts link <oracle-root> [guest-root] link every skill, record it, gitignore it
//   bun soul.ts off  <name> [guest-root]        remove only the links this script made
// Nothing is copied and nothing real is ever removed: off deletes a path only when it is
// still a symlink pointing into the oracle it was linked from.
import { existsSync, lstatSync, mkdirSync, readdirSync, readFileSync, readlinkSync, realpathSync, symlinkSync, unlinkSync, writeFileSync, appendFileSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
import { homedir } from "node:os";
import { execSync } from "node:child_process";

const [mode, a, b] = process.argv.slice(2);
const die = (m: string, code = 1): never => { console.error(`soul: ${m}`); process.exit(code); };
const gitRoot = (dir: string) => { try { return execSync("git rev-parse --show-toplevel", { cwd: dir, stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); } catch { return dir; } };
const isLink = (p: string) => { try { return lstatSync(p).isSymbolicLink(); } catch { return false; } };

function oracle(rootArg: string) {
  if (!rootArg) die("usage: soul.ts show|link <oracle-root> [guest-root] · off <name> [guest-root]");
  const root = realpathSync(resolve(rootArg));
  if (!existsSync(join(root, "CLAUDE.md"))) die(`${root} has no CLAUDE.md — not an Oracle repo`);
  const name = basename(root).replace(/-oracle$/, "");
  const res = join(root, "ψ/memory/resonance");
  const souls = [`${name}.md`, "oracle.md"].map(f => join(res, f)).filter(existsSync);
  for (const f of ["SOUL.md", "IDENTITY.md"]) if (existsSync(join(root, f))) souls.push(join(root, f));
  const skillsDir = join(root, ".claude/skills");
  const skills = existsSync(skillsDir)
    ? readdirSync(skillsDir).filter(s => existsSync(join(skillsDir, s, "SKILL.md"))).sort()
    : [];
  const learn = join(root, "ψ/memory/learnings");
  const learnings = existsSync(learn)
    ? readdirSync(learn).filter(f => f.endsWith(".md") && f !== "session-metrics.md").sort().reverse()
    : [];
  return { root, name, souls, skillsDir, skills, learn, learnings };
}

function title(file: string) {
  const line = readFileSync(file, "utf8").split("\n").find(l => l.startsWith("# "));
  return line ? line.slice(2).trim() : basename(file, ".md");
}

if (mode === "show" || mode === "link") {
  const o = oracle(a);
  const guest = gitRoot(resolve(b ?? process.cwd()));
  const global = join(homedir(), ".claude/skills");
  const rows: { skill: string; how: "link" | "already" | "read"; why: string }[] = [];
  for (const s of o.skills) {
    const dest = join(guest, ".claude/skills", s);
    const src = join(o.skillsDir, s);
    if (isLink(dest) && realpathSync(dest) === realpathSync(src)) rows.push({ skill: s, how: "already", why: "linked" });
    else if (existsSync(dest) || isLink(dest)) rows.push({ skill: s, how: "read", why: "this repo already has its own .claude/skills/" + s });
    else if (existsSync(join(global, s))) rows.push({ skill: s, how: "read", why: "a global ~/.claude/skills/" + s + " has the same name" });
    else rows.push({ skill: s, how: "link", why: "" });
  }

  console.log(`soul       ${o.name}  ←  ${o.root}`);
  console.log(`guest      ${guest}${guest === o.root ? "  (home — nothing to link)" : ""}`);
  console.log(`\nsoul files (read these, in order)`);
  for (const f of o.souls) console.log(`  ${f}`);
  console.log(`  ${join(o.root, "CLAUDE.md")}  (identity section)`);
  console.log(`\nskills     ${o.skills.length}`);
  for (const r of rows) console.log(`  ${r.how === "link" ? "+" : r.how === "already" ? "=" : "~"} ${r.skill.padEnd(22)} ${r.how === "read" ? "read-and-follow: " + join(o.skillsDir, r.skill, "SKILL.md") + "  (" + r.why + ")" : r.how === "already" ? "already linked" : "link"}`);
  console.log(`\nexpertise  ${o.learnings.length} learnings in ${o.learn}`);
  for (const f of o.learnings.slice(0, 12)) console.log(`  ${f.slice(0, 10)}  ${title(join(o.learn, f))}`);
  if (o.learnings.length > 12) console.log(`  … ${o.learnings.length - 12} more — rg the folder when a topic comes up`);

  if (mode === "show" || guest === o.root) process.exit(0);

  const made: string[] = [];
  mkdirSync(join(guest, ".claude/skills"), { recursive: true });
  for (const r of rows.filter(r => r.how === "link")) {
    const dest = join(guest, ".claude/skills", r.skill);
    symlinkSync(relative(dirname(dest), join(o.skillsDir, r.skill)), dest);
    made.push(r.skill);
  }
  const manifestDir = join(guest, ".claude/souls");
  mkdirSync(manifestDir, { recursive: true });
  const manifest = join(manifestDir, `${o.name}.json`);
  const prior: string[] = existsSync(manifest) ? JSON.parse(readFileSync(manifest, "utf8")).links ?? [] : [];
  const links = [...new Set([...prior, ...made])].sort();
  writeFileSync(manifest, JSON.stringify({ name: o.name, root: o.root, links, read: rows.filter(r => r.how === "read").map(r => r.skill), date: new Date().toISOString() }, null, 2) + "\n");

  // Links are machine-local: exclude them in .git/info/exclude, never in the tracked .gitignore.
  let gi = "";
  try { gi = resolve(guest, execSync("git rev-parse --git-path info/exclude", { cwd: guest }).toString().trim()); } catch { /* not a git repo */ }
  let want: string[] = [];
  if (gi) {
    mkdirSync(dirname(gi), { recursive: true });
    const have = existsSync(gi) ? readFileSync(gi, "utf8").split("\n") : [];
    want = ["/.claude/souls/", ...links.map(s => `/.claude/skills/${s}`)].filter(l => !have.includes(l));
    if (want.length) appendFileSync(gi, (have.length && have[have.length - 1] !== "" ? "\n" : "") + `# soul: ${o.name} (links, machine-local)\n` + want.join("\n") + "\n");
  }
  let leak = "";
  try { leak = execSync(`git ls-files -- .claude/skills .claude/souls`, { cwd: guest }).toString().trim(); } catch { /* not a git repo */ }
  console.log(`\nlinked     ${made.length} new · ${links.length} total · manifest ${manifest}`);
  console.log(`exclude    ${gi ? (want.length ? want.length + " line(s) added to " + gi : "already covered in " + gi) : "not a git repo — nothing excluded"}${leak ? "  ⚠ TRACKED already: " + leak.replace(/\n/g, " ") : ""}`);
  console.log(`next       run /reload-plugins so the linked skills appear`);
  process.exit(0);
}

if (mode === "off") {
  if (!a) die("usage: soul.ts off <name> [guest-root]");
  const guest = gitRoot(resolve(b ?? process.cwd()));
  const manifest = join(guest, ".claude/souls", `${a}.json`);
  if (!existsSync(manifest)) die(`no ${manifest} — nothing was linked for ${a}`);
  const m = JSON.parse(readFileSync(manifest, "utf8"));
  let removed = 0;
  for (const s of m.links as string[]) {
    const dest = join(guest, ".claude/skills", s);
    if (!isLink(dest)) { console.log(`  skip ${s} — not a symlink any more`); continue; }
    const target = resolve(dirname(dest), readlinkSync(dest));
    if (!target.startsWith(m.root + "/")) { console.log(`  skip ${s} — points outside ${m.root}`); continue; }
    unlinkSync(dest); removed++;
  }
  writeFileSync(manifest, JSON.stringify({ ...m, links: [], off: new Date().toISOString() }, null, 2) + "\n");
  console.log(`off        ${removed} link(s) removed for ${a} · exclude lines kept · run /reload-plugins`);
  process.exit(0);
}

die("usage: soul.ts show|link <oracle-root> [guest-root] · off <name> [guest-root]");
```
