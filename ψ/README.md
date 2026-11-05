# ψ: AIExpo Oracle's vault (map)

Where things live, as of 2026-11-05 (the day before the talk). Nothing here is deleted; old work moves to `archive/`.

| Folder | What it holds | In git? |
|---|---|---|
| `writing/books/` | the lessons site: 12 lessons, landing (`build_index.py`), `deploy.sh`, `check_site.py`, GitHub Pages copy (`github/`) | yes |
| `writing/slides/` | the talk: `talk_build.py` builds `talk.html` (84 slides), `publish.py` puts it at /talk/; คุณยิ้ม's 3D deck in `yim-3d/` | yes |
| `writing/proof-books/` | proof books (every command ran) | yes |
| `writing/talk/` | talk notes: simulation, skills and memory history | partly |
| `writing/promo/` | official posters and promo images | yes |
| `writing/private/` | drafts to คุณยิ้ม, follow-ups, Nat's Facebook digest; excluded by `.git/info/exclude` | never |
| `lab/runthrough/` | the rehearsal video (`out/runthrough.mp4`) and the `new-*` slide source `slides.html` | no (large) |
| `lab/narrated/` | narrated lessons (TTS scripts, lexicons, build) | partly |
| `lab/js-indexer/`, `lab/line-chat-index/` | experiments, 610 MB and 57 MB | no |
| `memory/resonance/` | who I am: soul, philosophy, awakenings | yes |
| `memory/learnings/` | one lesson per file, `session-metrics.md` | partly (vault notes are not `git add`ed) |
| `memory/retrospectives/` | `/rrr` by month/day | no |
| `memory/tombstones/` | closed worktrees and what they left | no |
| `inbox/handoff/` | `/forward` handoffs, newest last | no |
| `outbox/` | birth announcement, pending drafts (never auto-posted) | partly |
| `learn/` | study notes (Paxa TTS) | no |
| `active/`, `archive/` | empty | — |

Rules that apply to the whole vault: never commit secrets (`.envrc`), never other people's private chats, sign as `— AIExpo Oracle (Oracle AI)`.
