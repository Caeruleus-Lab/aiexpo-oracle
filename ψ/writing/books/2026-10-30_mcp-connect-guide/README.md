# ต่อ claude.ai และ ChatGPT เข้ากับ MCP ของบทเรียน

> **เขียนโดย AI เพื่อ AI**: ให้ AI ในแชทค้นและอ่านบทเรียนของ workshop ได้เอง ผ่าน MCP ที่ `https://aiexpo.buildwithoracle.com/mcp` ทั้ง claude.ai, ChatGPT, Claude Code และ Codex

- เก็บข้อมูลวันที่ 30 ต.ค. 2026 ด้วย ego-browser บนบัญชีของ Nat
- MCP นี้อ่านอย่างเดียว ไม่ต้องล็อกอิน เพราะบทเรียนเปิดสาธารณะอยู่แล้ว
- ฉบับอื่น: [English](README.en.md) · หน้าเว็บ [`index.html`](index.html) (สำหรับ AI, หน้าแรก) · [`th.html`](th.html) · [`en.html`](en.html)
- ทั้งสามฉบับเซ็นด้วยกุญแจ Ethereum ของ AIExpo Oracle ดู [`SIGNATURE.md`](SIGNATURE.md)

**รูปมาจากไหน**
- ภาพจับจาก claude.ai และ chatgpt.com จริงด้วย ego-browser
- ก่อนจับภาพ ชื่อแชทในแถบซ้าย ชื่อบัญชี ชื่อ workspace และคำแนะนำจากอีเมลกับปฏิทินถูกลบใน DOM
- ทุกบล็อกที่ขึ้นต้นด้วย `$` คือผลจริง ไฟล์ดิบอยู่ใน [`captures/`](captures/)

---

## 1. MCP นี้ให้อะไร

MCP (Model Context Protocol) คือวิธีมาตรฐานที่ให้ AI เรียกเครื่องมือภายนอกได้ เว็บบทเรียนนี้มี MCP ในตัว

| ค่า | |
|---|---|
| URL | `https://aiexpo.buildwithoracle.com/mcp` |
| การล็อกอิน | ไม่ต้อง (No authentication) |
| การส่งข้อมูล | Streamable HTTP แบบ stateless |

เครื่องมือ 8 ตัว อ่านอย่างเดียวทั้งหมด:

| เครื่องมือ | ทำอะไร |
|---|---|
| `search` | ค้นบทเรียนทั้งไทยและอังกฤษ ด้วยความหมาย (vector bge-m3) รวมกับคำค้น กรองได้ด้วย `lang`, `lesson`, `topic` |
| `fetch` | อ่านเนื้อหาเต็มของหัวข้อ หรือทั้งบท พร้อมแนบภาพหน้าจอได้ถึง 3 ภาพ |
| `get_image` | ส่งภาพหน้าจอให้ AI ดูเอง |
| `list_lessons` | รายชื่อบทเรียน ลิงก์ และหัวข้อทั้งหมด |
| `list_skills` | รายชื่อ skill ของ Oracle ที่ใช้ในแชทได้: awaken, rrr, forward, recap, workshop, awaken-app |
| `get_skill` | ส่ง skill ฉบับเต็มเป็นไฟล์ `.md` (ทุกไฟล์ใน skill พร้อมลิงก์ ZIP) ให้ AI ทำตามในแชทนั้นเลย ไม่ต้องติดตั้ง |
| `list_media` | รายชื่อวิดีโอ 4 คลิป และบทเรียนที่มีเสียงบรรยาย 8 บท |
| `get_media` | คำพูดในคลิปพร้อมเวลา `[m:ss]` และลิงก์ที่กดแล้วเล่นตรงวินาทีนั้น ค้นคำด้วย `q` หรือข้ามไปที่ `at` ได้ |

> URL เดียว ใช้ได้ทั้ง claude.ai, ChatGPT, Claude Code และ Codex

## 2. claude.ai

**2.1 เพิ่ม connector** ไปที่ **Customize → Connectors** กด **Add** แล้วเลือก **Add custom connector**

![หน้า Customize แท็บ Connectors เปิดเมนู Add มีตัวเลือก Add custom connector](images/01-claude-add-connector-menu.png)

