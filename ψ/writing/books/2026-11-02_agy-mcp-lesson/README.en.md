# Use the Antigravity CLI (agy) with the lessons MCP

> This lesson installs Google's Antigravity CLI (the `agy` command), signs in for the first time, then connects it to the AIExpo lessons MCP, both the server on Cloudflare and the one that runs on your machine. Every `agy` command ran for real on 2 Nov 2026 with agy 1.4.12; raw outputs are in [captures/](captures/). Written by AI, for people and AI. The three editions are signed with one Ethereum key.

- Install and first sign-in happen once per machine and need a person at the keyboard. Steps 2-5 were written down from the real install on this machine the same morning.
- Two traps were hit for real at sign-in: a cut URL that made Google answer `invalid_scope`, and a data-sharing box that comes pre-ticked.
- Companion lesson: [Build your own MCP](../2026-11-02_build-mcp-lesson/en) explains how the MCP connected here works.
- Other edition: [ไทย (the original)](README.md)
- Compiled by AIExpo Oracle (AI), not a person.

---

## 1. What the Antigravity CLI is

The Antigravity CLI is Google's coding agent for the terminal; the command is `agy`. It uses the Gemini model of the signed-in account (on this machine: Google AI Pro, model "Gemini 4 Argon (Medium)").

- **The Antigravity desktop app (2.3.1) does not ship the `agy` command.** The CLI is a separate install.
- `agy` connects to MCP servers of both kinds: `http` (a URL) and `stdio` (a command run on your machine).

```
$ agy --version
1.4.12
(exit 0)
```

![Summary card: two MCP servers added to agy, agy mcp list shows both enabled, agy -p answers through aiexpo-github with 7 lessons, and the three traps at sign-in and add](images/01-agy-mcp.png)

## 2. Install

The official command:

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

- The path needs `/cli/`: `https://antigravity.google/install.sh`, which some docs show, answers 404.
- **Read the script before running it** (`curl -fsSL ... | less`). What it does:
  - no sudo
  - downloads the binary from an updater on Google Cloud Run and checks its SHA-512
  - puts it at `~/.local/bin/agy` and removes the macOS quarantine flag
  - `agy install` appends `export PATH="$HOME/.local/bin:$PATH"` to both `~/.zshrc` and `~/.profile`
- During the install you will see lines like `ERROR: logging before google.Init: I1102 ...`. They are INFO logs (the leading `I`), not real errors; the script ends with exit 0.
- At the end: `✅ Antigravity CLI installed successfully at ~/.local/bin/agy`. Open a new terminal or `source ~/.zshrc`, then try `agy --version`.

## 3. First sign-in

Run `agy` (or your first `agy -p`) and it prints a Google sign-in URL.

1. Open it with **"→ Click here to authenticate"** (do not copy it by hand; see step 4).
2. Sign in to Google; antigravity.google shows a code starting with `4/0...`.
3. Paste the code into agy's prompt and press Enter (`agy -p` waits only 60 seconds for it; if that is too short, sign in with plain `agy` first).
4. The next screen asks about data sharing; see step 5.
5. "Do you trust the contents of this project?": answer **Yes, I trust this folder** only for a folder you really trust.

Then the banner shows the version, the account's plan and the model.

## 4. Trap: a cut URL makes Google answer invalid_scope

The sign-in URL is very long. agy shows it in a box with a pager (`(1–16 of 29 lines)`, scroll with shift+↑/↓). Copying only the visible part with the mouse cuts the URL mid-word.

What happened for real: the URL was cut inside the word `experimentsandconfigs`, and Google answered

```
Access blocked: Authorization Error
Error 400: invalid_scope (invalid=.../auth/experiments)
```

- **Fix**: press "→ Click here to authenticate", or scroll the box to the end; a complete URL ends with `&state=...`.
- General lesson: an error saying the scope is wrong is often not a permission problem but an incomplete URL.

## 5. Trap: the pre-ticked data-sharing box

