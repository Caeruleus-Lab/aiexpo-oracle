// MCP full test: stdio server from GitHub (npx) and the hosted Worker, same calls on both
import { spawn } from "node:child_process";
const calls = [
  ["initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "aix-test", version: "1" } }],
  ["tools/list", {}],
  ["tools/call", { name: "list_lessons", arguments: {} }],
  ["tools/call", { name: "search", arguments: { query: "herdr room out", limit: 3 } }],
  ["tools/call", { name: "search", arguments: { query: "ติดตั้ง ego lite", lang: "th", limit: 3 } }],
  ["tools/call", { name: "fetch", arguments: { id: "herdr-room/en/11" } }],
  ["tools/call", { name: "get_image", arguments: { id: "herdr-room/01-room.png" } }],
];
function summ(method, r) {
  if (r.error) return "ERROR " + JSON.stringify(r.error).slice(0, 120);
  const x = r.result;
  if (method === "initialize") return `server ${x.serverInfo?.name} ${x.serverInfo?.version} proto ${x.protocolVersion}`;
  if (method === "tools/list") return "tools: " + x.tools.map((t) => t.name).join(", ");
  const c = x.content || [];
  const t = c.filter((b) => b.type === "text").map((b) => b.text).join("\n");
  const imgs = c.filter((b) => b.type === "image").map((b) => `${b.mimeType} ${Math.round(b.data.length * 0.75 / 1024)}KB`);
  return `${x.isError ? "isError " : ""}text ${t.length} chars${imgs.length ? " · image " + imgs.join(",") : ""} · ${t.replace(/\s+/g, " ").slice(0, 110)}`;
}
async function stdio() {
  const p = spawn("npx", ["-y", "github:Caeruleus-Lab/aiexpo-lessons"], { stdio: ["pipe", "pipe", "inherit"] });
  let buf = "", waiters = {};
  p.stdout.on("data", (d) => { buf += d; let i; while ((i = buf.indexOf("\n")) >= 0) { const l = buf.slice(0, i); buf = buf.slice(i + 1); if (!l.trim()) continue; const m = JSON.parse(l); waiters[m.id]?.(m); } });
  const out = [];
  for (const [n, [method, params]] of calls.entries()) {
    const r = await new Promise((res, rej) => { waiters[n + 1] = res; setTimeout(() => rej(new Error("timeout " + method)), 90000);
      p.stdin.write(JSON.stringify({ jsonrpc: "2.0", id: n + 1, method, params }) + "\n");
      if (method === "initialize") setTimeout(() => p.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n"), 0); });
    out.push(`  ${method} ${params.name || ""}: ${summ(method, r)}`);
  }
  p.kill(); return out;
}
async function http() {
  const out = []; let sid;
  for (const [n, [method, params]] of calls.entries()) {
    const res = await fetch("https://aiexpo.buildwithoracle.com/mcp", { method: "POST",
      headers: { "content-type": "application/json", accept: "application/json, text/event-stream", ...(sid ? { "mcp-session-id": sid } : {}) },
      body: JSON.stringify({ jsonrpc: "2.0", id: n + 1, method, params }) });
    sid ||= res.headers.get("mcp-session-id");
    let body = await res.text();
    if (body.startsWith("event:") || body.startsWith("data:")) body = body.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5)).join("");
    out.push(`  ${method} ${params.name || ""}: ${summ(method, JSON.parse(body))}`);
  }
  return out;
}
console.log("STDIO  npx -y github:Caeruleus-Lab/aiexpo-lessons"); console.log((await stdio()).join("\n"));
console.log("HOSTED https://aiexpo.buildwithoracle.com/mcp"); console.log((await http()).join("\n"));
