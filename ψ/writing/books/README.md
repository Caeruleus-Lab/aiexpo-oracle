# บทเรียน AIExpo Oracle / Lessons

Step-by-step guides for the AI Expo workshop "ARRA Oracle & Multi-Agent Workflow" (Fri 6 Nov 2026), in workshop order.
Open [`index.html`](index.html) for the landing page. Agents: [`llms.txt`](llms.txt).

| # | ไทย | English | Webpages |
|---|---|---|---|
| 01 | [ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop](2026-10-30_claude-chatgpt-install-guide/README.md) | [Install Claude and ChatGPT, ready for the workshop](2026-10-30_claude-chatgpt-install-guide/README.en.md) | [index.html](2026-10-30_claude-chatgpt-install-guide/index.html) · [th](2026-10-30_claude-chatgpt-install-guide/th.html) · [en](2026-10-30_claude-chatgpt-install-guide/en.html) |
| 02 | [ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง](2026-10-30_ego-lite-guide/README.md) | [Install ego(lite) so your AI agent gets a browser of its own](2026-10-30_ego-lite-guide/README.en.md) | [index.html](2026-10-30_ego-lite-guide/index.html) · [th](2026-10-30_ego-lite-guide/th.html) · [en](2026-10-30_ego-lite-guide/en.html) |
| 03 | [ต่อ claude.ai และ ChatGPT เข้ากับ MCP ของบทเรียน](2026-10-30_mcp-connect-guide/README.md) | [Connect claude.ai and ChatGPT to the lessons MCP](2026-10-30_mcp-connect-guide/README.en.md) | [index.html](2026-10-30_mcp-connect-guide/index.html) · [th](2026-10-30_mcp-connect-guide/th.html) · [en](2026-10-30_mcp-connect-guide/en.html) |

Each lesson's editions are signed together with AIExpo Oracle's key; see the lesson's `SIGNATURE.md`.
## Ask the lessons from your AI (MCP)

Read-only MCP, no sign-in: `https://aiexpo.buildwithoracle.com/mcp` (tools: search, fetch, get_image, list_lessons).

- **claude.ai**: Customize → Connectors → Add → Add custom connector, paste the URL, choose No sign-in
- **ChatGPT**: Settings → Plugins → Browse directory → Add → Add custom MCP server, Authentication: No authentication
- **Claude Code**: `claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp` (this repo already ships `.mcp.json`)
- **Codex**: `codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp`

Step by step with screenshots: [lesson 03](2026-10-30_mcp-connect-guide/README.en.md).

Rebuild this list: `python3 build_index.py`; then `uv run --with pillow python build_chunks.py` for the MCP index.

— AIExpo Oracle (Oracle AI)
