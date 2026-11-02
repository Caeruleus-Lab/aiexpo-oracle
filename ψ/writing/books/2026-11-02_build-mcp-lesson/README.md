# สร้าง MCP ของตัวเอง: จากบทเรียนเป็นเครื่องมือให้ AI

> บทเรียนนี้เล่าว่า MCP ของบทเรียน AIExpo ทำงานยังไง ตั้งแต่ไฟล์ README จนถึง AI ที่เรียกเครื่องมือได้ ทุกคำสั่งรันจริงวันที่ 2 พ.ย. 2026 ผลดิบอยู่ใน [captures/](captures/) โค้ดเต็มอยู่ใน [code/](code/) เขียนโดย AI สำหรับคนและ AI ลงลายเซ็นทั้งสามฉบับด้วยกุญแจ Ethereum ดอกเดียว

- MCP ที่ใช้จริงมีสองตัว เครื่องมือชุดเดียวกัน: ตัวบน Cloudflare (`https://aiexpo.buildwithoracle.com/mcp`) กับตัวที่รันในเครื่องเรา (`npx -y github:Caeruleus-Lab/aiexpo-lessons`)
- ทั้งสองตัวไม่มี dependency เลย เขียนด้วย JavaScript ล้วน อ่านจบได้ในบ่ายเดียว
- บทเรียนเริ่มจาก MCP ที่เล็กที่สุด 59 บรรทัด แล้วค่อยขยายไปเป็นของจริง
- ฉบับอื่น: [English](README.en.md)
- เรียบเรียงโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. MCP คืออะไร

MCP (Model Context Protocol) คือภาษากลางระหว่าง AI กับเครื่องมือ ฝั่งที่ AI อยู่เรียกว่า client (claude.ai, ChatGPT, Claude Code, Codex) ฝั่งที่มีเครื่องมือเรียกว่า server

- ข้อความทุกอันเป็น JSON-RPC 2.0: `{"jsonrpc":"2.0","id":1,"method":"...","params":{...}}`
- server ที่มีแค่เครื่องมือ ตอบแค่สามคำสั่งก็พอ
  - `initialize`: client ทักทาย server ตอบชื่อ เวอร์ชัน และบอกว่ามี tools
  - `tools/list`: บอกว่ามีเครื่องมืออะไร แต่ละตัวรับ input หน้าตาแบบไหน (JSON Schema)
  - `tools/call`: เรียกเครื่องมือจริง ได้ `content` กลับมาเป็น text หรือ image
- ข้อความที่ไม่มี `id` คือ notification เช่น `notifications/initialized` server ไม่ต้องตอบ
- ส่งข้อความได้สองทาง (transport)
  - **stdio**: client เปิด server เป็นโปรเซสลูก ส่ง JSON บรรทัดละอันทาง stdin รับคำตอบทาง stdout
  - **Streamable HTTP**: client POST JSON ไปที่ URL เดียว เช่น `/mcp` ได้ JSON กลับมา

## 2. ภาพรวม: ชิ้นส่วนทั้งหมด

![แผนภาพ: README ถูกตัดเป็น chunks.json แล้วเสิร์ฟด้วย server สองตัว worker.js บน Cloudflare กับ server.mjs ในเครื่อง ให้ client ทุกตัวเรียก search fetch get_image list_lessons](images/01-architecture.png)

ขนาดจริงของแต่ละชิ้น:

```
$ wc -l worker.js mcp/server.mjs build_chunks.py; jq '.chunks|length' chunks.json
     343 worker.js
     232 github/mcp/server.mjs
     153 build_chunks.py
     728 total
chunks: 128
model: @cf/baai/bge-m3
(exit 0)
```

## 3. MCP ที่เล็กที่สุด: mini-mcp.mjs

ไฟล์เดียว 59 บรรทัด Node 18 ขึ้นไป ไม่ต้อง `npm install` มีเครื่องมือเดียวคือ `search` ค้นโน้ตสี่อันที่เขียนไว้ในไฟล์

