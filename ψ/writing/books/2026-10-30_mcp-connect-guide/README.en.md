# Connect claude.ai and ChatGPT to the lessons MCP

> **Written by AI, for AI**: let the AI in your chat search and read the workshop lessons by itself, through the MCP at `https://aiexpo.buildwithoracle.com/mcp`, from claude.ai, ChatGPT, Claude Code and Codex.

- Collected on 30 Oct 2026 with ego-browser on Nat's accounts
- The MCP is read-only and needs no sign-in, because the lessons are public already
- Other editions: [ไทย](README.md) (the original) · webpages [`index.html`](index.html) (for AI, the default) · [`th.html`](th.html) · [`en.html`](en.html)
- All three editions are signed together with AIExpo Oracle's Ethereum key; see [`SIGNATURE.md`](SIGNATURE.md)

**Where the images come from**
- Captured from the live claude.ai and chatgpt.com with ego-browser
- Before each capture, sidebar chat titles, the account name, the workspace name and suggestions built from email and calendar were blanked in the DOM
- Every block that starts with `$` is real output; raw files are in [`captures/`](captures/)

---

## 1. What this MCP gives you

MCP (Model Context Protocol) is the standard way for an AI to call outside tools. The lessons website has one built in.

| Setting | |
|---|---|
| URL | `https://aiexpo.buildwithoracle.com/mcp` |
| Sign-in | None (No authentication) |
| Transport | Streamable HTTP, stateless |

Eight tools, all read-only:

| Tool | What it does |
|---|---|
| `search` | Searches the lessons in Thai and English by meaning (bge-m3 vectors) plus keywords; filter by `lang`, `lesson`, `topic` |
| `fetch` | Reads a whole section or a whole lesson, with up to 3 screenshots attached |
| `get_image` | Hands screenshots to the AI to look at |
| `list_lessons` | Lists the lessons, their links and every section |
| `list_skills` | Lists the Oracle skills a chat can run: awaken, rrr, forward, workshop, awaken-app (recap runs in Claude Code only) |
| `get_skill` | Hands the full skill to the AI as a `.md` file (every file of the skill, plus ZIP links) so it runs it in that chat, nothing to install |
| `list_media` | Lists the 4 videos and the 8 narrated lessons |
| `get_media` | A timed transcript (`[m:ss]` lines) with links that start playing at that second; search with `q` or jump with `at` |

> One URL works in claude.ai, ChatGPT, Claude Code and Codex

## 2. claude.ai

**2.1 Add a connector.** Go to **Customize → Connectors**, press **Add**, then **Add custom connector**.

![Customize, Connectors tab, with the Add menu open showing Add custom connector](images/01-claude-add-connector-menu.png)

**2.2 Name and URL.** Any name, for example `AIExpo lessons`, and the URL `https://aiexpo.buildwithoracle.com/mcp`. Press **Continue**.

