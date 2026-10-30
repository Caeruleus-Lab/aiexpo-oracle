const task = await taskSpace("tutorial: ego lite guide");
const page = task.page("p1");
const receipt = await page.click("text=Learn more", { label: "open IANA help page" });
await page.waitForURL(/iana\.org/);
const path = await page.screenshot({ path: "/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle/wt/ego-lite-guide-aiexpo-30oct-fri2026/ψ/writing/books/2026-10-30_ego-lite-guide/images/11-iana-after-click.png" });
console.log({ url: await page.url(), title: await page.title(), screenshot: path.split("/").pop() });
console.log(await task.pages());