```js
#!/usr/bin/env node
// mini-mcp.mjs: the smallest useful MCP server. stdio, JSON-RPC 2.0, no dependencies, Node 18+.
// One tool, `search`, over a few notes kept in this file. Swap NOTES for your own data.
//
//   node mini-mcp.mjs                        (an MCP client starts it; it reads stdin, writes stdout)
//   claude mcp add mini -- node /path/to/mini-mcp.mjs
import { createInterface } from "node:readline";

const NOTES = [
  { id: "awaken", text: "/awaken gives a new Oracle its name, its principles and its ψ memory folder." },
  { id: "rrr", text: "/rrr writes a retrospective at the end of a session, so the next session remembers." },
  { id: "recap", text: "/recap reads the latest retros and handoffs and tells you where you left off." },
  { id: "mcp", text: "MCP lets an AI call tools: the client sends JSON-RPC, the server answers with results." },
];

const TOOLS = [{
  name: "search",
  description: "Search the notes by keyword. Returns the matching notes with their id.",
  inputSchema: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
}];

function search(query) {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  const hits = NOTES.map((n) => ({ ...n, score: words.filter((w) => n.text.toLowerCase().includes(w)).length }))
    .filter((n) => n.score > 0).sort((a, b) => b.score - a.score);
  const text = hits.length ? hits.map((n) => `${n.id}: ${n.text}`).join("\n") : "no match";
  return { content: [{ type: "text", text }] };
}

function handle({ id, method, params = {} }) {
  if (id === undefined) return null; // a notification (notifications/initialized): no answer
  switch (method) {
    case "initialize":
      return { protocolVersion: params.protocolVersion || "2025-06-18", capabilities: { tools: {} }, serverInfo: { name: "mini-mcp", version: "1.0.0" } };
    case "ping":
      return {};
    case "tools/list":
      return { tools: TOOLS };
    case "tools/call":
      if (params.name !== "search") throw { code: -32602, message: `unknown tool: ${params.name}` };
      return search(String(params.arguments?.query || ""));
    default:
      throw { code: -32601, message: `Method not found: ${method}` };
  }
}

// One JSON message per line in, one per line out. Never print anything else to stdout: it is the wire.
createInterface({ input: process.stdin }).on("line", (line) => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }); }
  try {
    const result = handle(msg);
    if (result !== null) send({ jsonrpc: "2.0", id: msg.id, result });
  } catch (e) {
    send({ jsonrpc: "2.0", id: msg.id ?? null, error: { code: e.code || -32603, message: e.message || String(e) } });
  }
});
const send = (m) => process.stdout.write(JSON.stringify(m) + "\n");
```

สามอย่างที่ต้องจำ:

- **stdout คือสายส่งข้อมูล** ห้าม `console.log` อะไรอย่างอื่นลง stdout ข้อความ debug ให้ไป stderr
- **notification ไม่ต้องตอบ** `handle()` คืน `null` เมื่อไม่มี `id`
- **error ตอบเป็น JSON-RPC error** ใช้รหัสมาตรฐาน `-32601` (ไม่มี method นี้) `-32602` (params ผิด) `-32700` (JSON พัง)

ลองคุยกับมันด้วยมือ ส่ง JSON เข้า stdin ทีละบรรทัด:

```
$ printf initialize + tools/list | node code/mini-mcp.mjs
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"mini-mcp","version":"1.0.0"}}}
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"search","description":"Search the notes by keyword. Returns the matching notes with their id.","inputSchema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}]}}
(exit 0)
```

เรียกเครื่องมือ พร้อมลองเรียกผิดสองแบบ:

```
$ printf tools/call search {query: "session memory"} | node code/mini-mcp.mjs
{"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"awaken: /awaken gives a new Oracle its name, its principles and its ψ memory folder.\nrrr: /rrr writes a retrospective at the end of a session, so the next session remembers."}]}}
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"unknown tool: nope"}}
{"jsonrpc":"2.0","id":3,"error":{"code":-32601,"message":"Method not found: bogus"}}
(exit 0)
```

## 4. ต่อ mini-mcp เข้า Claude Code

เขียน config บอก client ว่าจะเปิด server ยังไง แล้วให้ Claude ใช้เครื่องมือ:

```json
{"mcpServers":{"mini":{"command":"node","args":["mini-mcp.mjs"]}}}
```

```
$ claude -p --mcp-config mini.json --allowedTools mcp__mini__search "..."
`/rrr` writes the retrospective. The search returned the note's title, `rrr`, but no separate note id, so `rrr` is the closest identifier I have.
(exit 0)
```

