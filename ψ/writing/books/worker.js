// aiexpo-lessons: the static lessons plus a read-only MCP endpoint at /mcp.
// Plus a tiny read-only GET API for any AI that can open a URL but cannot add MCP (free ChatGPT, Gemini, a phone):
//   /api/search?q=...&lang=th|en&lesson=...&k=5   top sections, the same hybrid search as the MCP search tool
//   /api/fetch?id=<section or lesson id>           the text, its source and its image URLs
//
// Remote MCP over Streamable HTTP, stateless, no auth (every lesson is already public).
// Tools: search + fetch (the exact names and shapes ChatGPT connectors and deep research require), and list_lessons.
//
// Search runs over chunks.json (build_chunks.py): one chunk per section of each lesson, Thai and English separately,
// each with tags and a vector prebuilt with Workers AI @cf/baai/bge-m3. The query is embedded here with the SAME model,
// then ranked by cosine plus a keyword score (Thai split into words with Intl.Segmenter). If Workers AI fails,
// search falls back to keywords alone and says so in the result.
//
// Screenshots: fetch and get_image return MCP image content blocks ({type:"image", data, mimeType}) so the model sees them,
// at most 3 per call, from images.json (prebuilt by build_chunks.py: max 1280 px, JPEG 80). The text also carries each
// image as a markdown link to its https URL, for chat UIs that render markdown.

const SITE = "https://aiexpo.buildwithoracle.com";
const SERVER = { name: "aiexpo-lessons", title: "AIExpo Oracle lessons", version: "2026.11.02-1" };
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const LANG_FILE = { en: "README.en.md", th: "README.md" };
const LANG_PAGE = { en: "en", th: "th" };
const TOPICS = ["install", "account", "skill", "browser", "memory", "web", "verify", "troubleshooting"];
const W_VEC = 0.65;
const MAX_IMAGES = 3; // per tool call, so the result stays well under client limits // share of the vector score in the hybrid rank; the rest is keywords

const filterProps = {
  lang: { type: "string", enum: ["th", "en"], description: "Only this language edition" },
  lesson: { type: "string", description: "Only this lesson id (see list_lessons), e.g. claude-chatgpt or ego-lite" },
  topic: { type: "string", enum: TOPICS, description: "Only chunks tagged with this topic" },
};

