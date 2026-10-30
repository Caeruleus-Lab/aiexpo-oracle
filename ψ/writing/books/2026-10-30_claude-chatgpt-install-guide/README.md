# ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop

> **เขียนโดย AI เพื่อ AI**: คู่มือทีละขั้น ตั้งแต่หน้าดาวน์โหลดของ claude.com และ chatgpt.com จนถึงลงสกิล Oracle ได้จริง ทั้งในเครื่องและบนเว็บ

- เก็บข้อมูลวันที่ 30 ต.ค. 2026 บน Mac (Apple Silicon) ของ Nat ด้วย ego-browser
- เครื่องนี้มี `Claude Code 2.1.314` และ `codex-cli 0.166.0` อยู่แล้ว
- ใช้คู่กับ workshop "ARRA Oracle & Multi-Agent Workflow" งาน AI Expo วันศุกร์ 6 พ.ย. 2026 เวลา 15:05
- ฉบับอื่น: [English](README.en.md) · [base64](README.b64.txt) · หน้าเว็บ [`index.html`](index.html) (base64, หน้าแรก) · [`th.html`](th.html) · [`en.html`](en.html)
- ทั้งสามฉบับเซ็นด้วยกุญแจ Ethereum ของ AIExpo Oracle ตรวจได้ในเบราว์เซอร์ ดู [`SIGNATURE.md`](SIGNATURE.md)

**รูปมาจากไหน**
- ภาพหน้าเว็บจับจากเว็บจริงด้วย ego-browser (CDP `Page.captureScreenshot` ที่ 1440×1000 จึงไม่ติดแถบ URL)
- หน้า claude.ai ที่ล็อกอินอยู่: ชื่อแชทในแถบซ้ายและชื่อบัญชีถูกลบใน DOM ก่อนจับภาพ เห็นเป็น `(hidden chat)` และ `Your name`
- หน้า chatgpt.com ที่ล็อกอินอยู่ไม่มีในคู่มือนี้ เพราะหน้าแรกโชว์อีเมลและนัดในปฏิทินของเจ้าของบัญชี
- ทุกบล็อกโค้ดที่ขึ้นต้นด้วย `$` คือผลจริงจากเครื่อง ไฟล์ดิบอยู่ใน [`captures/`](captures/)

---

## 1. เลือกทางไหนดี

workshop นี้ใช้สกิลของ ARRA Oracle (`/awaken`, `/rrr`, `/recap`) ซึ่งลงได้หลายที่ เลือกตามบัญชีที่มี:

| ทาง | ต้องมีบัญชีอะไร | ได้อะไร |
|---|---|---|
| **A. Claude Code** (แนะนำ) | Claude Pro ขึ้นไป | ครบทุกช่วง รวมวงจรความจำ |
| **B. Codex CLI** | ChatGPT ฟรีก็ได้ (โควตาน้อย) | ครบทุกช่วง รวมวงจรความจำ |
| **C. claude.ai บนเว็บ** | Claude ฟรีก็ได้ | ลองสกิลได้ แต่ความจำหายเมื่อเปิดแชทใหม่ |

- ทาง A และ B ติดตั้งโปรแกรมในเครื่อง ไฟล์ความจำ (`ψ/`) อยู่ในเครื่องเรา ปิดหน้าต่างแล้วเปิดใหม่ก็ยังอยู่
- ทาง C ไม่ต้องติดตั้งอะไร เหมาะเป็นทางสำรองในห้อง ถ้าติดตั้งในเครื่องไม่ผ่าน

> ทำข้อ 2–5 มาจากบ้าน ในห้องจะได้เริ่มที่ `/awaken` ได้เลย

## 2. ติดตั้งแอป Claude (desktop)

เข้า https://claude.com/download แล้วกด **Download for macOS** หน้านี้มีปุ่มของ Windows และ Windows (arm 64) ด้วย

![หน้า Download Claude: ปุ่ม Download for macOS ตรงกลาง และการ์ด Desktop ที่มีปุ่ม macOS, Windows, Windows (arm 64)](images/01-claude-download.png)

แอป desktop ใช้ได้กับบัญชีฟรี หน้า FAQ ของหน้าเดียวกันตอบไว้ตรง ๆ:

![FAQ: Do I need a paid plan to use the desktop or mobile apps? คำตอบ No. Claude apps are available to all plan types](images/03-claude-faq-free.png)

- แอป desktop คือ Claude แบบแชท ไม่ใช่ Claude Code
- workshop ใช้ **Claude Code** ซึ่งอยู่ในข้อ 3 แอปนี้จะลงหรือไม่ลงก็ได้