ถ้าจะใช้ประจำ ลงทะเบียนครั้งเดียว: `claude mcp add mini -- node /path/to/mini-mcp.mjs` ชื่อเครื่องมือใน Claude Code จะเป็น `mcp__<ชื่อ server>__<ชื่อ tool>` เช่น `mcp__mini__search`

## 5. ข้อมูล: ตัดบทเรียนเป็นชิ้น (build_chunks.py)

mini-mcp ค้นโน้ตสี่อัน ของจริงค้นบทเรียนทั้งหมด ไทยและอังกฤษ งานแรกคือเตรียมข้อมูลไว้ล่วงหน้า ไม่ใช่ทำตอนมีคนถาม

`build_chunks.py` อ่าน README ของทุกบทเรียน แล้ว:

1. ตัดที่หัวข้อ `## ` ทีละหัวข้อ แต่ข้ามบรรทัดที่อยู่ในบล็อกโค้ด (นับ ```` ``` ```` เปิดปิด) ไม่งั้นคอมเมนต์ `## ` ในโค้ดจะกลายเป็นหัวข้อปลอม
2. ติดป้าย topic (install, skill, browser, ...) ด้วยคำที่เจอในหัวข้อและเนื้อหา
3. ทำ vector ของแต่ละชิ้นด้วย Workers AI `@cf/baai/bge-m3` (หลายภาษา ไทยได้ 1024 มิติ) ทำใหม่เฉพาะชิ้นที่ข้อความเปลี่ยน
4. เก็บภาพหน้าจอเป็น base64 ลง `images.json` (ย่อไม่เกิน 1280 px, JPEG 80) ให้ server ส่งภาพให้ AI ดูได้

หน้าตาของหนึ่งชิ้น:

```
$ jq '.chunks[] | select(.id=="herdr-room/th/5") | {id, lesson, lang, title, url, text: .text[0:120], vec: (.vec|length)}' chunks.json
{
  "id": "herdr-room/th/5",
  "lesson": "herdr-room",
  "lang": "th",
  "title": "5. room out: ทุกคนกลับ space ของตัวเอง",
  "url": "https://aiexpo.buildwithoracle.com/2026-10-31_herdr-room-lesson/th#s6",
  "text": "## 5. room out: ทุกคนกลับ space ของตัวเอง\n\n```bash\nherdr-room out team --session roomlab\n```\n\n```\n  run   herdr --sessio",
  "vec": 1024
}
(exit 0)
```

`url` ชี้ไปที่ `#s6` ของหน้าเว็บ ลิงก์จากผลค้นจึงพาคนไปถึงหัวข้อนั้นตรง ๆ id ของหัวข้อในหน้าเว็บจึงห้ามเลื่อน ถ้าเพิ่ม section ข้างหน้า ต้องให้ id เดิมคงที่

## 6. MCP บน Cloudflare Worker (worker.js)

Worker ตัวเดียวทำสองงาน: เสิร์ฟหน้าเว็บบทเรียน กับตอบ MCP ที่ `/mcp` ([code/worker.js](code/worker.js) 343 บรรทัด)

```js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/mcp" || url.pathname === "/mcp/") return mcp(request, env);
    if (url.pathname.endsWith(".mp4")) return video(request, env);
    return env.ASSETS.fetch(request);
  },
};
```

`mcp()` รับ POST อ่าน JSON (ทีละอันหรือเป็น array ก็ได้) ส่งแต่ละข้อความให้ `handle()` ซึ่งหน้าตาเหมือน mini-mcp แทบทุกบรรทัด ต่างกันแค่:

- **stateless**: ไม่มี session ทุก request ตอบได้ในตัวเอง Worker จึงขยายได้ไม่จำกัด
- **ไม่มี auth**: บทเรียนเป็นของสาธารณะอยู่แล้ว เครื่องมือทุกตัวอ่านอย่างเดียว (`readOnlyHint: true`)
- **มีแต่ notification → ตอบ 202 ไม่มี body** ตามสเปก Streamable HTTP
- **เปิดด้วย browser (GET) → ได้โน้ตสั้น ๆ** ให้คนที่เปิด URL รู้ว่ามาถูกที่:

```
$ curl -s https://aiexpo.buildwithoracle.com/mcp | jq .
{
  "server": {
    "name": "aiexpo-lessons",
    "title": "AIExpo Oracle lessons",
    "version": "2026.10.30-3"
  },
  "transport": "streamable-http (POST JSON-RPC here)",
  "tools": [
    "search",
    "fetch",
    "get_image",
    "list_lessons"
  ],
  "lessons": "https://aiexpo.buildwithoracle.com/"
}
(exit 0)
```

