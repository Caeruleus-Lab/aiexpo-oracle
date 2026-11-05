#!/usr/bin/env node
// aiexpo-lessons MCP over stdio: the same read-only tools as the hosted endpoint
// (https://aiexpo.buildwithoracle.com/mcp), served from the GitHub Pages copy of the lessons.
//
// GitHub Pages serves files only, so it cannot answer MCP's POST requests. This server runs on your machine
// instead and reads the lessons' prebuilt index (lessons.json, chunks.json, images.json) from the Pages site,
// or from a local checkout when AIEXPO_DIR is set. No dependencies; Node 18 or newer.
//
// Search is keyword only here (Thai split with Intl.Segmenter). The hosted endpoint adds meaning search with
// Workers AI bge-m3, which needs Cloudflare; the chunk vectors are in chunks.json if you have your own bge-m3.
//
//   claude mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp
//   AIEXPO_BASE=https://caeruleus-lab.github.io/aiexpo-lessons   (default)
//   AIEXPO_DIR=/path/to/a/clone                                    (read files from disk instead)

import { readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join } from "node:path";

const LIVE = "https://aiexpo.buildwithoracle.com";
const BASE = (process.env.AIEXPO_BASE || "https://caeruleus-lab.github.io/aiexpo-lessons").replace(/\/$/, "");
const CLONE = process.env.AIEXPO_DIR || "";
// a clone of aiexpo-lessons keeps the site in docs/ since 5 Nov 2026; older clones (or the site folder itself) have it at the top
const DIR = CLONE && existsSync(join(CLONE, "docs", "lessons.json")) ? join(CLONE, "docs") : CLONE;
const SERVER = { name: "aiexpo-lessons", title: "AIExpo Oracle lessons (GitHub copy)", version: "2026.10.31-1" };
const PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const LANG_FILE = { en: "README.en.md", th: "README.md" };
const LANG_PAGE = { en: "en", th: "th" };
const TOPICS = ["install", "account", "skill", "browser", "memory", "web", "verify", "troubleshooting"];
const MAX_IMAGES = 3;
const SIGNER = "0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78";

const filterProps = {
  lang: { type: "string", enum: ["th", "en"], description: "Only this language edition" },
  lesson: { type: "string", description: "Only this lesson id (see list_lessons), e.g. claude-chatgpt or ego-lite" },
  topic: { type: "string", enum: TOPICS, description: "Only chunks tagged with this topic" },
};
const ro = { readOnlyHint: true, openWorldHint: false };
const TOOLS = [
  {
    name: "search", title: "Search the lessons",
    description: "Search the AIExpo Oracle workshop lessons (Thai and English) by keyword. Returns sections; pass an id to fetch.",
    inputSchema: { type: "object", properties: { query: { type: "string", description: "What to look for, in Thai or English" }, ...filterProps }, required: ["query"] },
    annotations: ro,
  },
  {
    name: "fetch", title: "Read a lesson section",
    description: "Read the full text of a search result. id '<lesson>/<lang>/<section>' is one section, '<lesson>/<lang>' the whole lesson, e.g. 'claude-chatgpt/en/6' or 'ego-lite/th'.",
    inputSchema: { type: "object", properties: { id: { type: "string", description: "An id from search or list_lessons" } }, required: ["id"] },
    annotations: ro,
  },
  {
    name: "get_image", title: "Show a screenshot",
    description: "Return screenshots as images. id is an image id from fetch (e.g. 'claude-chatgpt/08-claude-capabilities.png') or a section id, which returns that section's screenshots, 3 at a time from 'start'.",
    inputSchema: { type: "object", properties: { id: { type: "string" }, start: { type: "integer", minimum: 0 } }, required: ["id"] },
    annotations: ro,
  },
  {
    name: "list_lessons", title: "List the lessons",
    description: "List every lesson in workshop order, with page URLs, language editions, and each section's id, title and topic tags.",
    inputSchema: { type: "object", properties: {} },
    annotations: ro,
  },
];

