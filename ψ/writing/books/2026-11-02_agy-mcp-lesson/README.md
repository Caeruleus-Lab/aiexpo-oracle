# ใช้ Antigravity CLI (agy) กับ MCP ของบทเรียน

> บทเรียนนี้พาติดตั้ง Antigravity CLI ของ Google (คำสั่ง `agy`) ล็อกอินครั้งแรก แล้วต่อเข้ากับ MCP ของบทเรียน AIExpo ทั้งตัวบน Cloudflare และตัวที่รันในเครื่อง คำสั่ง `agy` ทุกบรรทัดรันจริงวันที่ 2 พ.ย. 2026 บน agy 1.4.12 ผลดิบอยู่ใน [captures/](captures/) เขียนโดย AI สำหรับคนและ AI ลงลายเซ็นทั้งสามฉบับด้วยกุญแจ Ethereum ดอกเดียว

- การติดตั้งและล็อกอินครั้งแรกทำครั้งเดียวต่อเครื่อง ต้องมีคนกดเอง ขั้นตอนข้อ 2-5 จดจากการติดตั้งจริงบนเครื่องนี้เช้าวันเดียวกัน
- มีกับดักสองอันที่เจอจริงตอนล็อกอิน: URL ขาดจน Google ตอบ `invalid_scope` กับกล่องแชร์ข้อมูลที่ติ๊กไว้ให้แล้ว
- บทเรียนที่ต่อกัน: [สร้าง MCP ของตัวเอง](../2026-11-02_build-mcp-lesson/th) เล่าว่า MCP ที่เราต่อในบทนี้ทำงานยังไง
- ฉบับอื่น: [English](README.en.md)
- เรียบเรียงโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. Antigravity CLI คืออะไร

Antigravity CLI คือ coding agent ของ Google ที่รันใน terminal คำสั่งชื่อ `agy` ใช้โมเดล Gemini ตามบัญชีที่ล็อกอิน (เครื่องนี้เป็น Google AI Pro โมเดล "Gemini 4 Argon (Medium)")

- **แอป Antigravity บนเดสก์ท็อป (2.3.1) ไม่มีคำสั่ง `agy` มาให้** ต้องติดตั้ง CLI แยก
- `agy` ต่อ MCP ได้ทั้งสองแบบ: `http` (URL) กับ `stdio` (คำสั่งที่รันในเครื่อง)

```
$ agy --version
1.4.12
(exit 0)
```

![สรุปบนหน้าจอ: เพิ่ม MCP สองตัวใน agy, agy mcp list ขึ้น enabled ทั้งคู่, agy -p ตอบจาก aiexpo-github ว่ามี 7 บทเรียน และกับดักสามอันตอนล็อกอินและตอนเพิ่ม](images/01-agy-mcp.png)

## 2. ติดตั้ง

คำสั่งทางการ:

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

- ต้องมี `/cli/` ในพาธ `https://antigravity.google/install.sh` ที่บางเอกสารเขียนไว้ตอบ 404
- **อ่านสคริปต์ก่อนรัน** (`curl -fsSL ... | less`) สิ่งที่มันทำ:
  - ไม่ใช้ sudo
  - ดาวน์โหลดตัวโปรแกรมจาก updater บน Google Cloud Run แล้วตรวจ SHA-512
  - วางไว้ที่ `~/.local/bin/agy` แล้วลบ flag quarantine ของ macOS
  - `agy install` เติม `export PATH="$HOME/.local/bin:$PATH"` ลงทั้ง `~/.zshrc` และ `~/.profile`
- ระหว่างติดตั้งจะเห็นบรรทัด `ERROR: logging before google.Init: I1102 ...` นี่เป็น log ระดับ INFO (ตัว `I` นำหน้า) ไม่ใช่ error จริง สคริปต์จบด้วย exit 0
- จบแล้วจะขึ้น `✅ Antigravity CLI installed successfully at ~/.local/bin/agy` เปิด terminal ใหม่ หรือ `source ~/.zshrc` แล้วลอง `agy --version`

## 3. ล็อกอินครั้งแรก

