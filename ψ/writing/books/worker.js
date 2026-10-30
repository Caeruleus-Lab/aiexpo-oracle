// aiexpo-lessons: the static lessons plus a read-only MCP endpoint at /mcp.
//
// Remote MCP over Streamable HTTP, stateless, no auth (every lesson is already public).
// Tools: search + fetch (the exact names and shapes ChatGPT connectors and deep research require), and list_lessons.
//
// Search runs over chunks.json (build_chunks.py): one chunk per section of each lesson, Thai and English separately,
// each with tags and a vector prebuilt with Workers AI @cf/baai/bge-m3. The query is embedded here with the SAME model,
// then ranked by cosine plus a keyword score (Thai split into words with Intl.Segmenter). If Workers AI fails,
// search falls back to keywords alone and says so in the result.

const SITE = "https://aiexpo.buildwithoracle.com";
const SERVER = { name: "aiexpo-lessons", title: "AIExpo Oracle lessons", version: "2026.10.30-2" };
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const LANG_FILE = { en: "README.en.md", th: "README.md" };
const LANG_PAGE = { en: "en", th: "th" };
const TOPICS = ["install", "account", "skill", "browser", "memory", "web", "verify", "troubleshooting"];
const W_VEC = 0.65; // share of the vector score in the hybrid rank; the rest is keywords

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
    name: "list_lessons",
    title: "List the lessons",
    description: "List every lesson in workshop order, with page URLs, language editions, and each section's id, title and topic tags.",
    inputSchema: { type: "object", properties: {} },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type, accept, authorization, mcp-protocol-version, mcp-session-id",
  "access-control-expose-headers": "mcp-protocol-version",
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/mcp" || url.pathname === "/mcp/") return mcp(request, env);
    return env.ASSETS.fetch(request);
  },
};

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
          capabilities: { tools: { listChanged: false } },
          serverInfo: SERVER,
          instructions:
            "Read-only access to the AIExpo Oracle workshop lessons (AI Expo Thailand, 6 Nov 2026). " +
            "Use search (optionally filtered by lang, lesson or topic), then fetch an id for the full text. " +
            "Lessons exist in Thai (th, the original) and English (en).",
        });
      }
      case "ping":
        return ok(id, {});
      case "tools/list":
        return ok(id, { tools: TOOLS });
      case "tools/call":
        return ok(id, await callTool(params.name, params.arguments || {}, env));
      case "resources/list":
        return ok(id, { resources: [] });
      case "prompts/list":
        return ok(id, { prompts: [] });
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
    return result(doc);
  }
  return { content: [{ type: "text", text: `Unknown tool: ${name}` }], isError: true };
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
      id: c.id, title: c.label, text: c.text, url: c.url,
      metadata: { ...c.tags, title: c.title, source: `${SITE}/${lessonDir(lessons, c.lesson)}/${LANG_FILE[c.lang]}`, signed_by: SIGNER },
    };
  }
  const [key, lang] = id.split("/");
  const l = lessons.find((x) => x.key === key);
  if (!l || !LANG_FILE[lang] || id.split("/").length !== 2) return null;
  const text = await (await env.ASSETS.fetch(`${SITE}/${l.dir}/${LANG_FILE[lang]}`)).text();
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