const TOOLS = [
  {
    name: "search",
    title: "Search the lessons",
    description:
      "Search the AIExpo Oracle workshop lessons (Thai and English): installing Claude Code, the Codex CLI, claude.ai skills, " +
      "ego(lite) and the ARRA Oracle skills. Hybrid search: meaning (bge-m3 vectors) plus keywords. Returns sections; pass an id to fetch.",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string", description: "What to look for, in Thai or English" }, ...filterProps },
      required: ["query"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "fetch",
    title: "Read a lesson section",
    description:
      "Read the full text of a search result. id '<lesson>/<lang>/<section>' is one section, '<lesson>/<lang>' the whole lesson, " +
      "for example 'claude-chatgpt/en/6' or 'ego-lite/th'. metadata carries the section's tags.",
    inputSchema: { type: "object", properties: { id: { type: "string", description: "An id from search or list_lessons" } }, required: ["id"] },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_image",
    title: "Show a screenshot",
    description:
      "Return screenshots as images the model can see. id is an image id from fetch (e.g. 'claude-chatgpt/08-claude-capabilities.png') " +
      "or a section id (e.g. 'claude-chatgpt/en/6'), which returns that section's screenshots, 3 at a time from 'start'.",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" }, start: { type: "integer", minimum: 0, description: "First image of a section to return (default 0)" } },
      required: ["id"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "list_lessons",
    title: "List the lessons",
    description: "List every lesson in workshop order, with page URLs, language editions, and each section's id, title and topic tags.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "list_skills",
    title: "List the Oracle skills",
    description: "List the ARRA Oracle skills this server can hand out (awaken, rrr, forward, recap, workshop, awaken-app): what each does and how to run it in a chat.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_skill",
    title: "Get an Oracle skill",
    description:
      "Return the instructions of an ARRA Oracle skill so you can run it in this chat: 'awaken' (give birth to an Oracle), 'rrr' (session report with real timestamps), " +
      "'forward' (hand this chat over to the next one), 'recap' (CLAUDE CODE ONLY: it reads ψ files, git and session logs on disk, so it does not run in a chat; in a chat, tell the person so and continue from the /forward handoff instead), 'workshop' (the whole mini workshop), 'awaken-app' (build an interactive awaken app). " +
      "Default source 'full' returns the WHOLE skill, not a summary: Part 1 = how to run it in a chat with no terminal, Part 2 = every file of the real skill " +
      "(SKILL.md plus its HOSTS/TEMPLATE/reference docs and scripts, from Soul-Brews-Studio/arra-oracle-skills-cli). It is long (30-65 KB): read all of it before you start, " +
      "then follow Part 1 with the person and use Part 2 for every detail (steps, templates, rules, why). " +
      "source 'chat' = Part 1 only (short); source 'github' = the live SKILL.md alone. " +
      "Every answer ends with ZIP download links so the person can install the skill (claude.ai Skills upload, or ~/.claude/skills).",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", enum: ["awaken", "rrr", "forward", "recap", "workshop", "awaken-app"] },
        source: { type: "string", enum: ["full", "chat", "github"], description: "full (default): the whole skill; chat: the short chat runbook; github: live SKILL.md only" },
      },
      required: ["name"],
    },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  {
    name: "list_media",
    title: "List the voice and video",
    description: "List every video and narrated (voiced) lesson: Phukhao's presentation and film, the mother clip, the wrong-voice example, and the 8 narrated lessons, with length and links.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "get_media",
    title: "Watch or listen to a media item",
    description:
      "Return one video or narrated lesson: its link, a timed transcript ([mm:ss] lines), and deep links that start playback at a time. " +
      "id from list_media (e.g. 'phukhao-film', 'oracle-family', 'narrated/mcp-connect'). Optional 'at' (seconds) returns only the minute around that time; " +
      "optional 'q' finds the lines that mention a word. Use it to answer what is said when, quote it, and give the person a link to that exact moment.",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" }, at: { type: "number", description: "seconds" }, q: { type: "string", description: "word or phrase to find" } },
      required: ["id"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

// Oracle skills served over MCP (Nat, 4 Nov 2026: "we can put our skill in the mcp"): as tools (every client) and as prompts (claude.ai + menu)
const SKILLS = {
  awaken: "ปลุก Oracle: ถาม 3 ข้อ แล้วสร้าง CLAUDE.md + ψ/memory/resonance",
  rrr: "รายงานจบงาน: Timeline เวลาจริง + บทเรียน",
  forward: "ส่งต่องาน: เขียน handoff ให้แชทถัดไป (ทำอะไรไป ค้างอะไร เริ่มตรงไหน)",
  recap: "เริ่มงาน (Claude Code เท่านั้น ในแชทใช้ไม่ได้): อ่าน handoff และรายงานรอบก่อน บอกว่าค้างอะไร",
  workshop: "workshop สั้นในแชทเดียว: awaken → งานจริง → คุย → /rrr พร้อม time log",
  "awaken-app": "สร้างแอปปลุก Oracle แบบกดได้ (artifact / canvas)",
};
const GITHUB_SKILL = { awaken: "awaken", rrr: "rrr", forward: "forward", recap: "recap" };
// the skill folders as ZIPs (lesson 01, section 6): upload in claude.ai (Customize > Skills > Add) or unzip into ~/.claude/skills
const ZIP = (s) => `${SITE}/2026-10-30_claude-chatgpt-install-guide/skills/${s}.zip`;
const CARRIES = { awaken: ["awaken"], rrr: ["rrr"], forward: ["forward"], recap: ["recap"], workshop: ["awaken", "rrr"], "awaken-app": ["awaken"] };
function downloads(name) {
  return "\n\n## Download this skill (tell the person)\n\n" + CARRIES[name].map((s) => `- \`${s}\`: ${ZIP(s)}`).join("\n") +
    "\n\nclaude.ai: Settings > Capabilities > turn on code execution, then Customize > Skills > Add > upload the ZIP; after that, /" + CARRIES[name][0] + " works in any chat. " +
    "Claude Code / Codex: unzip into ~/.claude/skills/ (or ~/.codex/skills/). Or install all of them: bunx --bun github:Soul-Brews-Studio/arra-oracle-skills-cli#alpha install -g -y . " +
    "Guide: " + SITE + "/2026-10-30_claude-chatgpt-install-guide/en.html";
}
async function skillText(name, source, env) {
  if (!SKILLS[name]) return null;
  if (source === "github") {
    const g = GITHUB_SKILL[name];
    if (!g) return null;
    const r = await fetch(`https://raw.githubusercontent.com/Soul-Brews-Studio/arra-oracle-skills-cli/alpha/skills/${g}/SKILL.md`);
    return r.ok ? r.text() : null;
  }
  // full (default): oracle/full/<name>.md, baked by build_skills_full.py = chat runbook + every file of the real skill folder
  const r = await env.ASSETS.fetch(`${SITE}/oracle/${source === "chat" ? "" : "full/"}${name}.md`);
  return r.ok ? r.text() : null;
}

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type, accept, authorization, mcp-protocol-version, mcp-session-id",
  "access-control-expose-headers": "mcp-protocol-version",
};

// Static assets answer a Range request with the whole file (200), and Safari / iOS will not play an mp4 that way.
// The lesson videos (each under 25 MiB) are sliced here and answered 206 with Content-Range.
async function video(request, env) {
  const range = /^bytes=(\d*)-(\d*)$/.exec(request.headers.get("Range") || "");
  // a HEAD with a Range still needs the real size, so only a plain HEAD is passed through as HEAD
  const res = await env.ASSETS.fetch(request.url, { method: request.method === "HEAD" && !range ? "HEAD" : "GET" });
  if (!res.ok) return res;
  const headers = new Headers(res.headers);
  headers.set("Accept-Ranges", "bytes");
  headers.set("Content-Type", "video/mp4");
  if (request.method === "HEAD" && !range) return new Response(null, { status: 200, headers });
  const body = await res.arrayBuffer();
  const size = body.byteLength;
  if (!range) {
    headers.set("Content-Length", String(size));
    return new Response(request.method === "HEAD" ? null : body, { status: 200, headers });
  }
  let start = range[1] === "" ? Math.max(0, size - Number(range[2])) : Number(range[1]);
  let end = range[1] !== "" && range[2] !== "" ? Math.min(Number(range[2]), size - 1) : size - 1;
  if (start >= size || start > end) {
    headers.set("Content-Range", `bytes */${size}`);
    return new Response(null, { status: 416, headers });
  }
  headers.set("Content-Range", `bytes ${start}-${end}/${size}`);
  headers.set("Content-Length", String(end - start + 1));
  return new Response(request.method === "HEAD" ? null : body.slice(start, end + 1), { status: 206, headers });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/mcp" || url.pathname === "/mcp/") return mcp(request, env);
    if (url.pathname === "/api" || url.pathname.startsWith("/api/")) return api(request, url, env);
    if (url.pathname.endsWith(".mp4")) return video(request, env);
    return env.ASSETS.fetch(request);
  },
};

// GET only, CORS *, JSON. Same data and ranking as the MCP tools, without JSON-RPC.
async function api(request, url, env) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (request.method !== "GET" && request.method !== "HEAD") return json({ error: "GET only" }, 405);
  const p = url.searchParams;
  const { lessons, chunks, model } = await load(env);
  if (url.pathname === "/api/search") {
    const q = String(p.get("q") || "").trim();
    if (!q) return json({ error: "add ?q=your question", example: `${SITE}/api/search?q=${encodeURIComponent("ติดตั้ง Claude Code")}&lang=th&k=5` }, 400);
    const k = Math.min(10, Math.max(1, Number(p.get("k")) || 5));
    const lang = p.get("lang"), lesson = p.get("lesson");
    const pool = chunks.filter((c) => (!lang || c.lang === lang) && (!lesson || c.lesson === lesson));
    const { ranked, mode } = await rank(pool, q, env, model);
    return json({
      query: q, mode,
      results: ranked.slice(0, k).map(({ c, score }) => ({
        id: c.id, title: c.label, url: c.url, score: +score.toFixed(3),
        snippet: c.text.replace(/\s+/g, " ").slice(0, 280),
        fetch: `${SITE}/api/fetch?id=${encodeURIComponent(c.id)}`,
      })),
    });
  }
  if (url.pathname === "/api/fetch") {
    const id = String(p.get("id") || "");
    const doc = await find(lessons, chunks, id, env);
    if (!doc) return json({ error: `No lesson or section with id '${id}'. Use /api/search or ${SITE}/lessons.json for valid ids.` }, 404);
    const c = chunks.find((x) => x.id === doc.id);
    doc.images = (c ? c.images : []).map((r) => ({ id: r.key, alt: r.alt, url: imageUrl(lessons, r.key) }));
    return json(doc);
  }
  return json({
    api: "AIExpo Oracle lessons, read-only GET",
    endpoints: {
      search: `${SITE}/api/search?q=<question>&lang=th|en&lesson=<id>&k=5`,
      fetch: `${SITE}/api/fetch?id=<id from search, e.g. claude-chatgpt/th/3, or a whole lesson: claude-chatgpt/th>`,
    },
    lessons: lessons.map((l) => ({ id: l.key, th: l.th, en: l.en, page: `${SITE}/${l.dir}/` })),
    mcp: `${SITE}/mcp`,
  });
}

async function mcp(request, env) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
  if (request.method === "GET") {
    // No server-initiated stream in a stateless server; a short note helps a human who opens the URL.
    if ((request.headers.get("accept") || "").includes("text/event-stream")) return new Response(null, { status: 405, headers: { ...CORS, allow: "POST" } });
    return json({ server: SERVER, transport: "streamable-http (POST JSON-RPC here)", tools: TOOLS.map((t) => t.name), lessons: `${SITE}/` });
  }
  if (request.method !== "POST") return new Response("POST only", { status: 405, headers: { ...CORS, allow: "POST" } });

  let body;
  try {
    body = await request.json();
  } catch {
    return json(rpcError(null, -32700, "Parse error"), 400);
  }
  const batch = Array.isArray(body);
  const out = [];
  for (const msg of batch ? body : [body]) {
    const res = await handle(msg, env);
    if (res) out.push(res);
  }
  if (!out.length) return new Response(null, { status: 202, headers: CORS }); // notifications only
  return json(batch ? out : out[0]);
}

