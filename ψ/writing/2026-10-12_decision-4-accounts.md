# Decision 4: which account do attendees need? (research, 2026-10-12)

Checked by AIExpo Oracle (AI). The vendor pages were read live; third-party pages are marked as such.

| Tool | Free plan works? | Skills install path (arra-oracle-skills-cli) | Source |
|---|---|---|---|
| Claude Code | **No.** Pro or higher only ($17/mo annual, $20/mo monthly) | `/plugin install` or `--agent claude-code` | claude.com/pricing (read live) |
| Codex CLI (ChatGPT login) | **Yes.** "Codex is included across ChatGPT plans, including Free and Go." The CLI signs in with ChatGPT. Low limits; Codex Cloud is not included | `--agent codex --with-commands` | help.openai.com/en/articles/11369540 (read live) |
| Antigravity (`agy`) | **Yes.** $0 Individual plan with a weekly agent quota (third-party sources) | `--agent antigravity` writes to `~/.gemini/antigravity/skills`, which matches Google's codelab | third-party pricing blogs + Google codelab + `src/cli/agents.ts` |
| Gemini CLI | **Unclear, probably no.** Third-party reports say the personal free tier ended June 2026. Works with an API key | `--agent gemini-cli --with-commands` | third-party only, not confirmed |

Not tested yet: an actual `/awaken --fast` run on Codex Free or Antigravity Free. Needs a rehearsal on a clean account before the event.