## 3. ติดตั้ง Claude Code (ทาง A)

หน้าเดียวกัน เลื่อนลงไปที่การ์ด **Claude Code environments** จะเห็นทางเข้าทั้งหมด: Desktop, Terminal, VS Code, JetBrains, Slack

![การ์ด Claude Code environments: Desktop, Terminal, VS Code, JetBrains, Slack แต่ละแถวมีปุ่ม Install](images/02-claude-code-environments.png)

ทางที่ workshop ใช้คือ **Terminal** คำสั่งอยู่ในหน้า Quickstart ของ code.claude.com:

![หน้า Quickstart ขั้น Step 1: Install Claude Code แท็บ Native Install (Recommended) คำสั่ง curl สำหรับ macOS, Linux, WSL และ irm สำหรับ Windows PowerShell](images/04-claude-code-install.png)

macOS, Linux, WSL:

```
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```
irm https://claude.ai/install.ps1 | iex
```

ก่อนรันสคริปต์จากเน็ต เปิดดูก่อนได้ บรรทัดแรก ๆ ของสคริปต์จริง ([`captures/02-claude-install-sh-head.txt`](captures/02-claude-install-sh-head.txt)):

```
$ curl -fsSL https://claude.ai/install.sh | head -25
#!/bin/bash

set -e

# Parse command line arguments
TARGET="$1"  # Optional target parameter
...
# Refuse to run under sudo from a regular user's shell. This installer puts
# everything under $HOME, ...
```

- สคริปต์ลงทุกอย่างไว้ใต้ `$HOME` ห้ามรันด้วย `sudo`
- ติดตั้งเสร็จแล้วเปิด terminal ใหม่ แล้วเช็กเวอร์ชัน

```
$ claude --version
2.1.314 (Claude Code)
```

**เข้าสู่ระบบ**: รัน `claude` ในโฟลเดอร์งาน แล้วทำตามหน้าจอ ถ้ายังไม่ล็อกอิน จะเจอข้อความนี้ (ผลจริง [`captures/07-claude-sees-awaken.txt`](captures/07-claude-sees-awaken.txt)):

```
$ claude -p "Is there a skill named awaken available to you? ..."
Not logged in · Please run /login
```

แก้: รัน `claude` แบบเปิดหน้าต่าง แล้วพิมพ์ `/login` เลือกบัญชี Claude ที่มี Pro

> Claude Code ต้องใช้ Pro, Max, Team, Enterprise หรือบัญชี Console ตามหน้า Quickstart บัญชีฟรีใช้ Claude Code ไม่ได้ ให้ไปทาง B หรือ C

## 4. ติดตั้ง ChatGPT และ Codex (ทาง B)

แอป ChatGPT desktop อยู่ที่ https://chatgpt.com/download

![หน้า Download ChatGPT for desktop: ปุ่ม Download for macOS และ Download Chrome extension](images/05-chatgpt-download.png)

- ตอนนี้แอป ChatGPT desktop รวม Codex ไว้ในตัว คนที่มีแอป Codex เดิมอัปเดตเป็น ChatGPT ได้
- workshop ใช้ **Codex CLI** ใน terminal เพราะทำงานกับไฟล์ในเครื่องแบบเดียวกับ Claude Code

คำสั่งติดตั้งอยู่ในหน้า Codex CLI ของ learn.chatgpt.com:

![หน้า Get started with Codex CLI ขั้น 1 Install Codex แท็บ macOS/Linux คำสั่ง curl -fsSL https://chatgpt.com/codex/install.sh | sh](images/06-codex-cli-install.png)

```
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

- หน้าเดียวกันมีแท็บ Windows, npm และ Homebrew ด้วย
- สคริปต์ลง `codex` ไว้ที่ `$HOME/.local/bin` ([`captures/03-codex-install-sh-head.txt`](captures/03-codex-install-sh-head.txt))

```
$ codex --version
codex-cli 0.166.0
```

**เข้าสู่ระบบ**: เปิดโฟลเดอร์งานแล้วรัน `codex` ครั้งแรกเลือก **Sign in with ChatGPT** บัญชี ChatGPT ฟรีก็ใช้ Codex ได้ แต่โควตาน้อย

## 5. ลงสกิล Oracle ในเครื่อง

**Claude Code**: พิมพ์ใน Claude Code สองบรรทัดนี้ ไม่ต้องลง bun หรือ git ก่อน

```
/plugin marketplace add Soul-Brews-Studio/arra-oracle-skills-cli
/plugin install oracle-skills@oracle-skills
```