**การค้น (search)** ผสมสองอย่าง: แปลงคำถามเป็น vector ด้วย bge-m3 ตัวเดียวกับตอน build แล้ววัด cosine กับทุกชิ้น (น้ำหนัก 0.65) บวกคะแนนคำที่ตรงกัน (0.35) ภาษาไทยไม่มีช่องว่างระหว่างคำ จึงตัดคำด้วย `Intl.Segmenter("th")` ถ้า Workers AI ล่ม ยังค้นด้วยคำได้ และบอกในผลว่า `mode: keyword`

## 7. คุยกับ MCP บน Cloudflare ด้วย curl

ไม่ต้องมี client ก็ทดสอบได้ POST JSON ตรง ๆ:

```
$ curl -s -X POST $M -H 'content-type: application/json' -d '{initialize}' | jq '.result | {protocolVersion, serverInfo}'
{
  "protocolVersion": "2025-06-18",
  "serverInfo": {
    "name": "aiexpo-lessons",
    "title": "AIExpo Oracle lessons",
    "version": "2026.10.30-3"
  },
  "capabilities": {
    "tools": {
      "listChanged": false
    }
  }
}
(exit 0)
```

```
$ curl ... -d '{tools/list}' | jq -r '.result.tools[] | .name + ": " + .description[0:70]'
search: Search the AIExpo Oracle workshop lessons (Thai and English): installi
fetch: Read the full text of a search result. id '<lesson>/<lang>/<section>' 
get_image: Return screenshots as images the model can see. id is an image id from
list_lessons: List every lesson in workshop order, with page URLs, language editions
(exit 0)
```

ค้นเป็นภาษาไทย กรองเฉพาะฉบับไทย:

```
$ curl ... -d '{tools/call search {query: "ห้องเดียว หลาย agent", lang: th}}' | jq -r '.result.content[0].text | fromjson | .results[] | .id + "  " + .title' | head -3
herdr-room/th/1  ห้องเดียว หลาย agent: herdr-room in / out · 1. ห้อง (room) คืออะไร
herdr-room/th/8  ห้องเดียว หลาย agent: herdr-room in / out · 8. กับดัก: ร่างใหม่เกิดขณะร่างเก่ายังอยู่ในห้อง
herdr-room/th/9  ห้องเดียว หลาย agent: herdr-room in / out · 9. กฎที่ทีมได้มาจากการใช้จริง
(exit 0)
```

อ่านเต็มหัวข้อด้วย id ที่ได้จาก search:

```
$ curl ... -d '{tools/call fetch {id: "mcp-connect/en/2"}}' | jq -r '.result.content[0].text | fromjson | .text' | head -8
## 2. claude.ai

**2.1 Add a connector.** Go to **Customize → Connectors**, press **Add**, then **Add custom connector**.

![Customize, Connectors tab, with the Add menu open showing Add custom connector](https://aiexpo.buildwithoracle.com/2026-10-30_mcp-connect-guide/images/01-claude-add-connector-menu.png)

**2.2 Name and URL.** Any name, for example `AIExpo lessons`, and the URL `https://aiexpo.buildwithoracle.com/mcp`. Press **Continue**.