พิมพ์ `agy` (หรือ `agy -p` ครั้งแรก) จะขึ้น URL สำหรับล็อกอิน Google

1. เปิด URL ด้วย **"→ Click here to authenticate"** (อย่า copy เอง ดูข้อ 4)
2. ล็อกอินบัญชี Google หน้า antigravity.google จะโชว์รหัสขึ้นต้นด้วย `4/0...`
3. วางรหัสใน prompt ของ agy กด Enter (`agy -p` รอรหัสแค่ 60 วินาที ถ้าช้าให้ล็อกอินผ่าน `agy` ธรรมดาก่อน)
4. หน้าถัดไปถามเรื่องแชร์ข้อมูล ดูข้อ 5
5. "Do you trust the contents of this project?" ตอบ **Yes, I trust this folder** เฉพาะโฟลเดอร์ที่เราไว้ใจจริง

เสร็จแล้ว banner จะบอกเวอร์ชัน แผนของบัญชี และโมเดล

## 4. กับดัก: URL ขาด จน Google ตอบ invalid_scope

URL ล็อกอินยาวมาก agy วางไว้ในกล่องที่มี pager (`(1–16 of 29 lines)` เลื่อนด้วย shift+↑/↓) ถ้าลากเมาส์ copy แค่ส่วนที่เห็น URL จะขาดกลางคำ

ที่เจอจริง: URL ขาดตรงกลางคำ `experimentsandconfigs` Google ตอบหน้า

```
Access blocked: Authorization Error
Error 400: invalid_scope (invalid=.../auth/experiments)
```

- **ทางแก้**: กด "→ Click here to authenticate" หรือเลื่อนกล่องจนสุด URL ที่ครบจะจบด้วย `&state=...`
- บทเรียนทั่วไป: error ที่บอกว่า scope ผิด มักไม่ใช่ปัญหาสิทธิ์ แต่เป็น URL ที่ไม่ครบ

## 5. กับดัก: กล่องแชร์ข้อมูลที่ติ๊กไว้ให้แล้ว

หลังวางรหัส จะเจอกล่องนี้ **ติ๊กไว้ให้แล้ว**:

```
[x] Yes, I agree to help improve Antigravity CLI by allowing Google to collect and use my Interactions data
```

- ถ้ากด Done เลย แปลว่ายอมให้ Google เก็บบทสนทนาไปใช้
- Nat เลือกเอาติ๊กออก: กด Enter ที่กล่องเพื่อสลับ แล้วค่อย Done
- เวิร์กช็อปนี้แนะนำ: อ่านทุกกล่องก่อนกด Done โดยเฉพาะกล่องที่ติ๊กมาให้แล้ว เลือกเองว่าจะแชร์หรือไม่

## 6. คำสั่ง agy mcp

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

ตัวเลือกของ `add`:

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

สองบรรทัดที่สำคัญที่สุดใน Notes:

- **flag ต้องมาก่อน `<name>`** วางหลังชื่อจะโดนปฏิเสธ ด้วย error ที่ไม่ได้พูดถึง flag เลย (ข้อ 8)
- URL ที่ขึ้นต้นด้วย http/https ถูกจับเป็น `http` อัตโนมัติ ไม่ต้องใส่ `--type`

## 7. เพิ่ม MCP ของบทเรียน

สองตัว เครื่องมือชุดเดียวกัน (`search` `fetch` `get_image` `list_lessons`):

- `aiexpo`: ตัวบน Cloudflare ค้นได้ทั้งความหมายและคำ
- `aiexpo-github`: ตัวที่ `npx` ดึงจาก GitHub มารันในเครื่อง ค้นด้วยคำ ใช้ได้แม้ Cloudflare ล่ม

```
$ agy mcp add aiexpo https://aiexpo.buildwithoracle.com/mcp; agy mcp add aiexpo-github npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
Added MCP server "aiexpo" (http)
Added MCP server "aiexpo-github" (stdio)
(exit 0)
```

`add` คือ "add or update" รันซ้ำได้ ไม่สร้างซ้ำ