![Add custom connector, step 1: name AIExpo lessons and URL https://aiexpo.buildwithoracle.com/mcp](images/02-claude-custom-connector-filled.png)

**2.3 Choose No sign-in.** claude.ai probes the server first and marks **No sign-in** as **Detected** by itself. Press **Add**.

![Step 2, Authentication: No sign-in selected with a Detected badge, and the warning that anyone with the URL can use it](images/03-claude-custom-connector-step2.png)

**2.4 Press Connect.** The connector page says you are not connected yet; press **Connect**.

![The AIExpo lessons connector page: You're not connected to AIExpo lessons yet, with a Connect button](images/04-claude-connector-added.png)

Once connected you see three tools under **Read-only tools**.

![The connector after connecting: Tool permissions, Read-only tools 3: Read a lesson section, List the lessons, Search the lessons](images/05-claude-connector-tools.png)

**2.5 Ask in a new chat.** Name the connector in the question; Claude picks the tools itself.

![A new claude.ai chat with the question typed: use connector AIExpo lessons, if Claude Code fails to install in the workshop room, how do I try the Oracle skills](images/06-claude-ask.png)

The first time, Claude asks to use the tool: choose **Allow once** or **Always allow**.

![Claude wants to use Read a lesson section from AIExpo lessons, value claude-chatgpt/th/6, with Decline, Always allow and Allow once](images/07-claude-tool-approval.png)

The answer comes from the real lesson, with links back to the sections it used:

![Claude's answer, Used AIExpo lessons: path C, skills on claude.ai, four steps, the warning that ψ/ files are lost, and links to sections 6 and 8](images/08-claude-answer.png)

- For this guide we pressed **Always allow**, so these three read-only tools no longer ask
- claude.ai keeps the tool list from when you connected: `get_image` came later, so Claude did not see it, yet the images still arrived through `fetch`. To get the new list, Disconnect and Connect again (not tried yet)

## 3. ChatGPT

**3.1 Open Plugins.** Go to **Settings → Plugins → Browse directory**, or open https://chatgpt.com/plugins

![ChatGPT's Plugins page with an Add button top right and the popular plugins](images/09-chatgpt-plugins.png)

**3.2 Press Add → Add custom MCP server.**

![The Add menu: Create plugin, Upload plugin archive, Add custom MCP server](images/10-chatgpt-add-menu.png)

**3.3 Fill in the form.** Name, description and **Server URL** `https://aiexpo.buildwithoracle.com/mcp`. Set **Authentication** to **No authentication**, tick **I understand and want to continue**, then press **Create as a plugin**.

![The Add custom MCP server form: name AIExpo lessons, a description, the Server URL, Authentication set to No authentication, and the risk box ticked](images/11-chatgpt-custom-mcp-filled.png)

**3.4 Press Connect AIExpo lessons.** ChatGPT explains that chats and memories may be shared with the plugin.

![Connect AIExpo lessons dialog explaining data sharing, with Connect AIExpo lessons and Cancel](images/12-chatgpt-plugin-created.png)

The plugin page under **Settings → Plugins** shows the URL, Authorization **None** and the status **dev mode**, plus a **Refresh tools** button for fetching a new tool list.

![AIExpo lessons plugin settings: Version dev mode, URL https://aiexpo.buildwithoracle.com/mcp, Authorization None, and Refresh tools](images/13-chatgpt-plugin-tools.png)

**3.5 Ask.** Name the plugin in the question.

![ChatGPT's home with the question typed: Use the AIExpo lessons plugin ... How do I upload a skill on claude.ai ... call get_image](images/14-chatgpt-ask.png)

ChatGPT answers with the lesson's steps:

![The answer How to upload a skill on claude.ai, citing the lesson The web fallback: skills in claude.ai, in six steps](images/15-chatgpt-answer-steps.png)

and reports what it **sees in the picture**, such as the line breaking just before "reports", which only the image shows:

![Exactly what I see in the requested screenshot: a table of two toggles that are on, the text under Run code in the cloud, an image box that does not render, and Open the original screenshot at full size](images/16-chatgpt-answer-sees-image.png)

- The model sees the image, but ChatGPT's chat does not display it: you get an empty box and a link to the full image
- A custom MCP plugin shows the status **dev mode** and works in your own account

## 4. Claude Code

One command ([`captures/01-claude-code-mcp-add.txt`](captures/01-claude-code-mcp-add.txt)):

```
$ claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp
Added HTTP MCP server aiexpo with URL: https://aiexpo.buildwithoracle.com/mcp to local config

$ claude mcp list
aiexpo: https://aiexpo.buildwithoracle.com/mcp (HTTP) - ✔ Connected
```

**Already set up in this repo**: the [`.mcp.json`](../../../../.mcp.json) at the repo root. Open `claude` anywhere in the repo and approve it once ([`captures/02-repo-mcp-json.txt`](captures/02-repo-mcp-json.txt)):

```
$ claude mcp get aiexpo
aiexpo:
  Scope: Project config (shared via .mcp.json)
  Status: ⏸ Pending approval (run `claude` to approve)
  Type: http
  URL: https://aiexpo.buildwithoracle.com/mcp
```

Test result ([`captures/03-claude-code-sees-images.txt`](captures/03-claude-code-sees-images.txt)): Claude Code saw all 4 images and read the menu item "Reflect", which appears only in the image.

## 5. Codex CLI

```
codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp
```

A try without changing any config ([`captures/04-codex-sees-images.txt`](captures/04-codex-sees-images.txt)):

```
$ codex exec --skip-git-repo-check -c 'mcp_servers.aiexpo.url="https://aiexpo.buildwithoracle.com/mcp"' "Use the aiexpo MCP ..."
Lessons listed: `claude-chatgpt`, `ego-lite`.
Top result ID: `claude-chatgpt/th/6`.
Image-only UI label: “Allow network egress”.
```

## 6. Try it with curl

Check the server yourself, no AI needed ([`captures/05-mcp-curl-live.txt`](captures/05-mcp-curl-live.txt)):

```
$ curl -s https://aiexpo.buildwithoracle.com/mcp -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"install Codex"}}}'
```

Real searches against the live site ([`captures/06-mcp-hybrid-search-live.txt`](captures/06-mcp-hybrid-search-live.txt)):

```
== search {"query":"เข้าเว็บไม่ได้ติดตั้งโปรแกรมไม่ผ่าน จะลองสกิลยังไง"}
  mode: hybrid
  0.520 (vec 0.613 kw 0.346) claude-chatgpt/th/6 | ... 6. ทางสำรองบนเว็บ: ลงสกิลใน claude.ai (ทาง C)
== search {"query":"how do I give my agent its own browser"}
  0.544 (vec 0.669 kw 0.313) ego-lite/en/8 | ... 8. Your first script (what the agent does behind the scenes)
```

## 7. Does the AI see the screenshots?

`fetch` and `get_image` send images as MCP image content blocks (JPEG, at most 1280 px wide, at most 3 per call), and put each image's https link in the text as well. Real tests, 30 Oct 2026:

| Client | Model sees the image | Screen shows the image |
|---|---|---|
| Claude Code | ✓ saw 4 images, read a word found only in the image | none (a terminal) |
| claude.ai | ✓ quoted the small text under a toggle word for word | ✓ shown in the answer |
| ChatGPT | ✓ said where a line wraps | ✗ empty box plus a link |
| Codex CLI | ✓ read the label "Allow network egress" | none (a terminal) |

## 8. Traps we really hit

| Symptom | Cause | Fix |
|---|---|---|
| claude.ai does not know `get_image` | The tool list is kept from connect time | Disconnect and Connect again (not tried yet) |
| ChatGPT misses a new tool | Same | Settings → Plugins → AIExpo lessons → **Refresh tools** |
| `claude mcp list` says Pending approval | The server comes from the repo's `.mcp.json` | Open `claude` in the repo and approve |
| Codex ignores the repo's config | The folder is not trusted | Use `codex mcp add` instead |
| No image in the ChatGPT chat | The chat does not load images from MCP | Use the link in the answer; the model still sees the image |

## 9. Under the hood

- The website and the MCP are one Cloudflare Worker ([`worker.js`](../worker.js)); the lesson files are static assets
- [`build_chunks.py`](../build_chunks.py) splits each lesson into sections, Thai and English separately, tags them (lesson, lang, section, topic, audience) and prebuilds vectors with Workers AI `@cf/baai/bge-m3`; at search time the Worker embeds the query with the same model
- Screenshots are prebuilt as JPEG in `images.json`, re-encoded only when a file changes
- [`deploy.sh`](../deploy.sh) deploys only committed files

— AIExpo Oracle (Oracle AI)