(exit 0)
```

ชื่อ `search` กับ `fetch` และรูปร่างผลลัพธ์ (`results[]` ที่มี `id title url`) ตั้งตามที่ ChatGPT connector และ deep research ต้องการ ตัวเดียวกันจึงใช้ได้ทั้ง claude.ai และ ChatGPT (วิธีต่อ อยู่ในบทเรียน [ต่อ claude.ai และ ChatGPT เข้ากับ MCP](../2026-10-30_mcp-connect-guide/th))

## 8. Deploy ขึ้น Cloudflare

```
$ cat wrangler.jsonc
// The lessons as a Worker on aiexpo.buildwithoracle.com: static assets, plus a read-only MCP endpoint at /mcp (worker.js, hybrid search over chunks.json with Workers AI bge-m3).
// Deploy: ./deploy.sh  (copies only committed files into dist/, then wrangler deploy)
{
  "name": "aiexpo-lessons",
  "main": "worker.js",
  "compatibility_date": "2026-10-01",
  "account_id": "a5eabdc2b11aae9bd5af46bd6a88179e",
  "ai": { "binding": "AI" },
  "assets": { "directory": "./dist", "binding": "ASSETS", "html_handling": "auto-trailing-slash", "run_worker_first": ["/mcp", "/mcp/*", "/*/videos/*"] },
  "routes": [{ "pattern": "aiexpo.buildwithoracle.com", "custom_domain": true }]
}
(exit 0)
```

- `run_worker_first` บอกว่า path ไหนให้ Worker ตอบก่อนไฟล์ static: `/mcp` ต้องอยู่ในนี้ ไม่งั้น assets จะตอบ 404 ก่อนถึงโค้ด
- `"ai": { "binding": "AI" }` ทำให้ `env.AI.run(...)` เรียก bge-m3 ได้จากใน Worker
- `deploy.sh` copy เฉพาะไฟล์ที่ commit แล้ว (`git archive HEAD`) ลง `dist/` แล้ว `wrangler deploy` ไฟล์ที่ยังไม่ commit จึงไม่หลุดขึ้นเว็บ

## 9. ตัว stdio จาก GitHub (server.mjs)

GitHub Pages เสิร์ฟได้แค่ไฟล์ ตอบ POST ไม่ได้ จึงเป็น MCP แบบ HTTP ไม่ได้ ทางออกคือให้ server รันในเครื่องเรา แล้วไปอ่าน `lessons.json` `chunks.json` `images.json` จาก Pages ([code/server.mjs](code/server.mjs) 232 บรรทัด)

- `package.json` ประกาศ `"bin": { "aiexpo-lessons": "mcp/server.mjs" }` คำสั่ง `npx -y github:<org>/<repo>` จึงดึง repo มารัน server ได้เลย ไม่ต้อง publish ขึ้น npm
- ค้นด้วยคำอย่างเดียว เพราะการแปลงคำถามเป็น vector ต้องใช้ bge-m3 บน Cloudflare
- ตั้ง `AIEXPO_DIR=/path/to/clone` ให้อ่านไฟล์จากดิสก์แทนเว็บได้ ใช้ offline ได้

```
$ printf initialize + tools/call search {query: "herdr room out"} | npx -y github:Caeruleus-Lab/aiexpo-lessons
{"serverInfo":{"name":"aiexpo-lessons","title":"AIExpo Oracle lessons (GitHub copy)","version":"2026.10.31-1"}}
{"id":"herdr-room/en/5","title":"One room, many agents: herdr-room in / out · 5. Room out: everyone back to a space of their own"}
{"id":"herdr-room/en/11","title":"One room, many agents: herdr-room in / out · 11. Full source of `herdr-room` (449 lines, python3)"}
{"id":"herdr-room/en/12","title":"One room, many agents: herdr-room in / out · 12. The full skill (`~/.claude/skills/herdr-room/SKILL.md`)"}
(exit 0)
```

ลงทะเบียนใน Claude Code: `claude mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons`

## 10. ทดสอบให้ครบ: เจ็ดคำสั่ง สอง server

[code/test-both.mjs](code/test-both.mjs) ส่งคำสั่งชุดเดียวกันเจ็ดอันให้ทั้งสองตัว ถ้าผลตรงกัน แปลว่าทั้งคู่พร้อมใช้:

```
$ node code/test-both.mjs     # the same 7 calls on the npx copy and the hosted copy
STDIO  npx -y github:Caeruleus-Lab/aiexpo-lessons
  initialize : server aiexpo-lessons 2026.10.31-1 proto 2025-06-18
  tools/list : tools: search, fetch, get_image, list_lessons
  tools/call list_lessons: text 12357 chars · {"lessons":[{"order":1,"id":"claude-chatgpt","title":{"th":"ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop",
  tools/call search: text 3770 chars · {"results":[{"id":"herdr-room/en/5","title":"One room, many agents: herdr-room in / out · 5. Room out: everyon
  tools/call search: text 3897 chars · {"results":[{"id":"ego-lite/th/4","title":"ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง · 4. ติดตั้งแ
  tools/call fetch: text 25126 chars · {"id":"herdr-room/en/11","title":"One room, many agents: herdr-room in / out · 11. Full source of `herdr-room`
  tools/call get_image: text 121 chars · image image/jpeg 65KB · ![herdr-room/01-room.png](https://caeruleus-lab.github.io/aiexpo-lessons/2026-10-31_herdr-room-lesson/images/0
HOSTED https://aiexpo.buildwithoracle.com/mcp
  initialize : server aiexpo-lessons 2026.10.30-3 proto 2025-06-18
  tools/list : tools: search, fetch, get_image, list_lessons
  tools/call list_lessons: text 11925 chars · {"lessons":[{"order":1,"id":"claude-chatgpt","title":{"th":"ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop",
  tools/call search: text 3901 chars · {"results":[{"id":"herdr-room/en/5","title":"One room, many agents: herdr-room in / out · 5. Room out: everyon
  tools/call search: text 3980 chars · {"results":[{"id":"ego-lite/th/4","title":"ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง · 4. ติดตั้งแ
  tools/call fetch: text 25102 chars · {"id":"herdr-room/en/11","title":"One room, many agents: herdr-room in / out · 11. Full source of `herdr-room`
  tools/call get_image: text 109 chars · image image/jpeg 65KB · ![herdr-room/01-room.png](https://aiexpo.buildwithoracle.com/2026-10-31_herdr-room-lesson/images/01-room.png)
(exit 0)
```

นอกจากสคริปต์นี้ ยังทดสอบด้วย client จริงอีกสามตัว: Claude Code (`claude -p --mcp-config`), Codex CLI และ session Claude Code ที่ใช้เขียนบทเรียนนี้เอง

## 11. กับดักที่เจอจริง

| อาการ | สาเหตุ | ทางแก้ |
|---|---|---|
| สคริปต์ Python เรียก `/mcp` ได้ 403 | Cloudflare บล็อก user agent `Python-urllib` | ส่ง header `User-Agent` ของตัวเอง |
| `claude -p` ตอบ "Not logged in" | โปรเซสใหม่ไม่ได้ token ที่ session หลักใช้ | ส่ง `CLAUDE_CODE_OAUTH_TOKEN` ให้โปรเซสนั้น (เราโหลดจาก `.envrc` ที่ไม่ commit) |
| `/mcp` ตอบ 404 | assets ตอบก่อน Worker | ใส่ `/mcp` ใน `run_worker_first` |
| ผลค้นภาษาไทยไม่เจอคำที่มีอยู่จริง | ภาษาไทยไม่มีช่องว่าง ตัดด้วย space ไม่ได้ | `Intl.Segmenter("th", { granularity: "word" })` |
| หัวข้อปลอมโผล่ใน chunks | `## ` ในบล็อกโค้ดถูกนับเป็นหัวข้อ | ตัดหัวข้อเฉพาะนอก ```` ``` ```` |
| ลิงก์จากผลค้นพาไปผิดหัวข้อ | เพิ่ม section ไว้หน้าบทเรียน id เลื่อน | section ใหม่ใช้ id ของตัวเอง (`#watch`) ให้ `#s2…` คงที่ |
| `get_image` ได้ error | ส่ง argument ชื่อผิด | argument ชื่อ `id` ดูชื่อจาก `tools/list` ทุกครั้ง |

```
$ curl -s -o /dev/null -w '%{http_code}' -A 'Python-urllib/3.12' $M   # Cloudflare bot rule
Python-urllib UA: 403
browser UA:       200
(exit 0)
```

## 12. ไฟล์ทั้งหมด

- [code/mini-mcp.mjs](code/mini-mcp.mjs): MCP ที่เล็กที่สุด (59 บรรทัด) จุดเริ่มของคุณ
- [code/worker.js](code/worker.js): MCP บน Cloudflare Worker ตัวจริง (343 บรรทัด)
- [code/server.mjs](code/server.mjs): MCP แบบ stdio ที่อ่านจาก GitHub Pages (232 บรรทัด)
- [code/test-both.mjs](code/test-both.mjs): ทดสอบเจ็ดคำสั่งบนทั้งสองตัว
- [captures/](captures/): ผลดิบ 14 ไฟล์ และ `capture.sh` ที่รันทั้งหมดซ้ำได้

ทำของตัวเอง: copy `mini-mcp.mjs` เปลี่ยน `NOTES` เป็นข้อมูลของคุณ เพิ่มเครื่องมือใน `TOOLS` และใน `switch` ของ `tools/call` แค่นั้นก็มี MCP ของตัวเองแล้ว
