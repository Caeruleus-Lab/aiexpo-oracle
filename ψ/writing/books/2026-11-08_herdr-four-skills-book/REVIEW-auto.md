# REVIEW-auto — mechanical checks (verify.py), no LLM

748 findings in 9 chapters · token 29 · code 719

09-code.md:11 [code] tag ```markdown: use bash, zsh or none
09-code.md:14 [code] 1185 chars (max 76): description: Create a git worktree for a distinct 
09-code.md:15 [code] 80 chars (max 76): argument-hint: "<slug> [base-ref] [--here] [--no-i
09-code.md:20 [code] 88 chars (max 76): Works in any repo on any machine. Requires `herdr`
09-code.md:28 [code] 227 chars (max 76): | **home** | the repo you run `/herdr-wt` FROM: yo
09-code.md:31 [code] 89 chars (max 76): **The herdr space is always a worktree of HOME.** 
09-code.md:33 [code] 91 chars (max 76): `herdr worktree create --cwd <target>` lands in th
09-code.md:34 [code] 95 chars (max 76): owns the work. Home ≠ target → use *Under the orac
09-code.md:35 [code] 87 chars (max 76): in home, agent pane split into the code worktree).
09-code.md:41 [code] 82 chars (max 76): | 10-06 | floodboy-ops space `wQ` lost its worktre
09-code.md:42 [code] 94 chars (max 76): | 10-11 | herdr-board moved spaces with `workspace
09-code.md:45 [code] 103 chars (max 76): | 10-30 | reply-desk, messenger-archive#56, run by
09-code.md:47 [code] 88 chars (max 76): The 10-21 case added *Under the oracle*, but as pr
09-code.md:48 [code] 91 chars (max 76): copies; the 10-30 run copied the block from inside
09-code.md:49 [code] 85 chars (max 76): now checks it: *Run it* stops with exit 2 when hom
09-code.md:54 [code] 86 chars (max 76): `herdr worktree list` is the only surface that sho
09-code.md:55 [code] 88 chars (max 76): draws open spaces only, so a worktree you closed i
09-code.md:56 [code] 90 chars (max 76): disk, still registered in git, and one `herdr work
09-code.md:57 [code] 87 chars (max 76): `open_workspace_id` is present when a space is ope
09-code.md:62 [code] 82 chars (max 76): | [ (if .open_workspace_id then "OPEN " + .open_wo
09-code.md:65 [code] 90 chars (max 76): (.path | sub("^" + (env.PWD | sub("/wt/.*$";"")); 
09-code.md:70 [code] 88 chars (max 76): Scoped to ONE repo — the response's `source` block
09-code.md:71 [code] 84 chars (max 76): cwd. It will not show another oracle's worktrees; 
09-code.md:73 [code] 88 chars (max 76): `is_prunable` is the column that matters: it flags
09-code.md:78 [code] 90 chars (max 76): `/herdr-wt <slug>` runs these five steps in order.
09-code.md:80 [code] 86 chars (max 76): 1. **Issue first** — check the current repo, open 
09-code.md:81 [code] 91 chars (max 76): context of the task (section below). `--no-issue` 
09-code.md:83 [code] 88 chars (max 76): 2. **Worktree** — first *Step 0*: if the code live
09-code.md:84 [code] 128 chars (max 76): from, use *Under the oracle*, not *Run it*. Otherw
09-code.md:85 [code] 87 chars (max 76): in `ψ/lab/<slug>/` inside it (the default). `--rep
09-code.md:87 [code] 91 chars (max 76): 3. **Record the workspace on the issue** — one com
09-code.md:88 [code] 88 chars (max 76): 4. **Agent** — warm direnv, `pane run "claude"`, r
09-code.md:89 [code] 85 chars (max 76): 5. **Brief from the issue** — send the agent a sho
09-code.md:90 [code] 83 chars (max 76): The issue is the brief; the prompt only says where
09-code.md:92 [code] 89 chars (max 76): Why an issue and not just a long prompt: a prompt 
09-code.md:93 [code] 89 chars (max 76): scrollback and dies with it. Nobody else can read 
09-code.md:94 [code] 85 chars (max 76): issue is durable, linkable, and readable by the hu
09-code.md:95 [code] 88 chars (max 76): agent, and the eventual PR closes it with `Closes 
09-code.md:96 [code] 91 chars (max 76): (presentation, proof-with-coding) were each briefe
09-code.md:105 [code] 80 chars (max 76): -q '"\(.nameWithOwner) issues=\(.hasIssuesEnabled)
09-code.md:112 [code] 91 chars (max 76): - `viewerPermission` is `ADMIN`, `MAINTAIN` or `WR
09-code.md:113 [code] 87 chars (max 76): of. **Never open issues on a third-party repo** (f
09-code.md:116 [code] 92 chars (max 76): The body must stand alone: an agent that reads onl
09-code.md:121 [code] 88 chars (max 76): LABEL=$(gh label list --limit 100 --json name -q '
09-code.md:122 [code] 78 chars (max 76): ISSUE_URL=$(gh issue create --repo "$REPO" --title
09-code.md:128 [code] 90 chars (max 76): <why this exists; decisions already made; what was
09-code.md:137 [code] 89 chars (max 76): - <hard constraints: data it must not use, things 
09-code.md:155 [code] 92 chars (max 76): Keep the `--body-file -` heredoc form: long bodies
09-code.md:156 [code] 93 chars (max 76): where `--body "..."` gets mangled by the shell. Th
09-code.md:159 [code] 78 chars (max 76): Then run *Run it* below with `ISSUE` set, and afte
09-code.md:172 [code] 92 chars (max 76): Copy-paste, substituting the slug (and optionally 
09-code.md:173 [code] 91 chars (max 76): to the lock reason so the worktree can be traced b
09-code.md:177 [code] 103 chars (max 76): repo=$(dirname "$(git rev-parse --path-format=abso
09-code.md:178 [code] 91 chars (max 76): # Step 0 guard: home = the repo of YOUR pane (not 
09-code.md:179 [code] 142 chars (max 76): HOME_REPO=${HOME_REPO:-$(herdr pane get "$HERDR_PA
09-code.md:180 [code] 90 chars (max 76): home=$(dirname "$(git -C "$HOME_REPO" rev-parse --
09-code.md:181 [code] 157 chars (max 76): [ "$repo" = "$home" ] || { echo "STOP: code is in 
09-code.md:184 [code] 100 chars (max 76): name="$SLUG-$owner${ISSUE:+-issue$ISSUE}-$day"   #
09-code.md:187 [code] 95 chars (max 76): herdr worktree create --cwd "$repo" --branch "$nam
09-code.md:188 [code] 136 chars (max 76): | python3 -c "import json,sys; print('space', json
09-code.md:189 [code] 120 chars (max 76): git -C "$repo" worktree lock --reason "herdr|$(who
09-code.md:190 [code] 124 chars (max 76): [ -f "$dest/.envrc" ] || [ ! -f "$repo/.envrc" ] |
09-code.md:191 [code] 104 chars (max 76): (cd "$dest" && maw token use "$(maw token resolve)
09-code.md:192 [code] 83 chars (max 76): lab=""                                  # lab fold
09-code.md:199 [code] 97 chars (max 76): && { echo "$lab still ignored: a parent dir is exc
09-code.md:203 [code] 255 chars (max 76): herdr workspace list | python3 -c "import json,sys
09-code.md:206 [code] 87 chars (max 76): **`repo` is the main checkout, from `--git-common-
09-code.md:207 [code] 88 chars (max 76): inside a worktree, `--show-toplevel` returns that 
09-code.md:208 [code] 90 chars (max 76): `dest` nests as `<repo>/wt/<a>/wt/<b>` (the JSONDe
09-code.md:209 [code] 84 chars (max 76): create` answered with empty stdout), and `owner` b
09-code.md:211 [code] 90 chars (max 76): `worktree-calm-meadow-eea9`, `--git-common-dir` ga
09-code.md:214 [code] 84 chars (max 76): **New work goes in `ψ/lab/<slug>/`** (Nat, 2026-09
09-code.md:216 [code] 89 chars (max 76): (`!ψ/lab/codex-fleet/` in homelab), so the block a
09-code.md:217 [code] 89 chars (max 76): and stops if git still ignores it. That `.gitignor
09-code.md:220 [code] 90 chars (max 76): The lock is borrowed from `/incubate` (same `tool|
09-code.md:221 [code] 91 chars (max 76): reads both). It is **not** security — it is a "do 
09-code.md:224 [code] 84 chars (max 76): - `git worktree prune` leaves it registered **even
09-code.md:225 [code] 84 chars (max 76): Without a lock, prune is exactly what silently dro
09-code.md:230 [code] 91 chars (max 76): The lock reason is also the only per-worktree meta
09-code.md:231 [code] 85 chars (max 76): `<repo>/.git/worktrees/<id>/locked`, where `<id>` 
09-code.md:232 [code] 90 chars (max 76): (a later `git worktree move` keeps it). `git -C <w
09-code.md:242 [code] 94 chars (max 76): **In `laris-co/neo-oracle` only**, the same thing 
09-code.md:243 [code] 86 chars (max 76): No other repo has that recipe — verified across th
09-code.md:249 [code] 87 chars (max 76): herdr pane run <pane> 'echo "TOK=$CLAUDE_TOKEN_NAM
09-code.md:250 [code] 77 chars (max 76): herdr pane run <pane> "claude"          # NOT `her
09-code.md:254 [code] 87 chars (max 76): That first throwaway command is not decoration — w
09-code.md:255 [code] 90 chars (max 76): on the wrong token even though you used `pane run`
09-code.md:259 [code] 88 chars (max 76): `{"error":{"code":"agent_not_found",...}}` — the c
09-code.md:260 [token] pane `w6K:p1` is in no capture/BRIEF
09-code.md:263 [token] pid `40000` is in no capture/BRIEF
09-code.md:263 [code] 91 chars (max 76): herdr pane wait-output <pane> --match 'bypass perm
09-code.md:267 [code] 88 chars (max 76): `--timeout` is in **milliseconds**. The earlier `-
09-code.md:268 [token] pane `w6Q:p1` is in no capture/BRIEF
09-code.md:268 [token] pane `w6R:p1` is in no capture/BRIEF
09-code.md:268 [code] 88 chars (max 76): every time, even with claude already up (measured 
09-code.md:273 [code] 91 chars (max 76): Send it through fleet (`fleet_send`, target = the 
09-code.md:274 [code] 80 chars (max 76): prefix-matches agent names. Keep the prompt short;
09-code.md:280 [code] 90 chars (max 76): Report progress as comments on that issue (what is
09-code.md:281 [code] 106 chars (max 76): Work only in this worktree, commit on this branch.
09-code.md:284 [code] 89 chars (max 76): Anything you learn later that changes the task goe
09-code.md:285 [code] 91 chars (max 76): into the pane with a one-line "see the new comment
09-code.md:287 [code] 82 chars (max 76): **Do not use `herdr agent start` here**, despite i
09-code.md:290 [code] 85 chars (max 76): - **It bypasses direnv.** `herdr agent start` spaw
09-code.md:291 [code] 83 chars (max 76): environment, not through the pane's shell, so the 
09-code.md:292 [code] 81 chars (max 76): runs. The agent inherits whatever token the server
09-code.md:300 [code] 86 chars (max 76): `herdr pane run` goes through the shell, direnv fi
09-code.md:301 [code] 82 chars (max 76): - **Its `<name>` argument caps at 32 characters** 
09-code.md:305 [code] 79 chars (max 76): {"error":{"code":"invalid_agent_name","message":"a
09-code.md:306 [code] 79 chars (max 76): lowercase letter and contain only lowercase letter
09-code.md:310 [code] 82 chars (max 76): It **starts the agent anyway and leaves it unnamed
09-code.md:311 [code] 83 chars (max 76): side effect. Name the agent `<slug>-<owner>`; the 
09-code.md:316 [code] 89 chars (max 76): Use it when the human wants a second parallel agen
09-code.md:317 [code] 89 chars (max 76): but **not** in the same checkout. Two agents in on
09-code.md:318 [code] 85 chars (max 76): index, so one `git add` stages the other's half-do
09-code.md:321 [code] 88 chars (max 76): Everything else in the flow is unchanged: issue fi
09-code.md:324 [code] 88 chars (max 76): 1. **`git worktree add`, not `herdr worktree creat
09-code.md:326 [code] 87 chars (max 76): 2. **`pane split --cwd <dest>`**, so the new pane 
09-code.md:331 [code] 96 chars (max 76): main=$(dirname "$(git rev-parse --path-format=abso
09-code.md:338 [code] 120 chars (max 76): git -C "$main" worktree lock --reason "herdr|$(who
09-code.md:339 [code] 87 chars (max 76): [ -f "$dest/.envrc" ] || [ ! -f "$main/.envrc" ] |
09-code.md:342 [code] 91 chars (max 76): PANE=$(herdr pane split --current --direction "$DI
09-code.md:343 [code] 90 chars (max 76): | python3 -c "import json,sys;print(json.load(sys.
09-code.md:348 [code] 91 chars (max 76): Then run the lab-folder block from *Run it* agains
09-code.md:349 [code] 86 chars (max 76): agent in it* using `$PANE`. Use `--direction down`
09-code.md:351 [code] 92 chars (max 76): - **Use `--git-common-dir`, not `--show-toplevel`.
09-code.md:352 [code] 90 chars (max 76): that worktree, so `$toplevel/wt/...` would nest th
09-code.md:353 [code] 90 chars (max 76): Herdr's own spaces live in `~/.herdr/worktrees/<re
09-code.md:354 [code] 84 chars (max 76): - **The sidebar shows no new row.** The pane belon
09-code.md:355 [code] 78 chars (max 76): still shows the current branch. Check the new bran
09-code.md:357 [code] 84 chars (max 76): - **Splitting a pane is not `--here`.** Right-clic
09-code.md:358 [code] 88 chars (max 76): `--cwd`, opens the SAME worktree. A fresh `claude`
09-code.md:361 [token] pane `w2J:p4` is in no capture/BRIEF
09-code.md:361 [token] pane `w2J:t1` is in no capture/BRIEF
09-code.md:361 [code] 77 chars (max 76): Tested 2026-10-08 on a scratch repo: `w2J:p4` open
09-code.md:364 [code] 77 chars (max 76): ### `--here` with no slug: the agent names it, the
09-code.md:368 [code] 84 chars (max 76): 1. **Pick the slug yourself.** Base it on what the
09-code.md:369 [code] 80 chars (max 76): pane for, then on the conversation. Draft 3 slugs,
09-code.md:370 [code] 84 chars (max 76): memorable (`kong-cutover`, `fts-stopword-purge`), 
09-code.md:372 [code] 85 chars (max 76): 2. **Cut the worktree with the best pick right awa
09-code.md:373 [code] 85 chars (max 76): run only the lines up to and including `git worktr
09-code.md:377 [code] 85 chars (max 76): `Keep <slug> (Recommended)`, options 2-3 are the r
09-code.md:379 [code] 85 chars (max 76): 4. **If the human picks another name, move the who
09-code.md:389 [code] 85 chars (max 76): Set `SLUG` to the final pick too. The lock reason 
09-code.md:392 [code] 86 chars (max 76): Tested 2026-10-08 on a scratch repo: `rc=0`, and `
09-code.md:394 [code] 87 chars (max 76): 5. **Then the rest of the `--here` block, from `gi
09-code.md:396 [code] 90 chars (max 76): label. Lock **after** the popup, because `git work
09-code.md:398 [code] 77 chars (max 76): `git worktree move` keeps the admin dir under its 
09-code.md:401 [code] 88 chars (max 76): `cat "$(git -C "$dest" rev-parse --git-dir)/locked
09-code.md:404 [code] 82 chars (max 76): Name, folder, branch, label and lock reason all ag
09-code.md:407 [code] 90 chars (max 76): **No evidence at all** (the human said nothing abo
09-code.md:412 [code] 99 chars (max 76): "$(shuf -n1 -e dune fern meadow river valley)" "$(
09-code.md:415 [code] 85 chars (max 76): - **Skip the issue** for a placeholder (implied `-
09-code.md:416 [code] 79 chars (max 76): With an AI-picked slug, open the issue after the p
09-code.md:417 [code] 85 chars (max 76): - **Name a placeholder later with `/herdr-rename` 
09-code.md:418 [code] 84 chars (max 76): renames `git branch --show-current` of the pane it
09-code.md:421 [code] 87 chars (max 76): What a later rename changes and what it leaves beh
09-code.md:428 [code] 80 chars (max 76): | folder `wt/<placeholder>…` | **unchanged** (movi
09-code.md:430 [token] pane `w2J:p6` is in no capture/BRIEF
09-code.md:430 [code] 108 chars (max 76): | pane label | follows: `/herdr-rename` step 3 ren
09-code.md:432 [code] 86 chars (max 76): `git branch -m` also works from a different worktr
09-code.md:433 [code] 84 chars (max 76): from the main checkout, and the other worktree's p
09-code.md:438 [code] 97 chars (max 76): The oracle sits in its own repo, but the code live
09-code.md:439 [code] 92 chars (max 76): feature in the fork `Soul-Brews-Studio/herdr` (iss
09-code.md:440 [code] 93 chars (max 76): `repo=<that repo's main checkout>` instead of the 
09-code.md:444 [code] 368 chars (max 76): | sidebar row | **must nest under the ORACLE** (Na
09-code.md:445 [code] 329 chars (max 76): | the issue | open it in the **oracle's** repo whe
09-code.md:446 [code] 150 chars (max 76): | `gh repo view` | run it as `gh repo view <owner/
09-code.md:447 [code] 284 chars (max 76): | `.envrc` / token | the target repo has no `.envr
09-code.md:448 [code] 297 chars (max 76): | keep `.envrc` out of git | `echo .envrc >> "$(gi
09-code.md:449 [code] 153 chars (max 76): | report back | the brief ends with `maw hey <orac
09-code.md:451 [code] 82 chars (max 76): ### Under the oracle — space from the oracle, pane
09-code.md:453 [code] 110 chars (max 76): The fm-gw run (laris-meshtastic#3) first opened it
09-code.md:454 [code] 108 chars (max 76): so the sidebar showed it under `laris-meshtastic`.
09-code.md:455 [code] 110 chars (max 76): and this is the recipe from now on. It works becau
09-code.md:461 [code] 82 chars (max 76): git -C "$target" worktree lock --reason "herdr|…|$
09-code.md:462 [code] 83 chars (max 76): # 2. the SPACE: a worktree of the ORACLE repo, sam
09-code.md:463 [code] 92 chars (max 76): WS=$(herdr worktree create --cwd "$oracle" --branc
09-code.md:464 [code] 95 chars (max 76): --path "$oracle/wt/$SLUG-$owner-$day" --no-focus |
09-code.md:465 [code] 94 chars (max 76): ln -s "$target/wt/$name" "$oracle/wt/$SLUG-$owner-
09-code.md:466 [code] 108 chars (max 76): echo "/<repo>-$SLUG" >> "$(git -C "$oracle" rev-pa
09-code.md:468 [code] 108 chars (max 76): SHELL=$(herdr pane list | jq -r --arg w "$WS" '.re
09-code.md:469 [code] 116 chars (max 76): PANE=$(herdr pane split "$SHELL" --direction right
09-code.md:475 [code] 138 chars (max 76): herdr workspace list | jq -r --arg w "$WS" '.resul
09-code.md:478 [code] 96 chars (max 76): A team desk is an oracle here: the rd-team desk wo
09-code.md:479 [code] 93 chars (max 76): made space `wBC` from `rd-team` (`reply-desk-rd-te
09-code.md:480 [code] 93 chars (max 76): worktree as `messenger-archive-reply-desk/`, and s
09-code.md:481 [code] 93 chars (max 76): helper for the same work (`just desk`) goes in the
09-code.md:484 [code] 106 chars (max 76): Then `.envrc` + `maw token use` in BOTH worktrees,
09-code.md:485 [code] 109 chars (max 76): oracle space's own first pane stays as the agent's
09-code.md:486 [code] 77 chars (max 76): target repo; the oracle worktree only carries note
09-code.md:488 [code] 89 chars (max 76): **Repairing one that already landed under the targ
09-code.md:489 [code] 91 chars (max 76): (not briefed yet), do not move it: `/exit` it, `he
09-code.md:490 [code] 92 chars (max 76): locked code worktree stays), and run the recipe ab
09-code.md:491 [code] 101 chars (max 76): `wBC`), no live pane moved. If the agent is mid-wo
09-code.md:492 [code] 102 chars (max 76): create the oracle space as in step 2, then `herdr 
09-code.md:493 [code] 108 chars (max 76): <its shell> --split right`, close the leftover pan
09-code.md:494 [token] pane `wV:p1` is in no capture/BRIEF
09-code.md:494 [token] pane `wW:p2` is in no capture/BRIEF
09-code.md:496 [code] 90 chars (max 76): Starting claude in a folder it has never seen show
09-code.md:497 [token] pane `wBF:p1` is in no capture/BRIEF
09-code.md:497 [code] 90 chars (max 76): blocks `wait-output --match 'bypass permissions'` 
09-code.md:498 [code] 93 chars (max 76): throwaway `echo TOK=` command, start claude, wait 
09-code.md:499 [code] 93 chars (max 76): and if it is the trust prompt send `herdr pane sen
09-code.md:500 [code] 90 chars (max 76): we own. If the first `echo TOK=` prints an empty v
09-code.md:501 [code] 80 chars (max 76): (direnv evaluated the shell before `maw token use`
09-code.md:505 [code] 86 chars (max 76): Without `--repo`, work lands in `ψ/lab/<slug>/` in
09-code.md:506 [code] 81 chars (max 76): gets its own repo. Everything else is the normal f
09-code.md:507 [code] 79 chars (max 76): `<repo>/wt/`, agent, brief. **The main session doe
09-code.md:508 [code] 91 chars (max 76): 2026-09-28); the agent in the worktree does, becau
09-code.md:509 [code] 78 chars (max 76): in the current repo, because the new repo's name n
09-code.md:514 [code] 93 chars (max 76): oracle=homekeeper   # the oracle's own name (CLAUD
09-code.md:515 [code] 79 chars (max 76): [ -n "$ORG" ] || ORG=$(maw locate "$oracle" --json
09-code.md:516 [code] 84 chars (max 76): || { echo "oracle '$oracle' not in the maw registr
09-code.md:518 [code] 79 chars (max 76): echo "$names" | rg "^$oracle-$SLUG-issue[0-9]+$"  
09-code.md:519 [code] 104 chars (max 76): echo "$names" | rg -F -- "$SLUG"                  
09-code.md:522 [code] 92 chars (max 76): - **Exact hit**: the agent will run `/incubate $OR
09-code.md:523 [code] 89 chars (max 76): issue number, which is when the repo was born. A n
09-code.md:527 [code] 87 chars (max 76): `/incubate` creates the private repo when it does 
09-code.md:529 [code] 88 chars (max 76): Put that exact `/incubate` command in the issue as
09-code.md:530 [code] 87 chars (max 76): issue's URL to the new repo's README" as the secon
09-code.md:531 [code] 91 chars (max 76): minus the lab block (set `lab=""`, skip the `if`).
09-code.md:532 [code] 81 chars (max 76): with the others, and `/incubate` run from it links
09-code.md:535 [code] 94 chars (max 76): Do **not** open a bare space on the main checkout 
09-code.md:536 [code] 91 chars (max 76): Tried 2026-09-28 (space `w6Q`, closed): it lands i
09-code.md:539 [code] 83 chars (max 76): The agent's name is `$SLUG-$owner`, or just `$SLUG
09-code.md:543 [code] 86 chars (max 76): `laris-co/homekeeper-oracle` was in ghq and in the
09-code.md:544 [code] 80 chars (max 76): folder is an old clone of `laris-co/homelab`. `maw
09-code.md:545 [code] 88 chars (max 76): (`register-free-cloud` gives `not found in 313 reg
09-code.md:550 [code] 86 chars (max 76): `wt/` is already ignored **fleet-wide** via `~/.co
09-code.md:551 [code] 84 chars (max 76): Git reads that path by XDG default when `core.excl
09-code.md:552 [code] 88 chars (max 76): `.gitignore` edit is needed — one line covers ever
09-code.md:559 [code] 84 chars (max 76): The leading slash anchors it to each repo's root, 
09-code.md:562 [code] 83 chars (max 76): **`dig.py` must fold `wt`** or every worktree repo
09-code.md:571 [code] 87 chars (max 76): The original required a **digit** right after `wt-
09-code.md:572 [code] 86 chars (max 76): `wt-herdr-14sep-mon2026`. Session dirs then fall t
09-code.md:573 [code] 86 chars (max 76): report as a phantom repo — exactly why `homelab-ag
09-code.md:578 [code] 87 chars (max 76): Decided against the obvious alternatives, with evi
09-code.md:581 [code] 87 chars (max 76): **Date goes LAST.** maw's own day repos are date-f
09-code.md:584 [code] 84 chars (max 76): 1. *Date-first does not sort chronologically.* maw
09-code.md:585 [code] 80 chars (max 76): (`1sep-tue2026` … `9sep-tue2026`), so `9sep` sorts
09-code.md:587 [code] 85 chars (max 76): 2. *Trailing it groups by topic* — every `herdr-*`
09-code.md:590 [code] 87 chars (max 76): Not an inconsistency with maw: its date-first name
09-code.md:591 [code] 89 chars (max 76): the identity. A worktree is **task-scoped** — the 
09-code.md:593 [code] 85 chars (max 76): **Slug FIRST, then the oracle** (changed 2026-09-2
09-code.md:594 [code] 89 chars (max 76): name — a branch, a PR and `git worktree list` are 
09-code.md:595 [code] 88 chars (max 76): does not say whose it is. But it must not lead, be
09-code.md:596 [code] 88 chars (max 76): now** and truncates from the right: under a `neo-o
09-code.md:597 [code] 84 chars (max 76): the prefix spent ~4 of ~9 visible characters repea
09-code.md:599 [code] 84 chars (max 76): Measured over 38 live workspaces, collisions *with
09-code.md:608 [code] 86 chars (max 76): `neo-herdr…` for both `neo-herdr-14sep` and `neo-h
09-code.md:611 [code] 87 chars (max 76): `neo-oracle` → `neo`; a non-oracle repo keeps its 
09-code.md:613 [code] 87 chars (max 76): The earlier rationale said the sidebar "lists spac
09-code.md:614 [code] 89 chars (max 76): and is not true now; it is a three-level tree (Loc
09-code.md:617 [code] 87 chars (max 76): **Issue number between oracle and date** (`-issue2
09-code.md:618 [code] 86 chars (max 76): names its own brief: `register-free-cloud-homelab-
09-code.md:619 [code] 85 chars (max 76): without opening anything. Written `issue23`, not `
09-code.md:622 [code] 90 chars (max 76): **A new repo (`--repo`) is `<oracle>-<slug>-issue<
09-code.md:623 [code] 84 chars (max 76): (Nat, 2026-09-28): `homekeeper-register-free-cloud
09-code.md:624 [code] 94 chars (max 76): `ghq list` are flat and alphabetical, with no pare
09-code.md:625 [code] 94 chars (max 76): what keeps one oracle's repos together. A repo out
09-code.md:626 [code] 85 chars (max 76): on the worktree and branch, and the issue number a
09-code.md:627 [code] 92 chars (max 76): `-issue<N>` tail also ends the slug, so `^homekeep
09-code.md:628 [code] 92 chars (max 76): that feature and never `register-free-cloud-api`. 
09-code.md:632 [code] 94 chars (max 76): `<oracle>-<slug>-<oracle>-issue<N>-<day>` (69 char
09-code.md:635 [code] 88 chars (max 76): **Location `<repo>/wt/`, not `~/.herdr/worktrees/`
09-code.md:636 [code] 87 chars (max 76): single global root it appends `<repo>/<branch>` to
09-code.md:637 [code] 83 chars (max 76): current repo". `--path` is the only lever. `wt` al
09-code.md:642 [code] 77 chars (max 76): A worktree is a **new path**, so direnv's allow-li
09-code.md:643 [code] 79 chars (max 76): though the parent repo is trusted and `.envrc` is 
09-code.md:644 [code] 79 chars (max 76): allow it, direnv refuses to load and every pane op
09-code.md:647 [code] 85 chars (max 76): `direnv allow "$dest"` fixes only half of that, so
09-code.md:656 [code] 78 chars (max 76): Proof for both halves. Trust: with the allow-file 
09-code.md:657 [token] conv `dc56099d` is in no capture/BRIEF
09-code.md:657 [code] 87 chars (max 76): recreated `~/.local/share/direnv/allow/dc56099d…` 
09-code.md:659 [token] conv `812ca807` is in no capture/BRIEF
09-code.md:659 [token] conv `bc2ed1aa` is in no capture/BRIEF
09-code.md:662 [code] 84 chars (max 76): Why the token half matters: the `.envrc` a worktre
09-code.md:663 [code] 86 chars (max 76): names whatever token the source checkout named at 
09-code.md:664 [code] 86 chars (max 76): trusts a stale answer. `maw token resolve` reads t
09-code.md:665 [code] 86 chars (max 76): it resolves correctly from inside a worktree, veri
09-code.md:672 [code] 85 chars (max 76): `CLAUDE_CODE_OAUTH_TOKEN`, `CLAUDE_TOKEN_NAME`, `O
09-code.md:673 [code] 87 chars (max 76): different environment than the shell that created 
09-code.md:674 [code] 86 chars (max 76): failure nobody can reproduce. Measured 2026-09-15 
09-code.md:692 [code] 82 chars (max 76): That proves what a *shell* at that path gets. It d
09-code.md:693 [code] 78 chars (max 76): agent got — those differ whenever the agent was st
09-code.md:694 [code] 80 chars (max 76): statusline is no help either: its `🔐<name>` marker
09-code.md:695 [code] 83 chars (max 76): displayed `🔐dd2` for an agent whose process actual
09-code.md:706 [code] 81 chars (max 76): c=$(lsof -a -p "$p" -d cwd -Fn 2>/dev/null | rg '^
09-code.md:713 [code] 89 chars (max 76): - **`pgrep -f claude` is too wide.** An agent's MC
09-code.md:714 [code] 81 chars (max 76): pattern returned 5 pids all reporting the worktree
09-code.md:715 [code] 83 chars (max 76): `python`, a `bun` plugin server, and the real `cla
09-code.md:716 [code] 86 chars (max 76): (wrong) `CLAUDE_TOKEN_NAME`, so the output looked 
09-code.md:719 [code] 92 chars (max 76): - **`rg '^n'` must be `rg '^n/'` and end in `head 
09-code.md:720 [code] 83 chars (max 76): fields; without the anchor and the head, `$c` can 
09-code.md:723 [code] 84 chars (max 76): Recovery is cheap when the agent is fresh: `herdr 
09-code.md:728 [code] 89 chars (max 76): The table above says `pane run` gets the right tok
09-code.md:729 [code] 91 chars (max 76): reached a **prompt after** `maw token use` allowed
09-code.md:740 [code] 86 chars (max 76): The sequence is the cause. `herdr worktree create`
09-code.md:741 [code] 84 chars (max 76): starts **immediately** — before `maw token use` ru
09-code.md:742 [code] 84 chars (max 76): prompt, finds the path untrusted, and refuses. All
09-code.md:743 [code] 83 chars (max 76): reach back into a shell that is already sitting at
09-code.md:744 [code] 87 chars (max 76): executes in a shell holding no repo environment an
09-code.md:746 [code] 87 chars (max 76): Fire one throwaway command first — any command, it
09-code.md:747 [code] 84 chars (max 76): fresh prompt, direnv evaluates against the now-tru
09-code.md:756 [code] 88 chars (max 76): If you skip it and find the agent on the wrong tok
09-code.md:757 [code] 85 chars (max 76): `herdr agent prompt <pane> '/exit'`, one throwaway
09-code.md:768 [code] 87 chars (max 76): Removes the checkout AND deregisters from `git wor
09-code.md:775 [code] 86 chars (max 76): If the worktree was ever **moved**, herdr's record
09-code.md:784 [code] 86 chars (max 76): A running agent pins its **cwd and Claude project 
09-code.md:785 [code] 88 chars (max 76): relocate cleanly — git metadata updates, herdr's p
09-code.md:786 [code] 85 chars (max 76): cannot follow. It points at a vanished path and si
09-code.md:788 [code] 88 chars (max 76): The tell is quiet: `pwd` inside the agent returns 
09-code.md:795 [token] commit `31d3ceb` is in no capture/BRIEF
09-code.md:798 [code] 87 chars (max 76): **Rule**: move while empty, or restart the agent a
09-code.md:799 [code] 87 chars (max 76): `ctrl+c` did NOT exit it), then `herdr pane run <p
09-code.md:804 [code] 89 chars (max 76): From herdr's source, `src/workspace.rs:196` — `wor
09-code.md:807 [code] 88 chars (max 76): Moving a worktree's pane into another space's tab 
09-code.md:808 [code] 87 chars (max 76): the indented nesting and inherits the destination'
09-code.md:812 [code] 81 chars (max 76): herdr worktree open --cwd <repo> --path <worktree-
09-code.md:815 [code] 91 chars (max 76): Adjacency and worktree identity are mutually exclu
09-code.md:817 [code] 97 chars (max 76): **Putting worktree agents side by side and back (`
09-code.md:818 [code] 88 chars (max 76): worktree spaces, so the nesting disappears while t
09-code.md:822 [code] 188 chars (max 76): herdr workspace list | python3 -c "import json,sys
09-code.md:825 [code] 94 chars (max 76): Any `FLAT` row that should be a worktree is repair
09-code.md:826 [code] 95 chars (max 76): untouched, by the `worktree open` above (`already_
09-code.md:827 [code] 104 chars (max 76): space). Measured 2026-10-06: herdr-room before its
09-code.md:828 [code] 110 chars (max 76): repaired this way. The 5th was registered to its o
09-code.md:833 [code] 87 chars (max 76): `git checkout -b` in a repo other agents are worki
09-code.md:834 [code] 81 chars (max 76): branch. That is what this skill exists to avoid — 
09-code.md:839 [code] 79 chars (max 76): Both cut worktrees; they do not merge and neither 
09-code.md:840 [code] 78 chars (max 76): **ownership of the repo**, and it decides where th
09-code.md:845 [code] 90 chars (max 76): | worktree path | `$XDG_STATE_HOME/incubate/worktr
09-code.md:850 [code] 86 chars (max 76): **Why incubate must stay outside and we may stay i
09-code.md:851 [code] 82 chars (max 76): `ghq list` decides "is this a repository" by `stat
09-code.md:852 [code] 87 chars (max 76): worktree's `.git` is a *file*, not a directory. A 
09-code.md:853 [code] 89 chars (max 76): registers as a phantom repo. Incubate clones *into
09-code.md:854 [code] 88 chars (max 76): to place bodies elsewhere. Our `wt/` sits inside a
09-code.md:855 [code] 87 chars (max 76): ghq entry, and it is gitignored, so nothing enumer
09-code.md:858 [code] 86 chars (max 76): **Picking one**: if you would open a herdr space f
09-code.md:864 [code] 92 chars (max 76): `wt/<oracle>-<slug>-<date>` branch off `origin/<de
09-code.md:865 [code] 90 chars (max 76): from the work you are about to start. If the issue
09-code.md:870 [code] 95 chars (max 76): - `/herdr-bring` — land an existing maw handle int
09-code.md:871 [code] 79 chars (max 76): - `herdr` (global skill) — the CLI reference: pane
09-code.md:879 [code] tag ```markdown: use bash, zsh or none
09-code.md:882 [code] 639 chars (max 76): description: Ensure a herdr presence for any maw h
09-code.md:888 [code] 77 chars (max 76): Puts a Claude Code process into its own herdr spac
09-code.md:889 [code] 80 chars (max 76): resolves to, on **this pane's own herdr server**. 
09-code.md:898 [code] 77 chars (max 76): whatever local history exists*. A handle that only
09-code.md:904 [code] 79 chars (max 76): test "${HERDR_ENV:-}" = 1 || { echo "not inside a 
09-code.md:907 [code] 78 chars (max 76): If that fails, say so and stop. Do not drive a her
09-code.md:911 [code] 77 chars (max 76): herdr sockets are per-server and ids do not collid
09-code.md:912 [code] 81 chars (max 76): the **calling pane's own socket** (`$HERDR_SOCKET_
09-code.md:913 [code] 78 chars (max 76): every pane it manages). An earlier version hardcod
09-code.md:915 [code] 78 chars (max 76): `default`. To target a different server on purpose
09-code.md:918 [code] 83 chars (max 76): Note the documented precedence: `--session` > `HER
09-code.md:919 [code] 79 chars (max 76): > default. A pane's own `HERDR_SOCKET_PATH` silent
09-code.md:923 [code] 77 chars (max 76): Show what exists before touching anything, even wh
09-code.md:930 [code] 95 chars (max 76): print(f\"{s['session']:30} {s['status']:8} panes={
09-code.md:934 [code] 79 chars (max 76): `status` is **tmux pane recency**, not whether a t
09-code.md:935 [code] 81 chars (max 76): read `active` while sitting idle, or `stale` while
09-code.md:944 [code] 79 chars (max 76): `maw locate` exits 1 on an ambiguous match while s
09-code.md:945 [code] 79 chars (max 76): a `candidates` list, so capture it with `|| true` 
09-code.md:946 [code] 80 chars (max 76): has `candidates`, print them and stop — do not pic
09-code.md:953 [code] 88 chars (max 76): LABEL="$HANDLE"          # or an explicit label; o
09-code.md:956 [code] 84 chars (max 76): test -n "$info" || { echo "REFUSING: maw locate $H
09-code.md:957 [code] 104 chars (max 76): python3 -c "import json,sys; sys.exit(0 if 'candid
09-code.md:961 [code] 116 chars (max 76): for c in json.load(sys.stdin)['candidates']: print
09-code.md:964 [code] 95 chars (max 76): repo=$(python3 -c "import json,sys; print(json.loa
09-code.md:965 [code] 104 chars (max 76): maw_session=$(python3 -c "import json,sys; print(j
09-code.md:970 [code] 80 chars (max 76): if [ -n "$maw_session" ] && tmux has-session -t "$
09-code.md:972 [code] 95 chars (max 76): # Busy check: Claude's own spinner line — a glyph,
09-code.md:973 [code] 104 chars (max 76): if tmux capture-pane -t "$maw_session" -p 2>/dev/n
09-code.md:974 [code] 82 chars (max 76): echo "REFUSING: $maw_session looks mid-turn — brin
09-code.md:978 [code] 80 chars (max 76): echo "maw session: ${maw_session:-<none>} (not liv
09-code.md:981 [code] 92 chars (max 76): # Newest transcript for that repo. Encoded path: l
09-code.md:983 [code] 81 chars (max 76): claude_sess=$(ls -t "$HOME/.claude/projects/$enc"/
09-code.md:987 [code] 96 chars (max 76): | python3 -c "import json,sys; print(json.load(sys
09-code.md:991 [code] 135 chars (max 76): test -n "$claude_sess" || { echo "REFUSING: $maw_s
09-code.md:997 [code] 81 chars (max 76): echo "mode      : resumed local history — nothing 
09-code.md:1006 [code] 127 chars (max 76): | python3 -c "import json,sys; print(json.load(sys
09-code.md:1009 [code] 144 chars (max 76): [ "$agent" = "claude" ] || { echo "!! claude did n
09-code.md:1014 [code] 77 chars (max 76): **Kill before resume, never the other order.** Res
09-code.md:1018 [code] 80 chars (max 76): The 40s poll is not padding: direnv on a cold pane
09-code.md:1026 [code] 79 chars (max 76): **Never sweep every name from step 1 without the u
09-code.md:1027 [code] 81 chars (max 76): confirming a bulk sweep.** Landing a handle that t
09-code.md:1028 [code] 80 chars (max 76): its maw side — real, and only somewhat reversible:
09-code.md:1030 [code] 78 chars (max 76): which mode a name falls into until the script reso
09-code.md:1040 [code] 80 chars (max 76): State plainly which of the three modes happened — 
09-code.md:1041 [code] 81 chars (max 76): resumed local history with nothing killed, or star
09-code.md:1042 [code] 80 chars (max 76): at all. These are different outcomes. Never paraph
09-code.md:1054 [code] 86 chars (max 76): Both print `CONFLICT`, list options, and exit **2*
09-code.md:1057 [code] 87 chars (max 76): **On exit 2, present the options with `AskUserQues
09-code.md:1065 [code] 79 chars (max 76): The label guard exists because of a real miss on 2
09-code.md:1067 [code] 86 chars (max 76): `laris-co/pulse-oracle` passed the cwd check (diff
09-code.md:1068 [code] 86 chars (max 76): space, and only then failed at `herdr agent rename
09-code.md:1069 [code] 83 chars (max 76): live unnamed space behind. A guard that fires afte
09-code.md:1071 [code] 88 chars (max 76): What that implies: a wrong label on one space sile
09-code.md:1072 [code] 86 chars (max 76): taking its own name. When the existing space is th
09-code.md:1077 [code] 94 chars (max 76): A herdr pane cannot cross sessions (`pane move` wo
09-code.md:1078 [code] 102 chars (max 76): starting the same conversation in the target sessi
09-code.md:1079 [code] 94 chars (max 76): Done 2026-10-05 for 5 live bodies (claude x4, code
09-code.md:1081 [code] 185 chars (max 76): 1. **Read the body.** Scheduled tasks or backgroun
09-code.md:1082 [code] 92 chars (max 76): turn dies.) Its pid and exact flags (`herdr --sess
09-code.md:1084 [code] 107 chars (max 76): 2. **New space in the target session at that cwd.*
09-code.md:1087 [code] 130 chars (max 76): 3. **Arm it.** `herdr --session T pane run NEW 'wh
09-code.md:1088 [code] 92 chars (max 76): (codex: `codex resume ID`, same bypass flags). The
09-code.md:1089 [code] 86 chars (max 76): 4. **End the old one.** `herdr --session S agent p
09-code.md:1090 [code] 104 chars (max 76): 5. **Check.** `/herdr-info <oracle>` -> `warnings:
09-code.md:1091 [code] 108 chars (max 76): close the old space only when EVERY pane in EVERY 
09-code.md:1096 [code] 284 chars (max 76): | `/exit` stops at "You have N unsent feedback dra
09-code.md:1097 [code] 432 chars (max 76): | `/exit` stops at "Background work is running … 1
09-code.md:1098 [code] 284 chars (max 76): | a body that holds a live Discord connection (`--
09-code.md:1099 [token] pane `w8:p2` is in no capture/BRIEF
09-code.md:1099 [code] 114 chars (max 76): | pane ids repeat across sessions (`w8:p2` existed
09-code.md:1100 [code] 164 chars (max 76): | `maw herdr join` / `break` act on the tab of the
09-code.md:1104 [code] 78 chars (max 76): - **The agent name is cleared when the pane's occu
09-code.md:1108 [code] 79 chars (max 76): `herdr agent rename <pane> <label>` and address pa
09-code.md:1109 [code] 77 chars (max 76): - **A plain workspace has NO `worktree` object.** 
09-code.md:1112 [code] 78 chars (max 76): `worktree` object at all; a space made by `herdr w
09-code.md:1114 [code] 80 chars (max 76): duplicate you were guarding against. Hit for real 
09-code.md:1120 [code] 108 chars (max 76): print([p['workspace_id'] for p in json.load(sys.st
09-code.md:1124 [code] 78 chars (max 76): - **Errors are JSON on stderr with exit 1** for se
09-code.md:1126 [code] 79 chars (max 76): - **The transcript lookup takes the newest `.jsonl
09-code.md:1127 [code] 78 chars (max 76): with a fork or a worktree copy running concurrentl
09-code.md:1129 [code] 80 chars (max 76): - **The spinner regex is tuned to this fleet's sta
09-code.md:1135 [code] 104 chars (max 76): - Does not touch a session already inside herdr (u
09-code.md:1148 [code] 81 chars (max 76): - `/herdr-room` — pull live agents into one room a
09-code.md:1149 [code] 88 chars (max 76): - `/herdr-info` — where every body of an oracle (o
09-code.md:1156 [code] tag ```markdown: use bash, zsh or none
09-code.md:1159 [code] 643 chars (max 76): description: Sign a PR, issue, or comment with a "
09-code.md:1173 [code] 77 chars (max 76): # 2. print the block (pass your OWN exact model id
09-code.md:1176 [code] 78 chars (max 76): # 2b. PR in a repo that is NOT this pane's cwd — a
09-code.md:1179 [code] 98 chars (max 76): ~/.claude/skills/herdr-pr/herdr-sign.sh claude-opu
09-code.md:1186 [code] 86 chars (max 76): ~/.claude/skills/herdr-pr/herdr-sign.sh claude-opu
09-code.md:1189 [code] 101 chars (max 76): ~/.claude/skills/herdr-pr/herdr-sign.sh claude-opu
09-code.md:1197 [token] pane `w24:p5` is in no capture/BRIEF
09-code.md:1197 [code] 78 chars (max 76): Second arg signs another pane: `herdr-sign.sh gpt-
09-code.md:1202 [code] 78 chars (max 76): claude, omp (Oh My Pi) and codex all store transcr
09-code.md:1208 [code] 94 chars (max 76): | omp | `~/.omp/agent/sessions/<key>/<ts>_<uuid>.j
09-code.md:1209 [code] 91 chars (max 76): | codex | `~/.codex/sessions/YYYY/MM/DD/rollout-<t
09-code.md:1211 [code] 78 chars (max 76): herdr reports no session id for omp, so the newest
09-code.md:1220 [token] pane `w2F:p1` is in no capture/BRIEF
09-code.md:1224 [code] 80 chars (max 76): Unnamed → the script signs a pane id and warns on 
09-code.md:1229 [code] 146 chars (max 76): 1. **Session, not shell** — paths come from the pa
09-code.md:1231 [code] 277 chars (max 76): 3. **Parse herdr's JSON with `\x1f`, not tab** — b
09-code.md:1233 [code] 78 chars (max 76): 4. **`--work` is the PR's repo, not `$PWD`** — sam
09-code.md:1234 [code] 78 chars (max 76): the other side: pass the path explicitly, never le
09-code.md:1235 [code] 80 chars (max 76): 5. **One checkout cannot be on two branches** — `-
09-code.md:1236 [code] 77 chars (max 76): still reads whichever branch is checked out, so si
09-code.md:1237 [code] 77 chars (max 76): PR A silently cites A's branch and head. Use `--re
09-code.md:1240 [code] 78 chars (max 76): cites a commit that only exists on the un-merged b
09-code.md:1243 [code] 77 chars (max 76): fed the `incubated:` pair, which is suppressed whe
09-code.md:1244 [code] 78 chars (max 76): session's checkout, so same-repo `--ref` validated
09-code.md:1245 [code] 78 chars (max 76): the tree's branch anyway. Traps 5 and 6 are both s
09-code.md:1248 [code] 79 chars (max 76): 8. **`$HERDR_PANE_ID` goes stale after a pane move
09-code.md:1249 [code] 82 chars (max 76): it started with. After `/herdr-room` in/out or `pa
09-code.md:1250 [token] pane `wF:p1` is in no capture/BRIEF (+1 more: 09-code.md:1254)
09-code.md:1250 [code] 81 chars (max 76): id, and the script fails with `no herdr agent for 
09-code.md:1252 [code] 85 chars (max 76): `herdr agent list | jq -r '.result.agents[] | sele
09-code.md:1254 [token] pane `w15:p4` is in no capture/BRIEF
09-code.md:1254 [token] pane `wH:p1` is in no capture/BRIEF
09-code.md:1254 [token] pane `w15:p6` is in no capture/BRIEF
09-code.md:1254 [token] pane `wE:p1` is in no capture/BRIEF
09-code.md:1254 [token] pane `w16:p1` is in no capture/BRIEF
09-code.md:1254 [code] 81 chars (max 76): gods-eyes wF:p1 → w15:p4, water-api wH:p1 → w15:p6
09-code.md:1255 [code] 78 chars (max 76): **Fixed in the script the same morning:** when the
09-code.md:1257 [code] 83 chars (max 76): processes include an ancestor of itself, signs tha
09-code.md:1259 [code] 81 chars (max 76): 9. **A worktree session plus `--work <main checkou
09-code.md:1260 [code] 83 chars (max 76): `incubated:`.** The script decides "another repo" 
09-code.md:1261 [code] 82 chars (max 76): not git common dirs, so a linked worktree of the s
09-code.md:1262 [code] 79 chars (max 76): The `incubated:` stanza then carries the PR's ref,
09-code.md:1263 [code] 81 chars (max 76): session's own branch. The commit is right; the lab
09-code.md:1264 [code] 82 chars (max 76): session's own repo, pass `--work <your own worktre
09-code.md:1266 [code] 81 chars (max 76): 2026-10-07 for a same-checkout `--ref`). gods-eyes
09-code.md:1267 [code] 81 chars (max 76): night with the mislabel. **Fixed in the script the
09-code.md:1268 [code] 83 chars (max 76): `git rev-parse --git-common-dir`. Another worktree
09-code.md:1269 [code] 83 chars (max 76): PR's branch and head (or `--ref`) in `worktree:` a
09-code.md:1270 [code] 81 chars (max 76): PR checkout. `incubated:` appears only for a genui
09-code.md:1271 [code] 81 chars (max 76): same repo other worktree, with and without `--ref`
09-code.md:1274 [code] 80 chars (max 76): After editing the script, `ls` both printed paths.
09-code.md:1279 [code] 77 chars (max 76): An oracle working an **incubated** repo has its pa
09-code.md:1280 [code] 78 chars (max 76): diff in `$(ghq root)/...`. The session facts and t
09-code.md:1284 [code] 80 chars (max 76): `--work <path>` adds a second stanza for the repo 
09-code.md:1305 [token] conv `31d3ceb5` is in no capture/BRIEF (+3 more: 09-code.md:1354, 09-code.md:1366, 09-code.md:1367)
09-code.md:1313 [token] commit `97548ce` is in no capture/BRIEF
09-code.md:1323 [token] conv `8f3ac9b3` is in no capture/BRIEF
09-code.md:1333 [token] pane `w2N:p1` is in no capture/BRIEF
09-code.md:1335 [token] pane `w2N:t1` is in no capture/BRIEF
09-code.md:1344 [code] 79 chars (max 76): `--compact` folds every value back beside its key 
09-code.md:1364 [code] 80 chars (max 76): **Values are folded block scalars (`>-`) on their 
09-code.md:1365 [code] 78 chars (max 76): one, `#` starts no comment and `:` separates no ke
09-code.md:1371 [code] 79 chars (max 76): Compact — the default — is the one place those quo
09-code.md:1374 [code] 78 chars (max 76): `it's a 'quoted' value`, on a `#31` subject, and o
09-code.md:1377 [code] 81 chars (max 76): Four groups, in the order a reviewer asks: **who**
09-code.md:1378 [code] 78 chars (max 76): **which session** holds the reasoning, and **how t
09-code.md:1379 [code] 81 chars (max 76): `incubated`, naming **which repo** the diff is in,
09-code.md:1382 [code] 80 chars (max 76): `work` is the ghq clone, `link` the vault symlink 
09-code.md:1386 [code] 77 chars (max 76): Both print in both blocks. `link` was public-omitt
09-code.md:1387 [code] 81 chars (max 76): grounds that its path carries the private oracle r
09-code.md:1388 [code] 80 chars (max 76): also prints the oracle `cwd` and its worktree pare
09-code.md:1389 [code] 78 chars (max 76): so withholding one path while printing two others 
09-code.md:1392 [code] 78 chars (max 76): Merging the two into one `branch`/`head` pair is t
09-code.md:1393 [code] 78 chars (max 76): branch name gives the reader nothing to attach it 
09-code.md:1398 [code] 81 chars (max 76): The script reads `gh repo view <slug> --json isPri
09-code.md:1404 [code] 92 chars (max 76): | public | everything except the agent's own stora
09-code.md:1408 [code] 79 chars (max 76): checkout, vault symlink — identify which tree prod
09-code.md:1410 [code] 78 chars (max 76): content — the transcript of everything this sessio
09-code.md:1415 [code] 80 chars (max 76): before anyone notices. `--full` forces the complet
09-code.md:1417 [code] 77 chars (max 76): Even redacted, the block still answers the questio
09-code.md:1422 [code] 79 chars (max 76): Commits (use `Co-Authored-By`), third-party repos 
09-code.md:1431 [code] zsh builtin (print / &!) in a ```bash block: tag it ```zsh
09-code.md:1431 [code] command differs from its capture: no capture starts like '#!/usr/bin/env bash # Emit the "Built by" signatur'
09-code.md:1434 [code] 79 chars (max 76): # Describes a herdr SESSION (the pane), not whatev
09-code.md:1440 [code] 80 chars (max 76): # Output is compact by default — one line per fiel
09-code.md:1444 [code] 78 chars (max 76): # --ref reports a commit the working tree is not s
09-code.md:1445 [code] 81 chars (max 76): # SHA the rebase rewrote, or a second PR in the sa
09-code.md:1446 [code] 78 chars (max 76): # can only describe whatever branch happens to be 
09-code.md:1447 [code] 81 chars (max 76): # while working PR A meant checking B out first — 
09-code.md:1450 [code] 80 chars (max 76): # --work names the repo the PR actually lives in. 
09-code.md:1451 [code] 79 chars (max 76): # repo has its pane cwd in the oracle vault and th
09-code.md:1452 [code] 80 chars (max 76): # session facts and code facts come from two diffe
09-code.md:1453 [code] 79 chars (max 76): # the block reports the ORACLE's branch and HEAD o
09-code.md:1457 [code] 81 chars (max 76): # redacted block — no absolute paths, no transcrip
09-code.md:1458 [code] 82 chars (max 76): # private oracle slug — because those map a machin
09-code.md:1468 [code] 91 chars (max 76): --compact) compact=1; shift ;;   # default; kept s
09-code.md:1469 [code] 86 chars (max 76): --tall)    compact=0; shift ;;   # one value per l
09-code.md:1497 [code] 80 chars (max 76): # HERDR_PANE_ID is fixed when the shell starts. Af
09-code.md:1498 [code] 77 chars (max 76): # the agent lives at a new pane id while the env s
09-code.md:1499 [code] 79 chars (max 76): # three agents failed here in one round (2026-10-0
09-code.md:1501 [code] 78 chars (max 76): # include an ancestor of this script. That is the 
09-code.md:1502 [code] 80 chars (max 76): # Exactly one match, or keep failing: guessing a p
09-code.md:1516 [code] 111 chars (max 76): pi = json.loads(run("herdr", "pane", "process-info
09-code.md:1527 [code] 158 chars (max 76): echo "herdr-sign: HERDR_PANE_ID '${pane:-<unset>}'
09-code.md:1533 [code] 81 chars (max 76): # \x1f, not tab: bash collapses runs of whitespace
09-code.md:1535 [code] 79 chars (max 76): IFS=$'\x1f' read -r name pane_id tab wsid agent ti
09-code.md:1537 [code] 82 chars (max 76): # No pane means no session to point at. Emitting a
09-code.md:1538 [code] 85 chars (max 76): # exact failure this block exists to prevent: auth
09-code.md:1541 [code] 84 chars (max 76): echo "  Run this from inside a herdr pane (HERDR_P
09-code.md:1546 [code] 81 chars (max 76): # The block describes the session, so every path i
09-code.md:1550 [code] 82 chars (max 76): # A named agent is addressable by name; an unnamed
09-code.md:1554 [code] 113 chars (max 76): python3 -c 'import json,sys; print(json.load(sys.s
09-code.md:1556 [code] 81 chars (max 76): repo_root=$(git -C "$root" rev-parse --show-toplev
09-code.md:1560 [code] 103 chars (max 76): *)  main=$(cd "$repo_root/$(dirname "${common:-.gi
09-code.md:1562 [code] 82 chars (max 76): [ "$main" = "$repo_root" ] && where="main checkout
09-code.md:1564 [code] 85 chars (max 76): # Two passes: BSD sed has no lazy quantifier, so s
09-code.md:1565 [code] 106 chars (max 76): slug=$(git -C "$root" remote get-url origin 2>/dev
09-code.md:1568 [code] 81 chars (max 76): # The work repo: where the diff is. Defaults to th
09-code.md:1571 [code] 99 chars (max 76): [ -n "$work" ] && work_root=$(git -C "$work" rev-p
09-code.md:1572 [code] 116 chars (max 76): work_slug=$(git -C "$work_root" remote get-url ori
09-code.md:1578 [code] 83 chars (max 76): if ! work_head=$(git -C "$work_root" log --oneline
09-code.md:1585 [code] 78 chars (max 76): # Same repo, other checkout: a session in a linked
09-code.md:1586 [code] 79 chars (max 76): # --work is the main checkout (or another worktree
09-code.md:1588 [code] 78 chars (max 76): # `incubated:` (17 floodboy PRs, 2026-10-07). Comp
09-code.md:1590 [code] 115 chars (max 76): common_dir() { (cd "$1" 2>/dev/null && cd "$(git r
09-code.md:1597 [code] 78 chars (max 76): # The session tree's own branch and head. --ref na
09-code.md:1599 [code] 79 chars (max 76): # incubated stanza to carry it — so it has to land
09-code.md:1600 [code] 78 chars (max 76): # no-op in exactly the same-repo case traps 5 and 
09-code.md:1601 [code] 77 chars (max 76): # The same holds for another worktree of the same 
09-code.md:1602 [code] 78 chars (max 76): # checkout the PR is in, so its branch and head (o
09-code.md:1605 [code] 81 chars (max 76): if { [ -n "$ref" ] && [ "$work_root" = "$root" ]; 
09-code.md:1614 [code] 82 chars (max 76): # /incubate drops this breadcrumb into every repo 
09-code.md:1618 [code] 77 chars (max 76): when=$(sed -n 's/^date: //p' "$work_root/.claude/I
09-code.md:1622 [code] 79 chars (max 76): # Where the work repo actually is. Naming the repo
09-code.md:1623 [code] 77 chars (max 76): # reader which code to look at but not how to reac
09-code.md:1624 [code] 77 chars (max 76): # repo the ghq clone and the vault symlink are two
09-code.md:1630 [code] 113 chars (max 76): *)  work_main=$(cd "$work_root/$(dirname "${work_c
09-code.md:1639 [code] 79 chars (max 76): # Redact by default, open up only on proof of priv
09-code.md:1640 [code] 82 chars (max 76): # publishes a machine layout to the internet, and 
09-code.md:1644 [code] 87 chars (max 76): case "$(gh repo view "$work_slug" --json isPrivate
09-code.md:1653 [code] 82 chars (max 76): # Each agent stores transcripts under its own sche
09-code.md:1654 [code] 80 chars (max 76): # in ways that look like typos but aren't. Claude 
09-code.md:1655 [code] 82 chars (max 76): # omp replaces only "/" and wraps the whole thing 
09-code.md:1657 [code] 85 chars (max 76): claude_key() { local p=${1//\//-}; echo "${p//./-}
09-code.md:1658 [code] 88 chars (max 76): omp_key()    { local p=${1#/}; echo "--${p//\//-}-
09-code.md:1663 [code] 115 chars (max 76): transcript="${CODEX_COMPANION_TRANSCRIPT_PATH:-$HO
09-code.md:1666 [code] 83 chars (max 76): # herdr reports no session id for omp, so take the
09-code.md:1674 [code] 83 chars (max 76): # Date-partitioned rollouts; herdr gives the uuid,
09-code.md:1675 [code] 104 chars (max 76): transcript=$(find "$HOME/.codex/sessions" -name "r
09-code.md:1682 [code] 77 chars (max 76): # Valid YAML, so the block is machine-readable wit
09-code.md:1683 [code] 80 chars (max 76): # text. Every value is a folded block scalar (`>-`
09-code.md:1685 [code] 79 chars (max 76): # "feat: share… #31" survives verbatim. Quoted one
09-code.md:1689 [code] 78 chars (max 76): # blocks — the public block already carries cwd an
09-code.md:1696 [code] 79 chars (max 76): # One composed block, not two heredocs. Two drifte
09-code.md:1698 [code] 80 chars (max 76): # Groups answer the four questions a reviewer actu
09-code.md:1711 [code] 84 chars (max 76): ${HERDR_SOCKET_PATH:-~/.config/herdr/herdr.sock (d
09-code.md:1714 [code] 78 chars (max 76): # The incubated group only exists when the PR's re
09-code.md:1774 [code] 117 chars (max 76): $([ "$redact" = "1" ] && printf '%s' "Agent-privat
09-code.md:1777 [code] 77 chars (max 76): **Reach this session** — from any pane, agent, or 
09-code.md:1788 [code] 80 chars (max 76): # Compact (the default) folds "key: >-" + its inde
09-code.md:1789 [code] 81 chars (max 76): # The value must be re-quoted on the way: inline Y
09-code.md:1790 [code] 81 chars (max 76): # ": " as a key separator, which is exactly what t
09-code.md:1814 [code] 114 chars (max 76): echo "herdr-sign: ${work_slug:-this repo} is ${vis
09-code.md:1815 [code] 133 chars (max 76): [ "$visibility" = "unknown" ] && echo "  gh could 
09-code.md:1817 [code] 103 chars (max 76): [ -f "${transcript/#\~/$HOME}" ] || echo "warning:
09-code.md:1820 [code] 102 chars (max 76): echo "warning: --work ${work} has no origin remote
09-code.md:1823 [code] 113 chars (max 76): echo "warning: this agent has no name, so the bloc
09-code.md:1824 [code] 80 chars (max 76): echo "  herdr agent rename ${pane_id:-\$HERDR_PANE
09-code.md:1832 [code] tag ```markdown: use bash, zsh or none
09-code.md:1835 [code] 1291 chars (max 76): description: The reverse of /herdr-wt, and the one
09-code.md:1836 [code] 99 chars (max 76): argument-hint: "[<wt|pane> ...] | --all-but-me | -
09-code.md:1841 [code] 86 chars (max 76): `/herdr-wt` makes a branch, a locked worktree, a s
09-code.md:1842 [code] 90 chars (max 76): the right order, at any scale. **The agent that di
09-code.md:1843 [code] 87 chars (max 76): Only then is anything removed. Nothing is lost: wo
09-code.md:1844 [code] 86 chars (max 76): the parent, the transcript stays in `~/.claude/pro
09-code.md:1847 [code] 87 chars (max 76): Merged 2026-10-29 from `/herdr-dissolve` (save, th
09-code.md:1848 [token] conv `20261029` is in no capture/BRIEF (+1 more: 09-code.md:1849)
09-code.md:1848 [code] 94 chars (max 76): (sweep and sync). Nat: "merge … to one". The old t
09-code.md:1849 [code] 77 chars (max 76): here and `../herdr-clean-up-sync/SKILL.md.bak-2026
09-code.md:1855 [code] 82 chars (max 76): | `/herdr-dissolve <wt\|pane> [...]` | the named w
09-code.md:1856 [code] 155 chars (max 76): | `/herdr-dissolve --all-but-me` | every pane and 
09-code.md:1857 [code] 123 chars (max 76): | `/herdr-dissolve --sweep [--host H]` | every rep
09-code.md:1858 [code] 89 chars (max 76): | `/herdr-dissolve --sync [--all]` | checkouts tha
09-code.md:1859 [code] 94 chars (max 76): | `/herdr-dissolve self` | the worktree you are ru
09-code.md:1861 [code] 86 chars (max 76): `--sweep` runs sync's plan too, as the old `/herdr
09-code.md:1866 [code] 82 chars (max 76): Everything runs on `fleet` (`tools/fleet-tui/workt
09-code.md:1867 [code] 88 chars (max 76): installed as `fleet` by `just fleet-install`). Eve
09-code.md:1870 [code] 119 chars (max 76): fleet audit  [--host H] [--repo X] [--pick wt1,wt2
09-code.md:1871 [code] 114 chars (max 76): fleet clean  [--host H] [--repo X] [--pick wt1,wt2
09-code.md:1877 [code] 86 chars (max 76): No `--host` = this machine. `--host white.local` r
09-code.md:1880 [code] 88 chars (max 76): **`fleet <cmd> --help` is not help.** Unknown flag
09-code.md:1881 [code] 89 chars (max 76): ran a full-machine `clean` plan (2026-10-08, stopp
09-code.md:1882 [code] 84 chars (max 76): changes nothing, but never type a flag to "see the
09-code.md:1887 [code] 88 chars (max 76): Scope it to the mode. **With no `--repo` and no `-
09-code.md:1888 [code] 80 chars (max 76): repo on the machine** (1278 on m5, 2026-10-08). On
09-code.md:1893 [code] 91 chars (max 76): slug=$(git -C "$repo" remote get-url origin | sed 
09-code.md:1894 [code] 115 chars (max 76): fleet audit --repo "$slug" --idle-agents --idle-sh
09-code.md:1896 [code] 106 chars (max 76): fleet audit [--host H] --idle-agents --idle-shells
09-code.md:1900 [code] 88 chars (max 76): For `--all-but-me`, also list the panes on the mai
09-code.md:1915 [code] 95 chars (max 76): | B | merged (in the default branch, or a merged P
09-code.md:1917 [code] 77 chars (max 76): | D | uncommitted work or local-only commits | the
09-code.md:1918 [code] 82 chars (max 76): | K | an agent is **working/blocked** in it, or no
09-code.md:1926 [code] 89 chars (max 76): **✓ is not done.** ✓ means the agent finished its 
09-code.md:1927 [code] 90 chars (max 76): on a question ("A or B?"), a plan waiting for appr
09-code.md:1928 [code] 87 chars (max 76): me to merge?" is **waiting on the human**: list it
09-code.md:1938 [code] 101 chars (max 76): | D with an idle agent | **save first** (step 4a):
09-code.md:1941 [code] 127 chars (max 76): | idle agent on the MAIN checkout (`--all-but-me`)
09-code.md:1952 [code] 79 chars (max 76): - **Safe now**: A, plus B/C and empty worktrees wi
09-code.md:1953 [code] 92 chars (max 76): - **Done agents**: B/C with an idle ✓ agent whose 
09-code.md:1958 [code] 89 chars (max 76): - **Behind (sync)**: `would ff` rows, and SKIP rea
09-code.md:1960 [code] 83 chars (max 76): Then AskUserQuestion (multiSelect), one option per
09-code.md:1961 [code] 91 chars (max 76): COUNT and the repos in each description (`removes 
09-code.md:1962 [code] 87 chars (max 76): hides that `--sweep` is machine-wide. For a long "
09-code.md:1969 [code] 84 chars (max 76): **Who is the parent:** the agent in the repo's mai
09-code.md:1972 [code] 86 chars (max 76): repo=$(git -C "$wt" rev-parse --path-format=absolu
09-code.md:1977 [code] 87 chars (max 76): Usually that is you. If no agent runs there, the p
09-code.md:1978 [code] 90 chars (max 76): vault, `$repo/ψ/inbox/handoff/<date>_dissolve_<wt>
09-code.md:1980 [code] 83 chars (max 76): Brief each agent with `fleet send <pane> "<brief>"
09-code.md:1983 [code] 87 chars (max 76): - Commit everything that is work, on this worktree
09-code.md:1984 [code] 95 chars (max 76): `.env*`, shell snapshots or credentials. Hooks off
09-code.md:1985 [code] 100 chars (max 76): - Push the branch and open a PR signed with `/herd
09-code.md:1986 [code] 88 chars (max 76): - Tell the parent with `fleet send <parent-pane> "
09-code.md:1987 [code] 78 chars (max 76): done, what is verified, what is left open, anythin
09-code.md:1990 [code] 89 chars (max 76): Brief them all, then `fleet watch` them all. When 
09-code.md:1991 [code] 87 chars (max 76): confirm the `DISSOLVE-READY` line. If one fails, d
09-code.md:1996 [code] 87 chars (max 76): Removing a worktree ends its function, not its rec
09-code.md:2000 [code] 90 chars (max 76): python3 ~/.claude/skills/herdr-dissolve/tombstone.
09-code.md:2001 [code] 101 chars (max 76): python3 ~/.claude/skills/herdr-dissolve/tombstone.
09-code.md:2004 [code] 89 chars (max 76): It records what the worktree was (branch, born, ow
09-code.md:2005 [code] 91 chars (max 76): (PR url or `main@sha`) and where the record lives 
09-code.md:2006 [code] 77 chars (max 76): paths). It writes `<main checkout>/ψ/memory/tombst
09-code.md:2007 [code] 92 chars (max 76): `~/.herdr/tombstones/<repo>/` when the repo has no
09-code.md:2011 [code] 106 chars (max 76): - uncommitted or untracked files: not in any commi
09-code.md:2013 [code] 82 chars (max 76): - LOCKED: `/herdr-wt` and `wtui` lock every worktr
09-code.md:2016 [code] 87 chars (max 76): `/herdr-tree` shows the phase: `cease` rows are re
09-code.md:2019 [code] 86 chars (max 76): **Why:** a removed thing with no death date and no
09-code.md:2020 [code] 85 chars (max 76): chain (2026-08-22: 33 of 39 archived skills had ne
09-code.md:2023 [code] 94 chars (max 76): fleet clean [--host H] --repo X --pick <wt1,wt2,..
09-code.md:2024 [code] 105 chars (max 76): fleet clean [--host H] --idle-shells --go         
09-code.md:2027 [code] 86 chars (max 76): `--pick` switches off the age rule for those rows 
09-code.md:2028 [code] 90 chars (max 76): acting: a working agent, new edits or new local co
09-code.md:2029 [code] 90 chars (max 76): an idle agent with ctrl-c (transcript kept), and r
09-code.md:2030 [code] 91 chars (max 76): through `herdr worktree remove`, so the sidebar ag
09-code.md:2033 [code] 90 chars (max 76): Run it from a pane **outside** the worktree. The *
09-code.md:2042 [code] 88 chars (max 76): Commits to `rescue/<wt>`, pushes, opens a signed d
09-code.md:2043 [code] 90 chars (max 76): `.codex/`, `.env*`, shell snapshots and credential
09-code.md:2044 [code] 89 chars (max 76): in the staged diff stops it before pushing; repo h
09-code.md:2050 [code] 80 chars (max 76): herdr agent prompt <pane> '/exit'          # an id
09-code.md:2054 [code] 88 chars (max 76): Never the pane running this skill. Never `rm` or r
09-code.md:2063 [code] 89 chars (max 76): It only fast-forwards. `SKIP diverged ↑N` means so
09-code.md:2069 [code] 82 chars (max 76): fleet snapshot --commit        # the fleet history
09-code.md:2072 [code] 85 chars (max 76): Report: before and after counts of worktrees and p
09-code.md:2073 [code] 83 chars (max 76): acknowledgement), spaces closed, agents quit (pane
09-code.md:2074 [code] 89 chars (max 76): revived), fast-forwards (`↓N → sha`), tombstones w
09-code.md:2079 [code] 84 chars (max 76): Do 4a yourself: commit, push, signed PR, report to
09-code.md:2083 [code] 95 chars (max 76): fleet send <parent-pane> "DISSOLVE-READY <pr-url> 
09-code.md:2088 [code] 97 chars (max 76): 1. **Never dissolve a working agent, and never one
09-code.md:2090 [code] 91 chars (max 76): (`worktrees.ts:49,71`): a modified `.envrc` reads 
09-code.md:2091 [code] 86 chars (max 76): Any other uncommitted file makes it `SKIP uncommit
09-code.md:2092 [code] 87 chars (max 76): (`IGNORED_CAP`) is deleted too, so copy anything y
09-code.md:2094 [code] 79 chars (max 76): 3. **Public repo:** before any PR or `--pr`, list 
09-code.md:2095 [code] 87 chars (max 76): (`git -C <wt> status --porcelain -uall | head -40`
09-code.md:2096 [code] 88 chars (max 76): Codex session logs into public PRs; closed PRs kee
09-code.md:2098 [code] 90 chars (max 76): 4. **A space can hold an agent in a second tab or 
09-code.md:2099 [code] 85 chars (max 76): into another space as its own tab; closing that sp
09-code.md:2100 [code] 89 chars (max 76): closing a space, list ALL its panes in ALL tabs (`
09-code.md:2101 [code] 90 chars (max 76): `herdr pane process-info --pane P`): close it only
09-code.md:2103 [code] 85 chars (max 76): 5. **Removing a worktree with `git` alone leaves a
09-code.md:2104 [code] 85 chars (max 76): `fleet clean` goes through `herdr worktree remove`
09-code.md:2105 [code] 88 chars (max 76): 6. **Other owners.** On m5, `arra-oracle-v4` and `
09-code.md:2106 [code] 77 chars (max 76): `--sweep` uses `--skip arra-oracle-v4,odoo-yd` unl
09-code.md:2107 [code] 84 chars (max 76): 7. **Idle shells on main checkouts** are not workt
09-code.md:2110 [code] 90 chars (max 76): 8. **"local-only commits" may be MAIN's, not the w
09-code.md:2111 [code] 91 chars (max 76): `main` that is ahead of `origin` reports main's un
09-code.md:2112 [code] 90 chars (max 76): empty worktree reads as D. Check `git -C <repo> lo
09-code.md:2113 [code] 87 chars (max 76): if those are the same commits, push main (the huma
09-code.md:2114 [code] 83 chars (max 76): `git -C <wt> log main..HEAD` instead. Measured 202
09-code.md:2116 [code] 79 chars (max 76): 9. **Survey files go to `mktemp`, not `.tmp/`.** N
09-code.md:2118 [code] 89 chars (max 76): 10. **Nothing merges here.** PRs wait for a human.
09-code.md:2124 [code] 91 chars (max 76): - `/herdr-issue`, `/herdr-ticket`: issue first, th
09-code.md:2134 [code] tag ```python: use bash, zsh or none
09-code.md:2136 [code] 85 chars (max 76): """tombstone: write the record of a worktree BEFOR
09-code.md:2138 [code] 84 chars (max 76): A worktree ceases as an active thing; what it was,
09-code.md:2139 [code] 82 chars (max 76): where its record lives must survive it. Dry run un
09-code.md:2148 [code] 102 chars (max 76): return subprocess.run(cmd, cwd=cwd, capture_output
09-code.md:2163 [code] 88 chars (max 76): for line in run(["git", "-C", path, "worktree", "l
09-code.md:2169 [code] 80 chars (max 76): me = next((w for w in wts if os.path.realpath(w["w
09-code.md:2171 [code] 99 chars (max 76): print("refusing: not a linked worktree (a main che
09-code.md:2174 [code] 80 chars (max 76): branch = (me.get("branch") or "").replace("refs/he
09-code.md:2181 [code] 89 chars (max 76): for w in json.loads(run(["herdr", "workspace", "li
09-code.md:2183 [code] 103 chars (max 76): if cp and os.path.realpath(cp) == path:   # realpa
09-code.md:2185 [code] 87 chars (max 76): for p in json.loads(run(["herdr", "pane", "list"])
09-code.md:2186 [code] 79 chars (max 76): if p.get("workspace_id") == wid and p.get("agent_s
09-code.md:2188 [code] 96 chars (max 76): tr = glob.glob(os.path.expanduser(f"~/.claude/proj
09-code.md:2189 [code] 105 chars (max 76): sessions.append((p.get("agent"), sid, tr[0] if tr 
09-code.md:2194 [code] 146 chars (max 76): rl = run(["git", "-C", path, "reflog", "show", "--
09-code.md:2195 [code] 99 chars (max 76): born_sha, born = (rl[-1].split("|")[0], rl[-1].spl
09-code.md:2197 [code] 102 chars (max 76): commits = run(["git", "-C", path, "log", "--format
09-code.md:2199 [code] 96 chars (max 76): in_main = subprocess.run(["git", "-C", path, "merg
09-code.md:2205 [code] 101 chars (max 76): for p in json.loads(run(["gh", "pr", "list", "--st
09-code.md:2206 [code] 108 chars (max 76): "number,headRefName,headRefOid,mergedAt,url,mergeC
09-code.md:2207 [code] 77 chars (max 76): if p["headRefName"] == branch and p["headRefOid"] 
09-code.md:2211 [code] 100 chars (max 76): dirty = [l for l in run(["git", "-C", path, "statu
09-code.md:2213 [code] 101 chars (max 76): if dirty: blockers.append(f"{len(dirty)} uncommitt
09-code.md:2214 [code] 106 chars (max 76): if not (pr or in_main): blockers.append("HEAD is n
09-code.md:2215 [code] 125 chars (max 76): if me.get("locked"): blockers.append(f"worktree is
09-code.md:2218 [code] 102 chars (max 76): "---", "kind: worktree-tombstone", f"repo: {repo}"
09-code.md:2219 [code] 89 chars (max 76): f"head: {head}", f"born: {born}", f"ceased: {now.i
09-code.md:2220 [code] 97 chars (max 76): f"reason: {reason or ('merged PR #%d' % pr['number
09-code.md:2224 [code] 81 chars (max 76): "A worktree ceased here. The function ended; this 
09-code.md:2225 [code] 81 chars (max 76): "## What it was", f"- repo `{repo}`, branch `{bran
09-code.md:2229 [code] 134 chars (max 76): f"- {reason or ('PR #%d merged %s' % (pr['number']
09-code.md:2230 [code] 91 chars (max 76): f"- HEAD contained in main: {'yes' if in_main else
09-code.md:2231 [code] 97 chars (max 76): f"- {pr['url'] if pr else 'main@' + main_sha[:7]}"
09-code.md:2234 [code] 114 chars (max 76): body += [f"- {a} session `{sid}`: `{tr}`" for a, s
09-code.md:2236 [code] 114 chars (max 76): body += ["", "## Not committed at the time (would 
09-code.md:2241 [code] 122 chars (max 76): dest_dir = vault if os.path.isdir(os.path.join(mai
09-code.md:2245 [code] 91 chars (max 76): dest = os.path.join(dest_dir, f"{now.strftime('%Y-
09-code.md:2253 [code] 92 chars (max 76): print("written." + ("  Blockers above still apply 
