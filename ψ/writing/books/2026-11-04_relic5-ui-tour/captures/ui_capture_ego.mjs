// Screenshots of the relic5 hub UI on white, taken with ego-browser (Nat, 4 Nov: "use /ego-browser").
// Nat, 5 Nov: "re-shoot the ui tour without blur on my stuff" -- his own sessions, searches and projects show as they are.
// Only e-mail addresses and token-shaped strings are blurred, found in the page's text before each shot.
// Run: ego-browser nodejs < captures/ui_capture_ego.mjs   AIExpo Oracle (Oracle AI), 2026-11-04, re-shot 2026-11-05.
const IMG = "/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle/ψ/writing/books/2026-11-04_relic5-ui-tour/images/";
const HUB = "http://white.follow-rankine.ts.net:8795/";
const SHOTS = [
  ["01-home", "", "", []],
  ["02-search", "search", "", [], "AIExpo workshop"],
  ["03-live", "live", "", []],
  ["04-knowledge", "memory", "", []],
  ["05-oracles", "oracles", "", []],
  ["06-map", "map", "", []],
  ["07-family", "family", "", []],
  ["08-asked", "queries", "", []],
  ["09-jobs", "jobs", "", []],
  ["10-perf", "perf", "", []],
  ["11-quality", "compare", "", []],
  ["12-disk", "store", "", []],
  ["13-connect", "connect", "", []],
  ["14-incidents", "incidents", "", []],
];
const only = (globalThis.ONLY || []);
const task = await taskSpace("relic5 lesson capture");
const page = task.page("p1");
await page.cdp("Emulation.setDeviceMetricsOverride", { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });
for (const [name, tab, css, boxes, query] of SHOTS) {
  if (only.length && !only.includes(name)) continue;
  await page.goto(HUB + (tab ? "#tab=" + tab : ""));
  await page.reload();   // a hash change keeps the document: reload so no blur from the page before stays
  await page.waitForTimeout(7000);
  if (query) {
    await page.fill('input[placeholder="Words from any session. Every word must appear."]', query); await page.keyboard.press("Enter"); await page.waitForTimeout(5000);
  }
  const closed = await page.evaluate(({ css, boxes }) => {
    let closed = 0;   // fold the floating "open incidents" card with its own button
    for (const b of document.querySelectorAll('button[aria-label="Fold the incidents"]')) { b.click(); closed++; }
    const SECRET = /[\w.+-]+@[\w-]+\.[\w.]+|\b(?:ghp_|sk-|xox[bp]-|AKIA|AIza)[\w-]{12,}|\b[A-Za-z0-9]{40,}\b/;
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const hits = []; for (let n; (n = walk.nextNode());) if (SECRET.test(n.textContent) && n.parentElement) hits.push(n.parentElement);
    for (const el of hits) el.style.filter = "blur(6px)";
    for (const [x, y, w, h] of boxes) {
      const d = document.createElement("div");
      d.style.cssText = `position:fixed;left:${x}px;top:${y}px;width:${w}px;height:${h}px;backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);z-index:99;border-radius:12px`;
      document.body.appendChild(d);
    }
    return closed;
  }, { css, boxes });
  await page.waitForTimeout(800);
  await page.screenshot({ path: IMG + name + ".png", clip: { x: 0, y: 0, width: 1600, height: 1000 } }).catch(async () => { await page.waitForTimeout(3000); return page.screenshot({ path: IMG + name + ".png", clip: { x: 0, y: 0, width: 1600, height: 1000 } }); });
  console.log("shot", name, "closed", closed);
}
console.log({ space: task.spaceId });
