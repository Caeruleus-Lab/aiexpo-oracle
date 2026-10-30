// aiexpo-lessons: the static lessons plus a read-only MCP endpoint at /mcp.
//
// Remote MCP over Streamable HTTP, stateless, no auth (every lesson is already public).
// Tools: search + fetch (the exact names and shapes ChatGPT connectors and deep research require),
// and list_lessons. Text comes from each lesson's README.md (Thai) and README.en.md (English),
// read from the same static assets the website serves; base64, vendor/ and tools/ are never read.

const SITE = "https://aiexpo.buildwithoracle.com";
const SERVER = { name: "aiexpo-lessons", title: "AIExpo Oracle lessons", version: "2026.10.30" };
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const LANGS = { en: { file: "README.en.md", page: "en" }, th: { file: "README.md", page: "th" } };

const TOOLS = [
  {
    name: "search",
    title: "Search the lessons",
    description:
      "Search the AIExpo Oracle workshop lessons (Thai and English): installing Claude Code, the Codex CLI, " +
      "claude.ai skills, ego(lite) and the ARRA Oracle skills. Returns matching sections; pass an id to fetch for the full text.",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string", description: "Words to look for, in Thai or English" } },
      required: ["query"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "fetch",
    title: "Read a lesson section",
    description:
      "Read the full text of a search result. id is '<lesson>/<lang>/<section>' (a section) or '<lesson>/<lang>' (the whole lesson), " +
      "for example 'claude-chatgpt/en/6' or 'ego-lite/th'.",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string", description: "An id from search or list_lessons" } },
      required: ["id"],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: "list_lessons",
    title: "List the lessons",
    description: "List every lesson in workshop order, with its page URLs, language editions and section titles.",
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
            "Use search, then fetch an id for the full text. Lessons exist in Thai (th, the original) and English (en).",
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

async function callTool(name, args, env) {
  const lessons = await loadLessons(env);
  if (name === "list_lessons") {
    const list = lessons.map((l, i) => ({
      order: i + 1,
      id: l.key,
      title: { th: l.th, en: l.en },
      summary: { th: l.th_sub, en: l.en_sub },
      urls: { th: `${SITE}/${l.dir}/th`, en: `${SITE}/${l.dir}/en`, base64: `${SITE}/${l.dir}/`, llms: `${SITE}/${l.dir}/llms.txt` },
      editions: Object.keys(LANGS).map((lang) => ({ lang, id: `${l.key}/${lang}`, markdown: `${SITE}/${l.dir}/${LANGS[lang].file}` })),
      sections: l.sections.en.map((s) => ({ id: s.id, title: s.title })),
    }));
    return result({ lessons: list });
  }
  if (name === "search") {
    const q = String(args.query || "").trim();
    if (!q) return result({ results: [] });
    return result({ results: search(lessons, q).slice(0, 10).map(({ s }) => ({ id: s.id, title: s.label, url: s.url })) });
  }
  if (name === "fetch") {
    const doc = find(lessons, String(args.id || ""));
    if (!doc) return { content: [{ type: "text", text: `No lesson or section with id '${args.id}'. Use search or list_lessons for valid ids.` }], isError: true };
    return result(doc);
  }
  return { content: [{ type: "text", text: `Unknown tool: ${name}` }], isError: true };
}

// One JSON text block (what ChatGPT's search/fetch contract expects) plus the same object as structuredContent.
function result(obj) {
  return { content: [{ type: "text", text: JSON.stringify(obj) }], structuredContent: obj };
}

async function loadLessons(env) {
  const index = await (await env.ASSETS.fetch(`${SITE}/lessons.json`)).json();
  return Promise.all(
    index.map(async (l) => {
      const sections = {};
      const full = {};
      for (const [lang, { file, page }] of Object.entries(LANGS)) {
        const md = await (await env.ASSETS.fetch(`${SITE}/${l.dir}/${file}`)).text();
        full[lang] = md;
        sections[lang] = split(md).map((s, n) => ({
          id: `${l.key}/${lang}/${n + 1}`,
          lesson: l.key,
          lang,
          title: s.title,
          label: `${lang === "th" ? l.th : l.en} · ${s.title}`,
          url: `${SITE}/${l.dir}/${page}#s${n + 2}`, // the page builder numbers the cover s1, the first ## s2
          text: s.text,
        }));
      }
      return { ...l, sections, full };
    }),
  );
}

// "## " headings after the front matter (the part before the first "\n---\n") become sections.
function split(md) {
  const body = md.includes("\n---\n") ? md.split("\n---\n").slice(1).join("\n---\n") : md;
  return body
    .split(/\n(?=## )/)
    .map((part) => part.trim())
    .filter((part) => part.startsWith("## "))
    .map((part) => ({ title: part.split("\n")[0].replace(/^##\s+/, "").trim(), text: part }));
}

function terms(q) {
  return q
    .toLowerCase()
    .split(/[\s,.;:!?()"'`]+/)
    .filter((t) => t.length > 1 || /[฀-๿]/.test(t));
}

function search(lessons, q) {
  const ts = terms(q);
  const whole = q.toLowerCase();
  const hits = [];
  for (const l of lessons)
    for (const lang of Object.keys(LANGS))
      for (const s of l.sections[lang]) {
        const title = s.title.toLowerCase();
        const text = s.text.toLowerCase();
        let score = text.includes(whole) ? 5 : 0;
        for (const t of ts) {
          if (title.includes(t)) score += 3;
          const n = text.split(t).length - 1;
          if (n) score += 1 + Math.min(n, 5) * 0.2;
        }
        if (score > 0) hits.push({ s, score });
      }
  return hits.sort((a, b) => b.score - a.score);
}

function find(lessons, id) {
  const [key, lang = "en", n] = id.split("/");
  const l = lessons.find((x) => x.key === key);
  if (!l || !LANGS[lang]) return null;
  const meta = { lesson: l.key, lang, signed_by: "0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78", source: `${SITE}/${l.dir}/${LANGS[lang].file}` };
  if (n === undefined)
    return { id: `${l.key}/${lang}`, title: lang === "th" ? l.th : l.en, text: l.full[lang], url: `${SITE}/${l.dir}/${LANGS[lang].page}`, metadata: meta };
  const s = l.sections[lang][Number(n) - 1];
  if (!s) return null;
  return { id: s.id, title: s.label, text: s.text, url: s.url, metadata: { ...meta, section: s.title } };
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
