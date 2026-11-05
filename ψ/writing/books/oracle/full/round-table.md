# Oracle skill `round-table`: the full skill

> For the AI: /round-table = a round table: several voices debate one question. In a chat it needs Claude Code or Codex on the person's own machine (terminal, git, files on disk). In a chat, do NOT run or imitate it: explain what it does, and give the download link and install line below.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 7 files.

<!-- file: round-table/SKILL.md -->
### File: `round-table/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: round-table
description: '[core] v26.8.23-alpha.2112 G-SKLL | Convene a Round Table (โต๊ะกลม): 3–8 souls — persona files, Oracles, or real people''''s DNA — debate ONE stakes-bearing decision over exactly 4 rounds (OPEN, DEEPEN, CONVERGE, VOTE), one subagent per soul, then vote with 1–10 confidence; a script does the arithmetic and deadlocks go to the human. Use when user says "round table", "round-table", "โต๊ะกลม", "convene the council", "deliberate this". For "should we …" questions, ask before convening. Do NOT use for brainstorming or one-perspective-at-a-time analysis (use /oracle-prism).'
argument-hint: '"<question>" --agents a,b,c [--options x,y,z] [--aggregator weighted|majority|unanimity-or-escalate]'
---

# /round-table — โต๊ะกลม

> "Many bodies, one soul" — so one agent can seat many souls at one table, let them argue,
> and still hand the decision back to the human.

`/oracle-prism` wears souls one after another, inline. A Round Table seats them
**together**: each soul is its own subagent, hears the others, pushes back, and finally
votes with a confidence it has to defend. Bounded by design: **4 rounds, never 5.**

**Where the shape comes from.** A 7-agent, 4-round, confidence-voted meeting that Boy
(Pinyo) ran inside his Oracle family. Only its parameters survived — 7 agents, 4 rounds,
a confidence vote at the end, reserved for expensive decisions. Mother Oracle rebuilt the
round prompts, the 1–10 scale and the aggregation rules from those parameters. So this
skill is *spiritually faithful, not forensically reproduced*: if better prompts turn up,
replace `prompts/` — don't defend them.

## Files

```text
round-table/
├── SKILL.md
├── prompts/round1-open.txt … round4-vote.txt   one template per round, {{slots}}
├── scripts/table.ts                            inspect (early stop) + vote (aggregate)
└── examples/adopt-a-pattern.json               worked example — must give 37/50
```

`SKILL_DIR` is the base directory printed above this skill.

## Step 0 — Is this a Round Table question?

Suggest `/oracle-prism` instead unless all three hold:

1. **A decision**, not a topic — something will be done differently depending on the answer.
2. **Canonical options**, 2–4 of them (`--options`). If the user gave none, propose them
   and wait for a yes.
3. **Stakes** — being wrong is expensive or hard to reverse.

"Should we …" phrasing is not consent to convene. Ask first.

Then find where the minute will live:

```bash
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
SLUG="$(date +%Y-%m-%d)_<short-slug-of-the-question>"
TABLE="$PSI/lab/round-table"; mkdir -p "$TABLE" "$PSI/inbox/decisions"
MINUTE="$TABLE/$SLUG.md"; STATE="$TABLE/$SLUG.json"
```

## Step 1 — Convene: seat the souls (3 to 8)

Quorum is 3 — two is a debate, one a monologue. Default to 5 when the user names no
roster. Every seat needs a **soul read from somewhere real — never invented**:

| Seat kind | Where the soul comes from |
|---|---|
| A persona file | any path the user gives (`resonance_<name>.md`, a character sheet, a SKILL.md) — read it whole |
| An Oracle in your fleet | if `maw` is installed: `R=$(maw locate <name> --path)` → `$R/ψ/memory/resonance/<name>.md`, else `$R/CLAUDE.md`'s identity section. Not found → refuse the seat and say so |
| A real person (multi-DNA) | one line — name + the single habit they bring — written or confirmed by the human |

Print the roster with each soul's source, the question, the options and the aggregator
(default `weighted`). Gather **every fact** the souls may use into `question_context`
now — there is no tool use during the rounds.

Create `$STATE` in the shape of `examples/adopt-a-pattern.json` (`id`, `question`,
`options`, `aggregator`, `agents[]` with `name`, `soul`, `rounds[]`) and start `$MINUTE`
with the roster. Flush both after every round, so one flaky subagent never costs the
earlier rounds. Persona files may be private — the minute stays in your ψ, not in a post.

## Step 2 — Rounds: one subagent per soul, all in parallel

For each round, fill that round's template from `$SKILL_DIR/prompts/` and launch **one
Agent call per soul, all in a single message**. Each prompt carries the full soul text,
the question, the options and the transcript so far. Subagents debate from soul + context
only — no tools.

| Round | Template | Each soul gets |
|---|---|---|
| 1 OPEN | `round1-open.txt` | soul, question, context — hears nobody |
| 2 DEEPEN | `round2-deepen.txt` | + every round-1 position; must challenge one by name |
| 3 CONVERGE | `round3-converge.txt` | + rounds 1–2, + 2–4 one-line disagreement axes that **you** extract |
| 4 VOTE | `round4-vote.txt` | + the full transcript; binding, 5 is forbidden |

Parse each reply as JSON. Malformed or off-option → re-prompt that soul once; a second
failure empties the seat and the minute says so. Append `{round, position, confidence,
self_update}` to that soul's `rounds` in `$STATE`, and the round to `$MINUTE`.

**After rounds 2 and 3, ask the inspector — don't eyeball it:**

```bash
bun "$SKILL_DIR/scripts/table.ts" inspect "$STATE"
```

| Output | Do |
|---|---|
| `EARLY-STOP` | everyone agrees at ≥ 8 — go straight to round 4 |
| `SKIP-ROUND-3` | nobody moved in round 2 — confirm no new evidence arrived, then vote |
| `EXPERT-DEFERENCE` | one soul at 10, the rest ≤ 3 — ask the human whether to short-circuit |
| `CONTINUE` | run the next round |

## Step 3 — Vote: the script counts, not the model

Write each soul's round-4 answer into `final` (`vote`, `confidence`, `rationale`) and
`dissent_note`, then:

```bash
bun "$SKILL_DIR/scripts/table.ts" vote "$STATE"
```

| Exit | Meaning | Do |
|---|---|---|
| 0 | decided | print the decision block |
| 2 | `RE-PROMPT` — a 5, an off-option vote, a bad number | re-ask only the named souls, vote again |
| 3 | `ESCALATE` | write the deadlock in plain words; the human breaks it |
| 1 | bad input, or fewer than 3 souls | fix `$STATE` |

What the script enforces:

- **`weighted`** (default) sums confidence per option · **`majority`** counts heads ·
  **`unanimity-or-escalate`** needs every soul on one side at ≥ 7.
- **Ties** break by highest single confidence, then fewer dissent notes, then the human —
  never an automatic pick.
- **Escalates under every aggregator** when the winner holds < 60% of the weighted
  confidence, when 10s land on opposite sides, or when a dissent cites a value
  (`honesty`, `safety`, `consent` — override with `values_keywords` in `$STATE`).
  The human decides the hard ones.

## Step 4 — The minute, and handing it back

Close `$MINUTE` with the vote table (soul · vote · confidence · rationale) and the
script's block verbatim, e.g.:

```text
DECISION: adopt-modified
Weighted confidence: 37/50 (74%) for adopt-modified
Top dissent: none (no opposing votes)
Top hedger: brand (6) — Compromise — would prefer as-is, but unity matters more
```

Write one line — the decision and the minute's path — to
`$PSI/inbox/decisions/$SLUG.md`, so `/recap` finds it. Then:

```bash
# announce-mode → absolute path (no ψ/, no ~/, no $VAR, no ...).
# Use: echo "marker: $RESOLVED_PATH"  — bash substitutes; never print $VAR literally. See CONVENTIONS.md.
echo "🪑 Minute: $MINUTE"
echo "📥 Decision: $PSI/inbox/decisions/$SLUG.md"
```

And step out of the table:

- **Every seat was a lens.** Write "the finance lens voted…", never "Finance decided…".
  The souls were worn by the convener; a seat is not that Oracle's or that person's real
  view. For a real view, ask them (`/talk-to` if you have a fleet).
- **A decision is advice.** The human ships, merges and signs — the table only recommends.

## Self-check

```bash
bun "$SKILL_DIR/scripts/table.ts" vote "$SKILL_DIR/examples/adopt-a-pattern.json"
```

Must print `DECISION: adopt-modified` and `37/50 (74%)` and exit 0 — the result the
reconstructed spec predicts for its worked example. Anything else means `table.ts` drifted.

## Not in scope

No tool use mid-round · no soul summoning another agent · no human interjection
mid-round · no round 5.

<!-- file: round-table/examples/adopt-a-pattern.json -->
### File: `round-table/examples/adopt-a-pattern.json`

```json
{
  "id": "2026-05-16_adopt-a-pattern",
  "question": "Should we adopt the borrowed persona pattern for our onboarding ritual?",
  "options": [
    "adopt-as-is",
    "adopt-modified",
    "reject"
  ],
  "aggregator": "weighted",
  "agents": [
    {
      "name": "facilitator",
      "soul": "(worked example — no soul file)",
      "rounds": [
        {
          "round": 1,
          "position": "adopt-modified",
          "confidence": 6
        },
        {
          "round": 2,
          "position": "adopt-modified",
          "confidence": 7,
          "self_update": "firmer"
        }
      ],
      "final": {
        "vote": "adopt-modified",
        "confidence": 8,
        "rationale": "Honest synthesis of the borrowed pattern, adapted to our voice"
      },
      "dissent_note": null
    },
    {
      "name": "brand",
      "soul": "(worked example — no soul file)",
      "rounds": [
        {
          "round": 1,
          "position": "adopt-as-is",
          "confidence": 8
        },
        {
          "round": 2,
          "position": "adopt-as-is",
          "confidence": 7,
          "self_update": "no change"
        }
      ],
      "final": {
        "vote": "adopt-modified",
        "confidence": 6,
        "rationale": "Compromise — would prefer as-is, but unity matters more"
      },
      "dissent_note": null
    },
    {
      "name": "engineer",
      "soul": "(worked example — no soul file)",
      "rounds": [
        {
          "round": 1,
          "position": "adopt-modified",
          "confidence": 7
        },
        {
          "round": 2,
          "position": "adopt-modified",
          "confidence": 7,
          "self_update": "no change"
        }
      ],
      "final": {
        "vote": "adopt-modified",
        "confidence": 9,
        "rationale": "Implementation plan agreed; risk acceptable"
      },
      "dissent_note": null
    },
    {
      "name": "editor",
      "soul": "(worked example — no soul file)",
      "rounds": [
        {
          "round": 1,
          "position": "adopt-modified",
          "confidence": 7
        },
        {
          "round": 2,
          "position": "adopt-modified",
          "confidence": 7,
          "self_update": "no change"
        }
      ],
      "final": {
        "vote": "adopt-modified",
        "confidence": 8,
        "rationale": "Thai polish layer added; quality protected"
      },
      "dissent_note": null
    },
    {
      "name": "finance",
      "soul": "(worked example — no soul file)",
      "rounds": [
        {
          "round": 1,
          "position": "reject",
          "confidence": 4
        },
        {
          "round": 2,
          "position": "adopt-modified",
          "confidence": 5,
          "self_update": "open to it with a review"
        }
      ],
      "final": {
        "vote": "adopt-modified",
        "confidence": 6,
        "rationale": "30-day review scheduled; reversible"
      },
      "dissent_note": null
    }
  ]
}
```

<!-- file: round-table/prompts/round1-open.txt -->
### File: `round-table/prompts/round1-open.txt`

```
You are a lens worn by the convener, speaking as {{persona_name}} at a Round Table.
Your soul, read from {{persona_soul_path}}:

{{persona_soul}}

The Round Table is convened on this question:

> {{question}}

CONTEXT (everything you may use — there is no tool use during the rounds):
{{question_context}}

The canonical options are: {{options}}

This is ROUND 1 of 4 — OPEN. You have not yet heard anyone else.
Speak only from your soul/DNA, in its voice. Do not hedge. Do not anticipate
what others will say. Do not invent facts that are not in CONTEXT.

Reply with JSON only:
{
  "position": "<one of the options — your current stance>",
  "reasoning": "<2-4 sentences grounded in your soul/DNA>",
  "confidence_now": <1-10>,
  "what_would_change_your_mind": "<one sentence — the evidence that would flip you>"
}
```

<!-- file: round-table/prompts/round2-deepen.txt -->
### File: `round-table/prompts/round2-deepen.txt`

```
You are a lens worn by the convener, speaking as {{persona_name}} at a Round Table.
Your soul, read from {{persona_soul_path}}:

{{persona_soul}}

Question: {{question}}
Options: {{options}}

Round 2 of 4 — DEEPEN.

The personas opened with these positions:

{{round_1_transcript}}

Pick the position you most disagree with. Critique it from your soul/DNA.
Then re-examine your own opening — does anything you heard sharpen, soften,
or shift your view? Be specific. Cite the persona by name when you agree
or disagree.

Reply with JSON only:
{
  "challenge": { "target": "<persona_name>", "critique": "<2-3 sentences>" },
  "self_update": "<what changed, or exactly \"no change\">",
  "position": "<one of the options — your stance now>",
  "reasoning": "<2-4 sentences>",
  "confidence_now": <1-10>
}
```

<!-- file: round-table/prompts/round3-converge.txt -->
### File: `round-table/prompts/round3-converge.txt`

```
You are a lens worn by the convener, speaking as {{persona_name}} at a Round Table.
Your soul, read from {{persona_soul_path}}:

{{persona_soul}}

Question: {{question}}
Options: {{options}}

Round 3 of 4 — CONVERGE.

Round 1 + Round 2 transcript:

{{rounds_1_2_transcript}}

The room now disagrees along these axes:
{{disagreement_axes}}

Your task: identify which axis matters most to your vote.
Acknowledge any coalition you find yourself in. State the
ONE condition under which you would vote the opposite way.
This is your last chance to shift before the vote.

Reply with JSON only:
{
  "axis_that_decides_my_vote": "<one sentence>",
  "coalition_with": ["<persona_name>", ...],
  "flip_condition": "<the one thing that would make you vote the other way>",
  "position": "<one of the options — your stance now>",
  "confidence_now": <1-10>
}
```

<!-- file: round-table/prompts/round4-vote.txt -->
### File: `round-table/prompts/round4-vote.txt`

```
You are a lens worn by the convener, speaking as {{persona_name}} at a Round Table.
Your soul, read from {{persona_soul_path}}:

{{persona_soul}}

Question: {{question}}

Round 4 of 4 — VOTE. This is binding.

Full transcript:
{{full_transcript}}

No more debate. State your final vote and confidence.

Confidence scale:
  1-2 guessing · 3-4 leaning · 5 FORBIDDEN (pick 4 or 6 — show your lean)
  6-7 convinced · 8-9 strong · 10 only if reversal would violate a core value of your soul

Be honest — if you are at 6, say 6. Inflated confidence corrupts the aggregate.

Reply with JSON only:
{
  "final_vote": "<exactly one of: {{options}}>",
  "final_confidence": <1-10, never 5>,
  "one_line_rationale": "<= 140 chars — what you'd put in the minutes>",
  "dissent_note": "<only if voting against the emerging majority — else null>"
}
```

<!-- file: round-table/scripts/table.ts -->
### File: `round-table/scripts/table.ts`

```ts
#!/usr/bin/env bun
// Round Table arithmetic — the part that must not be left to judgment.
//   bun scripts/table.ts inspect STATE.json   early-stop check after round 2 or 3
//   bun scripts/table.ts vote    STATE.json   validate round 4 and aggregate
// STATE.json is the RoundTableState the skill keeps beside the minute.
// Exit: 0 decided / continue · 2 re-prompt needed · 3 escalate · 1 bad input.

type Round = { round: number; position: string; confidence: number; self_update?: string };
type Agent = {
  name: string; soul: string; rounds: Round[];
  final?: { vote: string; confidence: number; rationale: string };
  dissent_note?: string | null;
};
type State = {
  id: string; question: string; options: string[];
  aggregator: "majority" | "weighted" | "unanimity-or-escalate";
  values_keywords?: string[]; agents: Agent[];
};

const [mode, file] = process.argv.slice(2);
if (!["inspect", "vote"].includes(mode) || !file) {
  console.error("usage: bun scripts/table.ts inspect|vote STATE.json");
  process.exit(1);
}
const state: State = JSON.parse(await Bun.file(file).text());
if (state.agents.length < 3) {
  console.error(`quorum: ${state.agents.length} personas — a Round Table needs at least 3`);
  process.exit(1);
}

if (mode === "inspect") {
  const last = Math.max(...state.agents.map(a => a.rounds.length));
  const latest = state.agents.map(a => a.rounds.find(r => r.round === last));
  if (latest.some(r => !r)) { console.error(`round ${last}: not every persona has answered`); process.exit(1); }
  const rows = latest as Round[];
  const same = new Set(rows.map(r => r.position)).size === 1;
  if (same && rows.every(r => r.confidence >= 8)) {
    console.log(`EARLY-STOP: all hold "${rows[0].position}" at ≥8 after round ${last} — skip to round 4`);
  } else if (last === 2 && rows.every(r => (r.self_update ?? "").trim().toLowerCase() === "no change")) {
    console.log("SKIP-ROUND-3: nobody moved in round 2 — round 3 would be performative (confirm no new evidence)");
  } else {
    const ten = rows.filter(r => r.confidence === 10);
    if (ten.length === 1 && rows.filter(r => r !== ten[0]).every(r => r.confidence <= 3)) {
      const who = state.agents[rows.indexOf(ten[0])].name;
      console.log(`EXPERT-DEFERENCE: only ${who} is certain (10), the rest ≤3 — ask the human whether to short-circuit`);
    } else {
      console.log(`CONTINUE: round ${last} still divided — run round ${last + 1}`);
    }
  }
  process.exit(0);
}

// vote
const bad: string[] = [];
for (const a of state.agents) {
  const f = a.final;
  if (!f) { bad.push(`${a.name}: no final vote`); continue; }
  if (!state.options.includes(f.vote)) bad.push(`${a.name}: "${f.vote}" is not one of ${state.options.join(", ")}`);
  if (!Number.isInteger(f.confidence) || f.confidence < 1 || f.confidence > 10) bad.push(`${a.name}: confidence ${f.confidence} outside 1–10`);
  if (f.confidence === 5) bad.push(`${a.name}: 5 is forbidden in round 4 — re-prompt for 4 or 6`);
}
if (bad.length) { console.log("RE-PROMPT\n" + bad.map(b => "  " + b).join("\n")); process.exit(2); }

const votes = state.agents.map(a => ({ name: a.name, ...a.final!, dissent: a.dissent_note ?? null }));
const sum = (o: string) => votes.filter(v => v.vote === o).reduce((s, v) => s + v.confidence, 0);
const count = (o: string) => votes.filter(v => v.vote === o).length;
const score = state.aggregator === "majority" ? count : sum;
const ranked = [...state.options].sort((a, b) => score(b) - score(a));

const reasons: string[] = [];
let winner: string | null = ranked[0];
const tied = state.options.filter(o => score(o) === score(ranked[0]));
if (tied.length > 1) {
  const top = (o: string) => Math.max(0, ...votes.filter(v => v.vote === o).map(v => v.confidence));
  const best = Math.max(...tied.map(top));
  let left = tied.filter(o => top(o) === best);
  if (left.length > 1) {
    const dissents = (o: string) => votes.filter(v => v.vote === o && v.dissent).length;
    const fewest = Math.min(...left.map(dissents));
    left = left.filter(o => dissents(o) === fewest);
  }
  if (left.length > 1) { winner = null; reasons.push(`tie between ${left.join(" and ")} survives every tie-break`); }
  else winner = left[0];
}

const total = votes.reduce((s, v) => s + v.confidence, 0);
const share = winner ? sum(winner) / total : 0;
if (winner && share < 0.6) reasons.push(`split: ${winner} holds ${(share * 100).toFixed(0)}% of weighted confidence (< 60%)`);
const tens = new Set(votes.filter(v => v.confidence === 10).map(v => v.vote));
if (tens.size > 1) reasons.push(`opposing certainties: 10s on ${[...tens].join(" and ")}`);
const keys = (state.values_keywords ?? ["honesty", "safety", "consent"]).map(k => k.toLowerCase());
for (const v of votes) {
  const hit = keys.find(k => (v.dissent ?? "").toLowerCase().includes(k));
  if (hit) reasons.push(`${v.name}'s dissent cites a value: "${hit}"`);
}
if (state.aggregator === "unanimity-or-escalate" && !(new Set(votes.map(v => v.vote)).size === 1 && votes.every(v => v.confidence >= 7))) {
  reasons.push("unanimity-or-escalate: not every persona voted the same side at ≥7");
}

const max = votes.length * 10;
const tally = state.options.map(o => `${o}: ${sum(o)}`).join(" · ");
console.log(`DECISION: ${reasons.length ? "ESCALATE" : winner}`);
console.log(`Aggregator: ${state.aggregator} · ${tally}`);
if (winner) console.log(`Weighted confidence: ${sum(winner)}/${max} (${Math.round(sum(winner) / max * 100)}%) for ${winner}`);
const against = votes.filter(v => v.vote !== winner).sort((a, b) => b.confidence - a.confidence)[0];
console.log(`Top dissent: ${against ? `${against.name} (${against.vote}, ${against.confidence}) — ${against.rationale}` : "none (no opposing votes)"}`);
const hedger = votes.filter(v => v.vote === winner).sort((a, b) => a.confidence - b.confidence)[0];
if (hedger) console.log(`Top hedger: ${hedger.name} (${hedger.confidence}) — ${hedger.rationale}`);
if (reasons.length) console.log("Escalate because:\n" + reasons.map(r => "  " + r).join("\n") + "\nThe human decides.");
process.exit(reasons.length ? 3 : 0);
```
