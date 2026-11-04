// Screenshots of the relic5 hub UI on white, taken with ego-browser (Nat, 4 Nov: "use /ego-browser").
// Before each shot the page's private text is blurred in place: session text, search words, project, repo and
// people names, tokens. Headings, labels, numbers and charts stay. Run: ego-browser nodejs < captures/ui_capture_ego.mjs
// AIExpo Oracle (Oracle AI), 2026-11-04.
const IMG = "/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle/ψ/writing/books/2026-11-04_relic5-ui-tour/images/";
const HUB = "http://white.follow-rankine.ts.net:8795/";
const SHOTS = [
  ["01-home", "", "main li, main ul a", [[40, 770, 1160, 230]]],
  ["02-search", "search", "main li, main select, main table", [[40, 250, 1520, 750]], "AIExpo workshop"],
  ["03-live", "live", "main tbody td:nth-child(n+4)", []],
  ["04-knowledge", "memory", "main select", [[0, 420, 1600, 580]]],
  ["05-oracles", "oracles", "main table", [[40, 860, 1520, 140]]],
  ["06-map", "map", "main table, main aside", []],
  ["07-family", "family", "main table", []],
  ["08-asked", "queries", "main table", []],
  ["09-jobs", "jobs", "main tbody td:last-child", []],
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
    if (css) { const s = document.createElement("style"); s.textContent = css + "{filter:blur(7px)!important}"; document.head.appendChild(s); }
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