After the code, this box appears **already ticked**:

```
[x] Yes, I agree to help improve Antigravity CLI by allowing Google to collect and use my Interactions data
```

- Pressing Done straight away means Google may collect and use your conversations.
- Nat chose to untick it: press Enter on the box to toggle it, then Done.
- What this workshop suggests: read every box before Done, especially the ones ticked for you, and decide yourself whether to share.

## 6. The agy mcp commands

```
$ agy mcp --help
Usage: agy mcp <subcommand> [flags] [args]

Available subcommands:
  add      Add or update an MCP server configuration
  remove   Remove an MCP server configuration
  list     List all configured MCP servers
  enable   Enable an MCP server
  disable  Disable an MCP server

Run "agy mcp <subcommand> --help" for flags, argument rules, and examples.
(exit 0)
```

The flags of `add`:

```
$ agy mcp add --help
Usage: agy mcp add [flags] <name> <commandOrUrl> [args...]

Add or update an MCP server configuration

Flags:
  -H        Short alias for --header (default [])
  -e        Short alias for --env (default [])
  --env     Environment variable KEY=value (repeatable) (default [])
  -h        Show help
  --header  HTTP header Key: Value (repeatable) (default [])
  --help    Show help
  -t        Short alias for --type (default stdio)
  --type    Server type: 'stdio' or 'http' (default stdio)

Arguments:
  <name>          Unique name for the server.
  <commandOrUrl>  Executable for a stdio server, or the URL for an http server.
  [args...]       Arguments passed to the stdio command.

Notes:
  Flags must come before <name>; a flag placed after it is rejected.
  http/https URLs are detected automatically, so --type is usually unnecessary.
  Use -- before the command to pass a command or args that begin with '-'.

Examples:
  agy mcp add fs npx -y @modelcontextprotocol/server-filesystem /work
  agy mcp add --header "Authorization: Bearer TOKEN" api https://example.com/mcp
  agy mcp add --env GITHUB_TOKEN=xxx gh -- docker run -i ghcr.io/github/mcp
(exit 0)
```

The two most important lines in Notes:

- **Flags must come before `<name>`**; a flag after the name is rejected, with an error that never mentions flags (section 8).
- URLs starting with http/https are detected as `http` automatically; no `--type` needed.

## 7. Add the lessons MCP

Two servers, the same tools (`search`, `fetch`, `get_image`, `list_lessons`):

- `aiexpo`: the server on Cloudflare; searches by meaning and by words
- `aiexpo-github`: fetched from GitHub by `npx` and run on your machine; searches by words, works even if Cloudflare is down

```
$ agy mcp add aiexpo https://aiexpo.buildwithoracle.com/mcp; agy mcp add aiexpo-github npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
Added MCP server "aiexpo" (http)
Added MCP server "aiexpo-github" (stdio)
(exit 0)
```

`add` is "add or update": running it again changes nothing and creates no duplicate.

```
$ agy mcp list
NAME           TYPE   STATUS   COMMAND/URL
aiexpo         http   enabled  https://aiexpo.buildwithoracle.com/mcp
aiexpo-github  stdio  enabled  npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
(exit 0)
```

Other MCP servers already on your machine show up in this list too (left out of the capture).

## 8. Trap: a flag after the name

```
$ agy mcp add try-x https://example.com/mcp --header 'X-Test: 1'   # flag after the name
Error: http server type does not accept command arguments
(exit 1)
```

The error does not say the flag is misplaced. Everything after `<commandOrUrl>` counts as arguments for the command, and an http server has no command to pass them to, so agy answers `http server type does not accept command arguments`. When you see this error, check the flag order first.

The right order: `agy mcp add --header "X-Test: 1" try-x https://example.com/mcp` (the capture script removes `try-x` if it was added).

## 9. Disable for a while, then enable again

No need to remove a server; disable it:

```
$ agy mcp disable aiexpo-github; agy mcp list; agy mcp enable aiexpo-github
Disabled MCP server "aiexpo-github"
NAME           TYPE   STATUS    COMMAND/URL
aiexpo         http   enabled   https://aiexpo.buildwithoracle.com/mcp
aiexpo-github  stdio  disabled  npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
Enabled MCP server "aiexpo-github"
aiexpo-github  stdio  enabled  npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
(exit 0)
```

## 10. Test with agy -p

`-p` asks once and exits, good for scripts and tests. The flags used:

- `--sandbox`: the agent works inside a sandbox
- `--dangerously-skip-permissions`: no prompt before each tool call. In `-p` nobody is there to press Allow, so it is needed; use it only together with `--sandbox` and with read-only MCP servers like these.
- `--print-timeout 240s`: wait at most 4 minutes for the answer

Ask through the Cloudflare server:

```
$ agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p "Use ONLY the MCP server aiexpo ... how do I build my own MCP server?"
- **Implement the JSON-RPC 2.0 handlers**: Create a script (starting from the 59-line dependency-free `mini-mcp.mjs`) that handles `initialize`, `tools/list` (declaring your tool names and JSON Schemas in `TOOLS`), and `tools/call` (running your tool logic and returning `{ content: [{ type: "text", text }] }`), while ignoring notifications without an `id`.
- **Add your data and choose a transport**: Swap `NOTES` for your own data (or pre-chunked/embedded data like `chunks.json`), and expose the handler either via **stdio** (reading one JSON line per `stdin` and writing responses strictly to `stdout`) or **Streamable HTTP** (accepting `POST` requests at `/mcp`, e.g., on a Cloudflare Worker).
- **Test and register with your client**: Verify responses using `stdio` pipes or `curl`, then connect the server to your AI client (e.g., `claude mcp add mini -- node /path/to/mini-mcp.mjs` for local stdio, or adding the `/mcp` URL as a custom connector in claude.ai and ChatGPT).

**Lesson URL:** https://aiexpo.buildwithoracle.com/2026-11-02_build-mcp-lesson/en

**MCP tools called:**
- `aiexpo` → `search`
- `aiexpo` → `fetch`
(exit 0)
```

Ask through the GitHub server:

```
$ agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p "Use ONLY the MCP server aiexpo-github ... list_lessons, then search"
- **Lesson count**: 7
- **Title of lesson 7**:
  - **English**: Build your own MCP: turn lessons into tools for AI
  - **Thai**: สร้าง MCP ของตัวเอง: จากบทเรียนเป็นเครื่องมือให้ AI
- **Top hit ID**: `build-mcp/en/3`
- **MCP tool names called** (on server `aiexpo-github`): `list_lessons`, `search`
(exit 0)
```

Both answer from the real lessons and name the tools they called. If agy answers without calling any tool, check that `agy mcp list` shows `STATUS` `enabled`.

## 11. All the traps in one place

| Symptom | Cause | Fix |
|---|---|---|
| `install.sh` answers 404 | URL without `/cli/` | `https://antigravity.google/cli/install.sh` |
| `ERROR: logging before google.Init` during install | INFO-level log | Nothing to do; check the exit code |
| No `agy` command although the Antigravity app is installed | The desktop app does not include the CLI | Install the CLI separately |
| `Error 400: invalid_scope` | Sign-in URL copied incompletely | Press "Click here to authenticate", or scroll until you see `&state=` |
| Sharing data without noticing | The box comes pre-ticked | Press Enter to untick it before Done |
| `agy -p` sign-in times out | It waits only 60 seconds for the code | Sign in with plain `agy` first |
| `http server type does not accept command arguments` | Flag placed after the name, read as arguments | Put every flag before `<name>` |

## 12. All the files

- [captures/](captures/): 9 raw outputs and `capture.sh`, which reruns them all (agy must be installed and signed in)
- MCP on Cloudflare: `https://aiexpo.buildwithoracle.com/mcp`
- stdio MCP: `npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp`
