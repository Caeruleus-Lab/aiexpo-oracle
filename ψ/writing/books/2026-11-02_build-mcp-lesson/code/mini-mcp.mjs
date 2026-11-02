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