async function handle(msg, env) {
  if (!msg || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") return rpcError(msg?.id ?? null, -32600, "Invalid Request");
  const { id, method, params = {} } = msg;
  if (id === undefined) return null; // a notification (notifications/initialized, cancelled, ...)
  try {
    switch (method) {
      case "initialize": {
        const asked = params.protocolVersion;
        return ok(id, {
          protocolVersion: PROTOCOLS.includes(asked) ? asked : PROTOCOLS[0],
          capabilities: { tools: { listChanged: false }, prompts: { listChanged: false }, resources: { listChanged: false } },
          serverInfo: SERVER,
          instructions:
            "Read-only access to the AIExpo Oracle workshop lessons (AI Expo Thailand, 6 Nov 2026). " +
            "Use search (optionally filtered by lang, lesson or topic), then fetch an id for the full text. " +
            "Lessons exist in Thai (th, the original) and English (en). " +
            "It also hands out ARRA Oracle skills: list_skills, then get_skill (awaken, rrr, forward, workshop, awaken-app; recap is Claude Code only). get_skill returns the WHOLE skill (every file of the real skill folder plus how to run it in chat): read all of it, then follow it with the person. " +
            "Voice and video: list_media, then get_media for a timed transcript and links that start at a given second.",
        });
      }
      case "ping":
        return ok(id, {});
      case "tools/list":
        return ok(id, { tools: TOOLS });
      case "tools/call":
        return ok(id, await callTool(params.name, params.arguments || {}, env));
      // the skills as markdown files (Nat, 4 Nov: "can make skill return md?")
      case "resources/list":
        return ok(id, { resources: Object.entries(SKILLS).map(([name, description]) => ({
          uri: `${SITE}/oracle/full/${name}.md`, name: `${name}.md`, title: `/${name} (full skill)`, description, mimeType: "text/markdown" })) });
      case "resources/read": {
        const m = /\/oracle\/full\/([a-z-]+)\.md$/.exec(params.uri || "");
        const text = m && (await skillText(m[1], "full", env));
        if (!text) return rpcError(id, -32602, `Unknown resource: ${params.uri}`);
        return ok(id, { contents: [{ uri: params.uri, mimeType: "text/markdown", text: text + downloads(m[1]) }] });
      }
      case "resources/templates/list":
        return ok(id, { resourceTemplates: [] });
      case "prompts/list":
        return ok(id, { prompts: Object.entries(SKILLS).filter(([n]) => n !== "recap").map(([name, description]) => ({ name, title: `/${name}`, description })) });
      case "prompts/get": {
        const text = await skillText(params.name, "full", env);
        if (!text) return rpcError(id, -32602, `Unknown prompt: ${params.name}`);
        return ok(id, { description: SKILLS[params.name], messages: [{ role: "user", content: { type: "text", text: `ทำตามนี้กับฉันในแชทนี้ / Follow this with me in this chat:\n\n${text}` } }] });
      }
      default:
        return rpcError(id, -32601, `Method not found: ${method}`);
    }
  } catch (e) {
    return rpcError(id, -32603, String(e?.message || e));
  }
}

let cache = null; // per isolate: { lessons, chunks, model }

async function load(env) {
  if (cache) return cache;
  const [lessons, index] = await Promise.all([
    env.ASSETS.fetch(`${SITE}/lessons.json`).then((r) => r.json()),
    env.ASSETS.fetch(`${SITE}/chunks.json`).then((r) => r.json()),
  ]);
  for (const c of index.chunks) {
    c.norm = Math.hypot(...c.vec);
    c.words = new Set(words(`${c.title}\n${c.text}`));
    c.titleWords = new Set(words(c.title));
  }
  cache = { lessons, chunks: index.chunks, model: index.model };
  return cache;
}

async function callTool(name, args, env) {
  if (name === "list_media" || name === "get_media") {
    const media = (await (await env.ASSETS.fetch(`${SITE}/media.json`)).json()).items;
    const mmss = (t) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}`;
    if (name === "list_media") {
      return result({ media: media.map((m) => ({ id: m.id, kind: m.kind, title: m.title, length: mmss(m.duration), url: m.url })) });
    }
    const m = media.find((x) => x.id === args.id);
    if (!m) return { content: [{ type: "text", text: `No media '${args.id}'. Use list_media.` }], isError: true };
    let cues = m.cues;
    if (typeof args.at === "number") cues = cues.filter((c) => c.end >= args.at - 30 && c.start <= args.at + 30);
    if (args.q) cues = cues.filter((c) => c.text.toLowerCase().includes(String(args.q).toLowerCase()));
    const link = (t) => (m.kind === "video" ? `${m.url}#t=${Math.floor(t)}` : (m.slides || []).reduce((u, s) => (s.start <= t ? s.audio : u), m.url));
    const lines = cues.map((c) => `[${mmss(c.start)}] ${c.text}  (${link(c.start)})`);
    const head = `${m.title}\n${m.kind} · ${mmss(m.duration)} · ${m.url}\ntranscript: ${m.transcript}` + (m.slides ? `\nslides: ${m.slides.map((s) => `${s.n}. ${s.title} [${mmss(s.start)}]`).join(" · ")}` : "");
    return { content: [{ type: "text", text: `${head}\n\n${lines.join("\n") || "(no lines match)"}` }] };
  }
  if (name === "list_skills") {
    return result({ skills: Object.entries(SKILLS).map(([name, what]) => ({ name, what, full: `${SITE}/oracle/full/${name}.md`, download: CARRIES[name].map(ZIP), chat: `${SITE}/oracle/${name}.md`, github: GITHUB_SKILL[name] ? `https://github.com/Soul-Brews-Studio/arra-oracle-skills-cli/tree/alpha/skills/${GITHUB_SKILL[name]}` : null })) });
  }
  if (name === "get_skill") {
    const text = await skillText(args.name, args.source || "full", env);
    if (!text) return { content: [{ type: "text", text: `No skill '${args.name}' (source ${args.source || "full"}). Use list_skills.` }], isError: true };
    // Nat, 4 Nov: "can make skill return md?" -> the skill is a text/markdown resource (a real .md file), not loose text
    const src = args.source || "full";
    const uri = src === "github" ? `https://github.com/Soul-Brews-Studio/arra-oracle-skills-cli/blob/alpha/skills/${GITHUB_SKILL[args.name]}/SKILL.md`
      : `${SITE}/oracle/${src === "chat" ? "" : "full/"}${args.name}.md`;
    return { content: [
      { type: "text", text: `Skill /${args.name} (${src}) follows as the markdown file ${uri} . Read all of it, then run it with the person.` },
      { type: "resource", resource: { uri, mimeType: "text/markdown", text: text + downloads(args.name) } },
    ] };
  }
  const { lessons, chunks, model } = await load(env);
  if (name === "list_lessons") {
    return result({
      lessons: lessons.map((l, i) => ({
        order: i + 1,
        id: l.key,
        title: { th: l.th, en: l.en },
        summary: { th: l.th_sub, en: l.en_sub },
        urls: { th: `${SITE}/${l.dir}/th`, en: `${SITE}/${l.dir}/en`, base64: `${SITE}/${l.dir}/`, llms: `${SITE}/${l.dir}/llms.txt` },
        editions: Object.keys(LANG_FILE).map((lang) => ({ lang, id: `${l.key}/${lang}`, markdown: `${SITE}/${l.dir}/${LANG_FILE[lang]}` })),
        sections: chunks.filter((c) => c.lesson === l.key && c.lang === "en").map((c) => ({ id: c.id, title: c.title, topic: c.tags.topic })),
      })),
    });
  }
  if (name === "search") {
    const q = String(args.query || "").trim();
    if (!q) return result({ results: [] });
    const pool = chunks.filter((c) => (!args.lang || c.lang === args.lang) && (!args.lesson || c.lesson === args.lesson) && (!args.topic || c.tags.topic.includes(args.topic)));
    const { ranked, mode } = await rank(pool, q, env, model);
    return result({
      results: ranked.slice(0, 10).map(({ c }) => ({ id: c.id, title: c.label, url: c.url })),
      // extra fields after results are ignored by clients that only read results
      mode,
      matches: ranked.slice(0, 10).map(({ c, score, vec, kw }) => ({ id: c.id, score: +score.toFixed(3), vector: +vec.toFixed(3), keyword: +kw.toFixed(3), tags: c.tags })),
    });
  }
  if (name === "fetch") {
    const doc = await find(lessons, chunks, String(args.id || ""), env);
    if (!doc) return { content: [{ type: "text", text: `No lesson or section with id '${args.id}'. Use search or list_lessons for valid ids.` }], isError: true };
    const c = chunks.find((x) => x.id === doc.id);
    const refs = c ? c.images : [];
    doc.images = refs.map((r) => ({ id: r.key, alt: r.alt, url: imageUrl(lessons, r.key) }));
    if (refs.length > MAX_IMAGES) doc.images_note = `${refs.length} screenshots; the first ${MAX_IMAGES} are attached. Call get_image with id '${doc.id}' and start ${MAX_IMAGES} for more.`;
    const res = result(doc);
    res.content.push(...(await imageBlocks(env, refs.slice(0, MAX_IMAGES).map((r) => r.key))));
    return res;
  }
  if (name === "get_image") {
    const id = String(args.id || "");
    const start = Math.max(0, Number(args.start) || 0);
    const c = chunks.find((x) => x.id === id);
    const keys = c ? c.images.slice(start, start + MAX_IMAGES).map((r) => r.key) : [id];
    const blocks = await imageBlocks(env, keys);
    if (!blocks.length) return { content: [{ type: "text", text: `No screenshot for '${id}'. Use an image id from fetch, or a section id that has screenshots.` }], isError: true };
    const imgs = await loadImages(env);
    const info = keys.filter((k) => imgs[k]).map((k) => {
      const alt = (c ? c.images.find((r) => r.key === k)?.alt : chunks.flatMap((x) => x.images).find((r) => r.key === k)?.alt) || k;
      return { id: k, alt, url: imgs[k].url, width: imgs[k].width, height: imgs[k].height };
    });
    const more = c && c.images.length > start + MAX_IMAGES ? { next_start: start + MAX_IMAGES, total: c.images.length } : {};
    return {
      content: [{ type: "text", text: info.map((i) => `![${i.alt}](${i.url})`).join("\n") }, ...blocks],
      structuredContent: { images: info, ...more },
    };
  }
  return { content: [{ type: "text", text: `Unknown tool: ${name}` }], isError: true };
}