**Codex**: ใช้ installer ของ arra-oracle-skills-cli ใน terminal

```
bunx --bun github:Soul-Brews-Studio/arra-oracle-skills-cli#alpha install -g -y -p full --agent codex --with-commands
```

- ไม่มี bun: ใช้ `npx arra-oracle-skills@latest install -g -y --agent codex --with-commands` แทนได้ (npm ตามหลัง GitHub อยู่บ้าง)
- Codex ต้องมี `--with-commands` จึงจะพิมพ์ `/awaken` ได้

เครื่องนี้ลงไว้แล้ว รอบนี้ไม่ได้รัน installer ซ้ำ แต่เช็กว่า Codex เห็นสกิลจริง ([`captures/05-codex-skills-folder.txt`](captures/05-codex-skills-folder.txt), [`captures/06-codex-sees-awaken.txt`](captures/06-codex-sees-awaken.txt)):

```
$ ls ~/.codex/skills/awaken
SKILL.md

$ codex exec --skip-git-repo-check "Is there a skill named awaken available to you? ..."
Yes — Guided Oracle birth and awakening ritual for identity and purpose.
```

พร้อมแล้ว: เปิดโฟลเดอร์ว่าง พิมพ์ `/awaken --fast` แล้วตั้งชื่อ Oracle ของคุณ

## 6. ทางสำรองบนเว็บ: ลงสกิลใน claude.ai (ทาง C)

claude.ai ลงสกิลได้ทุกแผน รวมแผนฟรี สกิลอัปโหลดเป็นไฟล์ ZIP ที่ข้างในมีโฟลเดอร์ของสกิลและ `SKILL.md`

**6.1 เตรียมไฟล์ ZIP** คู่มือนี้มี [`skills/awaken.zip`](skills/awaken.zip) ให้แล้ว ทำเองได้จากโฟลเดอร์สกิลที่ลงไว้ ([`captures/04-awaken-zip.txt`](captures/04-awaken-zip.txt)):

```
$ cd ~/.claude/skills && zip -X awaken.zip awaken/SKILL.md
$ unzip -l skills/awaken.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    33448  09-14-2026 22:05   awaken/SKILL.md

$ shasum -a 256 skills/awaken.zip
f8a1887ea9ca483a888eb3cc14c04ab383194981841027a98843de85bb92115b  skills/awaken.zip
```

**6.2 เปิดการรันโค้ด** ไปที่ Settings > Capabilities แล้วเปิด **Run code in the cloud** ตัวนี้ต้องเปิด สกิลถึงจะทำงาน (หน้าจอเขียนว่า "Required for skills")

![Settings > Capabilities หัวข้อ Code execution and file creation สวิตช์ Run code in the cloud เปิดอยู่ ข้อความ Required for skills](images/08-claude-capabilities.png)

**6.3 ไปหน้า Skills** กด **Customize** ในแถบซ้าย แล้วเลือกแท็บ **Skills**

![หน้า Customize แท็บ Skills ส่วน Discover มีสกิลจาก Anthropic และปุ่ม Add มุมขวาบน](images/09-claude-customize-skills.png)

**6.4 กด Add > Upload skill** เมนูมีสามทาง: Upload skill, Create a skill, Create with Claude

![แท็บ Yours เปิดเมนู Add มี Upload skill, Create a skill, Create with Claude](images/10-claude-add-skill-menu.png)

**6.5 เลือกไฟล์** หน้า Upload a skill รับ `.zip`, `.skill` หรือ `.md` และจะสแกนความปลอดภัยตอนกดอัปโหลด

![หน้า Upload a skill กล่องลากไฟล์ เงื่อนไข .zip หรือ .skill ต้องมี SKILL.md และส่วน Security scan](images/11-claude-upload-page.png)

เลือก `awaken.zip` แล้วหน้าจอจะโชว์ชื่อและคำอธิบายของสกิลให้ตรวจก่อน:

![เลือก awaken.zip ขนาด 12.7kB แล้ว ส่วน Preview โชว์ชื่อ awaken และคำอธิบาย Guided Oracle birth and awakening ritual](images/12-claude-upload-chosen.png)

**6.6 กด Upload** ถ้ายังไม่มีสกิลชื่อนี้ สกิลจะถูกเพิ่มเลย บัญชีที่ใช้ทำคู่มือมี `awaken` อยู่แล้ว (อัปโหลดไว้ 23 ส.ค.) จึงเจอหน้าต่างนี้:

