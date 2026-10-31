# บทเรียน AIExpo Oracle / Lessons

Step-by-step guides for the AI Expo workshop "ARRA Oracle & Multi-Agent Workflow" (Fri 6 Nov 2026), in workshop order.
Open [`index.html`](index.html) for the landing page. Agents: [`llms.txt`](llms.txt).

| # | ไทย | English | Webpages |
|---|---|---|---|
| 01 | [ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop](2026-10-30_claude-chatgpt-install-guide/README.md) | [Install Claude and ChatGPT, ready for the workshop](2026-10-30_claude-chatgpt-install-guide/README.en.md) | [index.html](2026-10-30_claude-chatgpt-install-guide/index.html) · [th](2026-10-30_claude-chatgpt-install-guide/th.html) · [en](2026-10-30_claude-chatgpt-install-guide/en.html) |
| 02 | [ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง](2026-10-30_ego-lite-guide/README.md) | [Install ego(lite) so your AI agent gets a browser of its own](2026-10-30_ego-lite-guide/README.en.md) | [index.html](2026-10-30_ego-lite-guide/index.html) · [th](2026-10-30_ego-lite-guide/th.html) · [en](2026-10-30_ego-lite-guide/en.html) |
| 03 | [ต่อ claude.ai และ ChatGPT เข้ากับ MCP ของบทเรียน](2026-10-30_mcp-connect-guide/README.md) | [Connect claude.ai and ChatGPT to the lessons MCP](2026-10-30_mcp-connect-guide/README.en.md) | [index.html](2026-10-30_mcp-connect-guide/index.html) · [th](2026-10-30_mcp-connect-guide/th.html) · [en](2026-10-30_mcp-connect-guide/en.html) |
| 04 | [ทำหนังสั้นให้ Oracle พูดเอง](2026-10-31_phukhao-film-guide/README.md) | [Make an Oracle tell its own story on film](2026-10-31_phukhao-film-guide/README.en.md) | [index.html](2026-10-31_phukhao-film-guide/index.html) · [th](2026-10-31_phukhao-film-guide/th.html) · [en](2026-10-31_phukhao-film-guide/en.html) |
| 05 | [เรื่องของภูเขา และการเดินทางของครอบครัว Oracle](2026-10-31_phukhao-oracle-journey/README.md) | [Phukhao's story, and the Oracle family's journey](2026-10-31_phukhao-oracle-journey/README.en.md) | [index.html](2026-10-31_phukhao-oracle-journey/index.html) · [th](2026-10-31_phukhao-oracle-journey/th.html) · [en](2026-10-31_phukhao-oracle-journey/en.html) |
| 06 | [ห้องเดียว หลาย agent: herdr-room in / out](2026-10-31_herdr-room-lesson/README.md) | [One room, many agents: herdr-room in / out](2026-10-31_herdr-room-lesson/README.en.md) | [index.html](2026-10-31_herdr-room-lesson/index.html) · [th](2026-10-31_herdr-room-lesson/th.html) · [en](2026-10-31_herdr-room-lesson/en.html) |

Each lesson's editions are signed together with AIExpo Oracle's key; see the lesson's `SIGNATURE.md`.
## Ask the lessons from your AI (MCP)

Read-only MCP, no sign-in: `https://aiexpo.buildwithoracle.com/mcp` (tools: search, fetch, get_image, list_lessons).

- **claude.ai**: Customize → Connectors → Add → Add custom connector, paste the URL, choose No sign-in
- **ChatGPT**: Settings → Plugins → Browse directory → Add → Add custom MCP server, Authentication: No authentication
- **Claude Code**: `claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp` (this repo already ships `.mcp.json`)
- **Codex**: `codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp`

Step by step with screenshots: [lesson 03](2026-10-30_mcp-connect-guide/README.en.md).

## GitHub copy

The same site is mirrored on GitHub Pages: https://caeruleus-lab.github.io/aiexpo-lessons/ (repo
[Caeruleus-Lab/aiexpo-lessons](https://github.com/Caeruleus-Lab/aiexpo-lessons)). Pages serves files only, so the hosted `/mcp`
stays on Cloudflare; the repo also ships the same four tools as a local stdio MCP server, keyword search only, no dependencies (Node 18+):

- **Claude Code**: `claude mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons`
- **Codex**: `codex mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons`
- Offline from a clone: set `AIEXPO_DIR=/path/to/clone` and run `node mcp/server.mjs`

The hosted endpoint's source is in `mcp/worker.js`. Rebuild the copy: `sh github/build_pages.sh <clone of aiexpo-lessons>`.

Rebuild this list: `python3 build_index.py`; then `uv run --with pillow python build_chunks.py` for the MCP index.

— AIExpo Oracle (Oracle AI)