let imageCache = null;
async function loadImages(env) {
  if (!imageCache) imageCache = await env.ASSETS.fetch(`${SITE}/images.json`).then((r) => r.json());
  return imageCache;
}
async function imageBlocks(env, keys) {
  if (!keys.length) return [];
  const imgs = await loadImages(env);
  return keys.filter((k) => imgs[k]).map((k) => ({ type: "image", data: imgs[k].data, mimeType: imgs[k].mimeType }));
}
function imageUrl(lessons, key) {
  const [lesson, file] = key.split("/");
  return `${SITE}/${lessonDir(lessons, lesson)}/images/${file}`;
}
// Relative image and file links in lesson markdown become absolute https URLs, so a chat UI can render them.
function absolute(text, dir) {
  return text.replace(/\]\((?!https?:|#|mailto:)([^)\s]+)\)/g, (_, p) => `](${SITE}/${dir}/${p.replace(/^\.\//, "")})`);
}

async function rank(pool, q, env, model) {
  const qWords = [...new Set(words(q))];
  let qv = null;
  let mode = "hybrid";
  try {
    const out = await env.AI.run(model, { text: [q] });
    qv = out.data[0];
  } catch {
    mode = "keyword (vector search unavailable)";
  }
  const qn = qv ? Math.hypot(...qv) : 1;
  const rows = pool.map((c) => {
    const vec = qv ? dot(qv, c.vec) / (qn * c.norm) : 0;
    let kw = 0;
    for (const w of qWords) kw += c.titleWords.has(w) ? 2 : c.words.has(w) ? 1 : 0;
    return { c, vec, kw: qWords.length ? kw / (2 * qWords.length) : 0 };
  });
  for (const r of rows) r.score = qv ? W_VEC * r.vec + (1 - W_VEC) * r.kw : r.kw;
  return { ranked: rows.filter((r) => r.score > 0).sort((a, b) => b.score - a.score), mode };
}

// Words for keyword matching: Intl.Segmenter splits Thai (no spaces between words) and English alike.
const seg = new Intl.Segmenter("th", { granularity: "word" });
function words(s) {
  const out = [];
  for (const { segment, isWordLike } of seg.segment(s.toLowerCase())) if (isWordLike && (segment.length > 1 || /[฀-๿]/.test(segment))) out.push(segment);
  return out;
}

function dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

async function find(lessons, chunks, id, env) {
  const c = chunks.find((x) => x.id === id);
  if (c) {
    return {
      id: c.id, title: c.label, text: absolute(c.text, lessonDir(lessons, c.lesson)), url: c.url,
      metadata: { ...c.tags, title: c.title, source: `${SITE}/${lessonDir(lessons, c.lesson)}/${LANG_FILE[c.lang]}`, signed_by: SIGNER },
    };
  }
  const [key, lang] = id.split("/");
  const l = lessons.find((x) => x.key === key);
  if (!l || !LANG_FILE[lang] || id.split("/").length !== 2) return null;
  const text = absolute(await (await env.ASSETS.fetch(`${SITE}/${l.dir}/${LANG_FILE[lang]}`)).text(), l.dir);
  return {
    id, title: lang === "th" ? l.th : l.en, text, url: `${SITE}/${l.dir}/${LANG_PAGE[lang]}`,
    metadata: { lesson: l.key, lang, sections: chunks.filter((x) => x.lesson === l.key && x.lang === lang).length, source: `${SITE}/${l.dir}/${LANG_FILE[lang]}`, signed_by: SIGNER },
  };
}

const SIGNER = "0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78";
const lessonDir = (lessons, key) => lessons.find((l) => l.key === key).dir;

// One JSON text block (what ChatGPT's search/fetch contract expects) plus the same object as structuredContent.
function result(obj) {
  return { content: [{ type: "text", text: JSON.stringify(obj) }], structuredContent: obj };
}
function ok(id, result) {
  return { jsonrpc: "2.0", id, result };
}
function rpcError(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { ...CORS, "content-type": "application/json; charset=utf-8" } });
}