![หน้าต่าง Replace awaken skill? บอกว่าจะบันทึกเป็นเวอร์ชันใหม่ เวอร์ชันเก่ายังอยู่ใน version history ไฟล์เดิม 995 บรรทัด ไฟล์ใหม่ 995 บรรทัด](images/13-claude-replace-dialog.png)

- อัปโหลดซ้ำ = บันทึกเป็น **เวอร์ชันใหม่** เวอร์ชันเก่าเก็บไว้ใน version history ของสกิล ไม่มีอะไรหาย
- รอบนี้เรากด **Cancel** เพราะไฟล์เหมือนของเดิมทุกบรรทัด และไม่อยากเปลี่ยนบัญชีของเจ้าของ

**6.7 ตรวจว่าลงแล้ว** แท็บ **Yours** กดชื่อสกิล จะเห็นคำอธิบาย สวิตช์เปิดปิด และปุ่ม **Try in chat**

![หน้าสกิล awaken by you v1 มีปุ่ม Try in chat สวิตช์เปิดอยู่ และ Connectors & tools: Only adds instructions for Claude](images/14-claude-awaken-skill.png)

เปิดแชทใหม่แล้วพิมพ์ "awaken --fast ตั้งชื่อ Oracle ให้ฉัน" Claude จะโหลดสกิลเมื่อคำขอตรงกับคำอธิบาย

> ⚠️ สกิลบนเว็บทำงานในพื้นที่ชั่วคราว ไฟล์ `ψ/` ที่ `/awaken` สร้างจะหายเมื่อเปิดแชทใหม่ ช่วง `/rrr` → ปิด → เปิดใหม่ → `/recap` จึงต้องดูบนจอ หรือใช้ทาง A/B

## 7. แล้ว ChatGPT บนเว็บล่ะ

เอกสารของ OpenAI (learn.chatgpt.com, หน้า Build skills) เขียนไว้ว่า:

![หน้า Build skills บรรทัดที่ขีดกรอบ: Standalone skills are available in the ChatGPT desktop app, Codex CLI, and IDE extension. Skills bundled in plugins are also available in Chat and Work across ChatGPT on the web](images/07-chatgpt-skills-where.png)

- สกิลเดี่ยว (standalone) ใช้ได้ใน **ChatGPT desktop**, **Codex CLI** และ IDE extension
- บน **chatgpt.com** สกิลมาได้ทางเดียวคืออยู่ใน plugin
- ในแอป ChatGPT desktop เปิดเมนู **Skills** ในแถบซ้ายเพื่อดูสกิล ใน ChatGPT พิมพ์ `@` เพื่อเลือกสกิล ใน Codex พิมพ์ `$` หรือ `/skills`

สรุปสำหรับ workshop: ใครมีแค่บัญชี ChatGPT ให้ไปทาง B (Codex CLI) ไม่ต้องลงสกิลบน chatgpt.com

## 8. กับดักที่เจอจริง

| อาการ | สาเหตุ | แก้ |
|---|---|---|
| `Not logged in · Please run /login` | ลง Claude Code แล้วแต่ยังไม่ล็อกอิน | รัน `claude` แล้วพิมพ์ `/login` |
| `claude: command not found` หลังติดตั้ง | terminal เดิมยังไม่รู้จัก `$HOME/.local/bin` | เปิด terminal ใหม่ |
| อัปโหลดสกิลแล้วขึ้น Replace | มีสกิลชื่อเดียวกันอยู่แล้ว | กด Upload and replace ได้ เวอร์ชันเก่าอยู่ใน history |
| สกิลบน claude.ai ไม่ทำงาน | ปิด Run code in the cloud อยู่ | Settings > Capabilities เปิดสวิตช์ |
| Codex พิมพ์ `/awaken` ไม่ขึ้น | ลงสกิลโดยไม่มี `--with-commands` | รัน installer ซ้ำพร้อม `--with-commands` |
| ความจำหายบนเว็บ | sandbox ของแชทรีเซ็ตทุกแชท | ใช้ทาง A หรือ B |

## 9. ที่มา

- https://claude.com/download (อ่านหน้าจริง 30 ต.ค. 2026)
- https://code.claude.com/docs/en/quickstart
- https://chatgpt.com/download
- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/skills-and-plugins และ https://learn.chatgpt.com/docs/build-skills
- https://github.com/Soul-Brews-Studio/arra-oracle-skills-cli (คำสั่งติดตั้งสกิล)
- การตัดสินใจข้อ 4–5 ใน issue #1 ของรีโปนี้ (บัญชีที่ต้องมี และทางสำรองบนเว็บ)

— AIExpo Oracle (Oracle AI)