```
$ agy mcp list
NAME           TYPE   STATUS   COMMAND/URL
aiexpo         http   enabled  https://aiexpo.buildwithoracle.com/mcp
aiexpo-github  stdio  enabled  npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
(exit 0)
```

ถ้าเครื่องมี MCP ตัวอื่นอยู่แล้ว จะเห็นในรายการนี้ด้วย (ใน capture ตัดออก)

## 8. กับดัก: flag วางหลังชื่อ

```
$ agy mcp add try-x https://example.com/mcp --header 'X-Test: 1'   # flag after the name
Error: http server type does not accept command arguments
(exit 1)
```

error ไม่ได้บอกตรง ๆ ว่า flag อยู่ผิดที่ ทุกอย่างหลัง `<commandOrUrl>` ถูกนับเป็น argument ของคำสั่ง แต่ server แบบ http ไม่มีคำสั่งให้ส่ง argument จึงตอบ `http server type does not accept command arguments` ถ้าเห็น error นี้ ให้ดูลำดับ flag ก่อน

วางใหม่ให้ถูก: `agy mcp add --header "X-Test: 1" try-x https://example.com/mcp` (สคริปต์ capture ลบ `try-x` ทิ้งถ้ามันถูกเพิ่มเข้าไป)

## 9. ปิดชั่วคราว แล้วเปิดคืน

ไม่ต้องลบ ปิดไว้ก่อนได้:

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

## 10. ทดสอบด้วย agy -p

`-p` คือถามครั้งเดียวแล้วจบ เหมาะกับสคริปต์และการทดสอบ flag ที่ใช้:

- `--sandbox`: ให้ agent ทำงานใน sandbox
- `--dangerously-skip-permissions`: ไม่ต้องถามก่อนใช้เครื่องมือ ใน `-p` ไม่มีใครกดอนุญาตให้ จึงต้องใช้ ใช้เฉพาะคู่กับ `--sandbox` และกับ MCP ที่อ่านอย่างเดียวแบบนี้
- `--print-timeout 240s`: รอคำตอบนานสุด 4 นาที

ถามผ่านตัวบน Cloudflare:

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

ถามผ่านตัวจาก GitHub:

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

ทั้งสองตัวตอบจากบทเรียนจริง พร้อมบอกชื่อเครื่องมือที่เรียก ถ้า agy ตอบโดยไม่เรียกเครื่องมือเลย ให้ตรวจ `agy mcp list` ว่า `STATUS` เป็น `enabled`

## 11. กับดักทั้งหมดในที่เดียว

| อาการ | สาเหตุ | ทางแก้ |
|---|---|---|
| `install.sh` ตอบ 404 | ใช้ URL ที่ไม่มี `/cli/` | `https://antigravity.google/cli/install.sh` |
| เห็น `ERROR: logging before google.Init` ตอนติดตั้ง | log ระดับ INFO | ไม่ต้องทำอะไร ดู exit code |
| หาคำสั่ง `agy` ไม่เจอ ทั้งที่มีแอป Antigravity | แอปเดสก์ท็อปไม่มี CLI มาด้วย | ติดตั้ง CLI แยก |
| `Error 400: invalid_scope` | copy URL ล็อกอินไม่ครบ | กด "Click here to authenticate" หรือเลื่อนจนเห็น `&state=` |
| ยอมแชร์ข้อมูลโดยไม่รู้ตัว | กล่องติ๊กมาให้แล้ว | Enter เพื่อเอาติ๊กออก ก่อน Done |
| `agy -p` ล็อกอินไม่ทัน | รอรหัสแค่ 60 วินาที | ล็อกอินด้วย `agy` ธรรมดาก่อน |
| `http server type does not accept command arguments` | flag อยู่หลังชื่อ ถูกนับเป็น argument | flag ทั้งหมดไว้ก่อน `<name>` |

## 12. ไฟล์ทั้งหมด

- [captures/](captures/): ผลดิบ 9 ไฟล์ และ `capture.sh` ที่รันทั้งหมดซ้ำได้ (ต้องติดตั้งและล็อกอิน agy ก่อน)
- MCP บน Cloudflare: `https://aiexpo.buildwithoracle.com/mcp`
- MCP แบบ stdio: `npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp`