// ---- data ----
const rebase = (s) => (typeof s === "string" ? s.split(LIVE).join(BASE) : s);
async function get(path, asText = false) {
  if (DIR) {
    const t = await readFile(join(DIR, path), "utf8");
    return asText ? t : JSON.parse(t);
  }
  const r = await fetch(`${BASE}/${path}`);
  if (!r.ok) throw new Error(`${BASE}/${path}: HTTP ${r.status}`);
  return asText ? r.text() : r.json();
}
let cache = null;
async function load() {
  if (cache) return cache;
  const [lessons, index] = await Promise.all([get("lessons.json"), get("chunks.json")]);
  for (const c of index.chunks) {
    delete c.vec; // vectors need bge-m3 at query time; not used here
    c.url = rebase(c.url);
    c.words = new Set(words(`${c.title}\n${c.text}`));
    c.titleWords = new Set(words(c.title));
  }
  cache = { lessons, chunks: index.chunks };
  return cache;
}
let imageCache = null;
async function loadImages() {
  if (!imageCache) {
    imageCache = await get("images.json");
    for (const v of Object.values(imageCache)) v.url = rebase(v.url);
  }
  return imageCache;
}

const seg = new Intl.Segmenter("th", { granularity: "word" });
function words(s) {
  const out = [];
  for (const { segment, isWordLike } of seg.segment(s.toLowerCase())) if (isWordLike && (segment.length > 1 || /[฀-๿]/.test(segment))) out.push(segment);
  return out;
}
const lessonDir = (lessons, key) => lessons.find((l) => l.key === key).dir;
const absolute = (text, dir) => text.replace(/\]\((?!https?:|#|mailto:)([^)\s]+)\)/g, (_, p) => `](${BASE}/${dir}/${p.replace(/^\.\//, "")})`);
const result = (obj) => ({ content: [{ type: "text", text: JSON.stringify(obj) }], structuredContent: obj });
const fail = (text) => ({ content: [{ type: "text", text }], isError: true });

async function imageBlocks(keys) {
  if (!keys.length) return [];
  const imgs = await loadImages();
  return keys.filter((k) => imgs[k]).map((k) => ({ type: "image", data: imgs[k].data, mimeType: imgs[k].mimeType }));
}

async function find(lessons, chunks, id) {
  const c = chunks.find((x) => x.id === id);
  if (c) {
    const dir = lessonDir(lessons, c.lesson);
    return { id: c.id, title: c.label, text: absolute(c.text, dir), url: c.url,
      metadata: { ...c.tags, title: c.title, source: `${BASE}/${dir}/${LANG_FILE[c.lang]}`, signed_by: SIGNER } };
  }
  const parts = id.split("/");
  const [key, lang] = parts;
  const l = lessons.find((x) => x.key === key);
  if (!l || !LANG_FILE[lang] || parts.length !== 2) return null;
  const text = absolute(await get(`${l.dir}/${LANG_FILE[lang]}`, true), l.dir);
  return { id, title: lang === "th" ? l.th : l.en, text, url: `${BASE}/${l.dir}/${LANG_PAGE[lang]}`,
    metadata: { lesson: l.key, lang, sections: chunks.filter((x) => x.lesson === l.key && x.lang === lang).length, source: `${BASE}/${l.dir}/${LANG_FILE[lang]}`, signed_by: SIGNER } };
}

async function callTool(name, args) {
  const { lessons, chunks } = await load();
  if (name === "list_lessons") {
    return result({
      lessons: lessons.map((l, i) => ({
        order: i + 1, id: l.key, title: { th: l.th, en: l.en }, summary: { th: l.th_sub, en: l.en_sub },
        urls: { th: `${BASE}/${l.dir}/th`, en: `${BASE}/${l.dir}/en`, base64: `${BASE}/${l.dir}/`, llms: `${BASE}/${l.dir}/llms.txt` },
        editions: Object.keys(LANG_FILE).map((lang) => ({ lang, id: `${l.key}/${lang}`, markdown: `${BASE}/${l.dir}/${LANG_FILE[lang]}` })),
        sections: chunks.filter((c) => c.lesson === l.key && c.lang === "en").map((c) => ({ id: c.id, title: c.title, topic: c.tags.topic })),
      })),
    });
  }
  if (name === "search") {
    const q = String(args.query || "").trim();
    if (!q) return result({ results: [] });
    const qWords = [...new Set(words(q))];
    const pool = chunks.filter((c) => (!args.lang || c.lang === args.lang) && (!args.lesson || c.lesson === args.lesson) && (!args.topic || c.tags.topic.includes(args.topic)));
    const ranked = pool.map((c) => {
      let kw = 0;
      for (const w of qWords) kw += c.titleWords.has(w) ? 2 : c.words.has(w) ? 1 : 0;
      return { c, score: qWords.length ? kw / (2 * qWords.length) : 0 };
    }).filter((r) => r.score > 0).sort((a, b) => b.score - a.score).slice(0, 10);
    return result({
      results: ranked.map(({ c }) => ({ id: c.id, title: c.label, url: c.url })),
      mode: "keyword (stdio server; the hosted endpoint adds meaning search)",
      matches: ranked.map(({ c, score }) => ({ id: c.id, score: +score.toFixed(3), tags: c.tags })),
    });
  }
  if (name === "fetch") {
    const doc = await find(lessons, chunks, String(args.id || ""));
    if (!doc) return fail(`No lesson or section with id '${args.id}'. Use search or list_lessons for valid ids.`);
    const c = chunks.find((x) => x.id === doc.id);
    const refs = c ? c.images : [];
    const imgs = refs.length ? await loadImages() : {};
    doc.images = refs.map((r) => ({ id: r.key, alt: r.alt, url: imgs[r.key]?.url }));
    if (refs.length > MAX_IMAGES) doc.images_note = `${refs.length} screenshots; the first ${MAX_IMAGES} are attached. Call get_image with id '${doc.id}' and start ${MAX_IMAGES} for more.`;
    const res = result(doc);
    res.content.push(...(await imageBlocks(refs.slice(0, MAX_IMAGES).map((r) => r.key))));
    return res;
  }
  if (name === "get_image") {
    const id = String(args.id || "");
    const start = Math.max(0, Number(args.start) || 0);
    const c = chunks.find((x) => x.id === id);
    const keys = c ? c.images.slice(start, start + MAX_IMAGES).map((r) => r.key) : [id];
    const blocks = await imageBlocks(keys);
    if (!blocks.length) return fail(`No screenshot for '${id}'. Use an image id from fetch, or a section id that has screenshots.`);
    const imgs = await loadImages();
    const info = keys.filter((k) => imgs[k]).map((k) => {
      const alt = chunks.flatMap((x) => x.images).find((r) => r.key === k)?.alt || k;
      return { id: k, alt, url: imgs[k].url, width: imgs[k].width, height: imgs[k].height };
    });
    const more = c && c.images.length > start + MAX_IMAGES ? { next_start: start + MAX_IMAGES, total: c.images.length } : {};
    return { content: [{ type: "text", text: info.map((i) => `![${i.alt}](${i.url})`).join("\n") }, ...blocks], structuredContent: { images: info, ...more } };
  }
  return fail(`Unknown tool: ${name}`);
}

// ---- JSON-RPC over stdio (one message per line) ----
const ok = (id, result) => ({ jsonrpc: "2.0", id, result });
const rpcError = (id, code, message) => ({ jsonrpc: "2.0", id, error: { code, message } });
async function handle(msg) {
  if (!msg || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") return rpcError(msg?.id ?? null, -32600, "Invalid Request");
  const { id, method, params = {} } = msg;
  if (id === undefined) return null;
  try {
    switch (method) {
      case "initialize":
        return ok(id, {
          protocolVersion: PROTOCOLS.includes(params.protocolVersion) ? params.protocolVersion : PROTOCOLS[0],
          capabilities: { tools: { listChanged: false } },
          serverInfo: SERVER,
          instructions: "Read-only access to the AIExpo Oracle workshop lessons (AI Expo Thailand, 6 Nov 2026), from the GitHub copy. Use search, then fetch an id for the full text. Thai (th) and English (en).",
        });
      case "ping": return ok(id, {});
      case "tools/list": return ok(id, { tools: TOOLS });
      case "tools/call": return ok(id, await callTool(params.name, params.arguments || {}));
      case "resources/list": return ok(id, { resources: [] });
      case "prompts/list": return ok(id, { prompts: [] });
      default: return rpcError(id, -32601, `Method not found: ${method}`);
    }
  } catch (e) {
    return rpcError(id, -32603, String(e?.message || e));
  }
}
const send = (obj) => process.stdout.write(JSON.stringify(obj) + "\n");
let buf = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => {
  buf += d;
  let i;
  while ((i = buf.indexOf("\n")) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (!line) continue;
    let msg;
    try { msg = JSON.parse(line); } catch { send(rpcError(null, -32700, "Parse error")); continue; }
    const batch = Array.isArray(msg);
    Promise.all((batch ? msg : [msg]).map(handle)).then((out) => {
      out = out.filter(Boolean);
      if (out.length) send(batch ? out : out[0]);
    });
  }
});