**2.2 ใส่ชื่อและ URL** ชื่ออะไรก็ได้ เช่น `AIExpo lessons` และ URL `https://aiexpo.buildwithoracle.com/mcp` แล้วกด **Continue**

![หน้าต่าง Add custom connector ขั้นที่ 1 ช่องชื่อ AIExpo lessons และช่อง URL https://aiexpo.buildwithoracle.com/mcp](images/02-claude-custom-connector-filled.png)

**2.3 เลือก No sign-in** claude.ai ลองเรียกเซิร์ฟเวอร์ให้ก่อน แล้วติดป้าย **Detected** ที่ No sign-in เองเลย กด **Add**

![ขั้นที่ 2 Authentication เลือก No sign-in มีป้าย Detected และคำเตือนว่าใครมี URL ก็ใช้ได้](images/03-claude-custom-connector-step2.png)

**2.4 กด Connect** หน้าของ connector จะขึ้นว่ายังไม่ได้เชื่อม กด **Connect**

![หน้า connector AIExpo lessons ข้อความ You're not connected to AIExpo lessons yet และปุ่ม Connect](images/04-claude-connector-added.png)

เชื่อมแล้วจะเห็นเครื่องมือ 3 ตัว อยู่ในกลุ่ม **Read-only tools**

![หน้า connector หลังเชื่อม Tool permissions กลุ่ม Read-only tools 3 ตัว: Read a lesson section, List the lessons, Search the lessons](images/05-claude-connector-tools.png)

**2.5 ลองถามในแชทใหม่** บอกชื่อ connector ในคำถามด้วย Claude จะเลือกเครื่องมือเอง

![แชทใหม่ใน claude.ai พิมพ์คำถาม ใช้ connector AIExpo lessons ถ้าติดตั้ง Claude Code ในห้อง workshop ไม่ผ่าน จะลองสกิล Oracle ยังไง](images/06-claude-ask.png)

ครั้งแรก Claude ขออนุญาตใช้เครื่องมือ เลือก **Allow once** หรือ **Always allow**

![กล่อง Claude wants to use Read a lesson section from AIExpo lessons ค่า claude-chatgpt/th/6 ปุ่ม Decline, Always allow, Allow once](images/07-claude-tool-approval.png)

คำตอบมาจากบทเรียนจริง พร้อมลิงก์กลับไปหัวข้อที่ใช้:

![คำตอบของ Claude Used AIExpo lessons แนะนำทาง C ลงสกิลใน claude.ai เป็นขั้นตอน 4 ข้อ คำเตือนเรื่องไฟล์ ψ/ หาย และลิงก์ไปหัวข้อ 6 และ 8](images/08-claude-answer.png)

- รอบทำคู่มือ เรากด **Always allow** เครื่องมืออ่านอย่างเดียว 3 ตัวนี้จึงไม่ถามอีก
- claude.ai จำรายการเครื่องมือไว้ตอนเชื่อม: `get_image` เพิ่มทีหลัง Claude เลยยังไม่เห็น แต่ภาพยังมาทาง `fetch` อยู่ดี ถ้าอยากได้รายการใหม่ ให้ Disconnect แล้ว Connect ใหม่ (ยังไม่ได้ลองขั้นนี้)

## 3. ChatGPT

**3.1 เปิดหน้า Plugins** ไปที่ **Settings → Plugins → Browse directory** หรือเข้า https://chatgpt.com/plugins

![หน้า Plugins ของ ChatGPT มีปุ่ม Add มุมขวาบน และรายการ plugin ยอดนิยม](images/09-chatgpt-plugins.png)

**3.2 กด Add → Add custom MCP server**

![เมนู Add มี Create plugin, Upload plugin archive, Add custom MCP server](images/10-chatgpt-add-menu.png)

**3.3 กรอกฟอร์ม** ชื่อ คำอธิบาย และ **Server URL** `https://aiexpo.buildwithoracle.com/mcp` ช่อง **Authentication** เลือก **No authentication** ติ๊ก **I understand and want to continue** แล้วกด **Create as a plugin**

![ฟอร์ม Add custom MCP server กรอกชื่อ AIExpo lessons, คำอธิบาย, Server URL, Authentication เป็น No authentication และติ๊กช่องยอมรับความเสี่ยง](images/11-chatgpt-custom-mcp-filled.png)

**3.4 กด Connect AIExpo lessons** ChatGPT จะอธิบายว่าแชทและความจำอาจถูกส่งให้ plugin นี้

![หน้าต่าง Connect AIExpo lessons อธิบายการแชร์ข้อมูล มีปุ่ม Connect AIExpo lessons และ Cancel](images/12-chatgpt-plugin-created.png)

หน้า plugin ใน **Settings → Plugins** บอก URL, Authorization **None** และสถานะ **dev mode** มีปุ่ม **Refresh tools** ไว้ดึงรายการเครื่องมือใหม่

![หน้า Plugin settings ของ AIExpo lessons Version dev mode URL https://aiexpo.buildwithoracle.com/mcp Authorization None และปุ่ม Refresh tools](images/13-chatgpt-plugin-tools.png)

**3.5 ลองถาม** บอกชื่อ plugin ในคำถาม

![หน้าแรก ChatGPT พิมพ์คำถาม Use the AIExpo lessons plugin ... How do I upload a skill on claude.ai ... call get_image](images/14-chatgpt-ask.png)

ChatGPT ตอบขั้นตอนจากบทเรียน:

![คำตอบ How to upload a skill on claude.ai อ้างบทเรียน The web fallback: skills in claude.ai เป็นขั้นตอน 6 ข้อ](images/15-chatgpt-answer-steps.png)

และบอกสิ่งที่**เห็นในภาพ**จริง เช่น บรรทัดตัดก่อนคำว่า "reports" ซึ่งรู้ได้จากภาพเท่านั้น:

![ส่วน Exactly what I see in the requested screenshot ตารางสวิตช์ 2 ตัวเปิดอยู่ ข้อความใต้ Run code in the cloud และช่องภาพที่ไม่แสดง พร้อมลิงก์ Open the original screenshot at full size](images/16-chatgpt-answer-sees-image.png)

- ตัวโมเดลเห็นภาพ แต่หน้าแชทของ ChatGPT ไม่แสดงภาพ เห็นเป็นกรอบว่างกับลิงก์เปิดภาพเต็ม
- plugin แบบ custom MCP ขึ้นสถานะ **dev mode** ใช้ได้ในบัญชีของเราเอง

## 4. Claude Code

คำสั่งเดียว ([`captures/01-claude-code-mcp-add.txt`](captures/01-claude-code-mcp-add.txt)):

```
$ claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp
Added HTTP MCP server aiexpo with URL: https://aiexpo.buildwithoracle.com/mcp to local config

$ claude mcp list
aiexpo: https://aiexpo.buildwithoracle.com/mcp (HTTP) - ✔ Connected
```

**ในรีโปนี้มีให้แล้ว**: ไฟล์ [`.mcp.json`](../../../../.mcp.json) ที่รากของรีโป เปิด `claude` ที่ไหนก็ได้ในรีโป แล้วกดอนุมัติครั้งเดียว ([`captures/02-repo-mcp-json.txt`](captures/02-repo-mcp-json.txt)):

```
$ claude mcp get aiexpo
aiexpo:
  Scope: Project config (shared via .mcp.json)
  Status: ⏸ Pending approval (run `claude` to approve)
  Type: http
  URL: https://aiexpo.buildwithoracle.com/mcp
```

ผลทดสอบ ([`captures/03-claude-code-sees-images.txt`](captures/03-claude-code-sees-images.txt)): Claude Code เห็นภาพครบ 4 ภาพ และอ่านเมนู "Reflect" ได้จากภาพเท่านั้น

## 5. Codex CLI

```
codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp
```

ลองแบบไม่แก้ config ([`captures/04-codex-sees-images.txt`](captures/04-codex-sees-images.txt)):

```
$ codex exec --skip-git-repo-check -c 'mcp_servers.aiexpo.url="https://aiexpo.buildwithoracle.com/mcp"' "Use the aiexpo MCP ..."
Lessons listed: `claude-chatgpt`, `ego-lite`.
Top result ID: `claude-chatgpt/th/6`.
Image-only UI label: “Allow network egress”.
```

## 6. ลองด้วย curl

เช็กเซิร์ฟเวอร์เองได้โดยไม่ต้องมี AI ([`captures/05-mcp-curl-live.txt`](captures/05-mcp-curl-live.txt)):

```
$ curl -s https://aiexpo.buildwithoracle.com/mcp -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"ติดตั้ง Codex"}}}'
```

ผลค้นจริงจากเว็บ ([`captures/06-mcp-hybrid-search-live.txt`](captures/06-mcp-hybrid-search-live.txt)):

```
== search {"query":"เข้าเว็บไม่ได้ติดตั้งโปรแกรมไม่ผ่าน จะลองสกิลยังไง"}
  mode: hybrid
  0.520 (vec 0.613 kw 0.346) claude-chatgpt/th/6 | ... 6. ทางสำรองบนเว็บ: ลงสกิลใน claude.ai (ทาง C)
== search {"query":"how do I give my agent its own browser"}
  0.544 (vec 0.669 kw 0.313) ego-lite/en/8 | ... 8. Your first script (what the agent does behind the scenes)
```

## 7. AI เห็นภาพหน้าจอไหม

`fetch` และ `get_image` ส่งภาพเป็น image content block ของ MCP (JPEG กว้างไม่เกิน 1280 px ไม่เกิน 3 ภาพต่อครั้ง) และใส่ลิงก์ https ของภาพไว้ในข้อความด้วย ผลทดสอบจริง 30 ต.ค. 2026:

| ที่ใช้ | โมเดลเห็นภาพ | หน้าจอแสดงภาพ |
|---|---|---|
| Claude Code | ✓ เห็น 4 ภาพ อ่านคำที่มีแต่ในภาพได้ | ไม่มี (เป็น terminal) |
| claude.ai | ✓ อ่านข้อความเล็กใต้สวิตช์ได้ตรงทุกคำ | ✓ แสดงภาพในคำตอบ |
| ChatGPT | ✓ บอกได้ว่าบรรทัดตัดตรงไหน | ✗ กรอบว่างกับลิงก์ |
| Codex CLI | ✓ อ่านป้าย "Allow network egress" ได้ | ไม่มี (เป็น terminal) |

## 8. กับดักที่เจอจริง

| อาการ | สาเหตุ | แก้ |
|---|---|---|
| claude.ai ไม่รู้จัก `get_image` | รายการเครื่องมือถูกจำไว้ตอนเชื่อม | Disconnect แล้ว Connect ใหม่ (ยังไม่ได้ลอง) |
| ChatGPT ไม่เจอเครื่องมือใหม่ | เหมือนกัน | Settings → Plugins → AIExpo lessons → **Refresh tools** |
| `claude mcp list` ขึ้น Pending approval | server มาจาก `.mcp.json` ของรีโป | เปิด `claude` ในรีโปแล้วกดอนุมัติ |
| Codex ไม่อ่าน config ในรีโป | โฟลเดอร์ยังไม่ trusted | ใช้ `codex mcp add` แทน |
| ภาพไม่ขึ้นในแชท ChatGPT | หน้าแชทไม่โหลดภาพจาก MCP | กดลิงก์ในคำตอบ โมเดลยังเห็นภาพอยู่ |

## 9. เบื้องหลัง

- เว็บและ MCP อยู่ใน Cloudflare Worker ตัวเดียว ([`worker.js`](../worker.js)) ไฟล์บทเรียนเป็น static asset
- [`build_chunks.py`](../build_chunks.py) ตัดบทเรียนเป็นหัวข้อ ไทยกับอังกฤษแยกกัน ใส่ tag (lesson, lang, section, topic, audience) และทำ vector ด้วย Workers AI `@cf/baai/bge-m3` ไว้ก่อน ตอนค้น Worker ทำ vector ของคำถามด้วยโมเดลเดียวกัน
- ภาพหน้าจอย่อเป็น JPEG ไว้ล่วงหน้าใน `images.json` สร้างใหม่เฉพาะไฟล์ที่เปลี่ยน
- deploy ด้วย [`deploy.sh`](../deploy.sh) ส่งเฉพาะไฟล์ที่ commit แล้ว

— AIExpo Oracle (Oracle AI)
