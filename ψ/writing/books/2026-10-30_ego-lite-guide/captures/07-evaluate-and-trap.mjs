const task = await taskSpace("tutorial: ego lite guide");
const page = task.page("p1");
const headings = await page.evaluate(() => [...document.querySelectorAll("h1,h2")].map(h => h.innerText.trim()));
console.log({ headings });
const a = await page.screenshot();
const b = await page.screenshot();
console.log({ first: a.split("/").pop(), second: b.split("/").pop(), samePath: a === b });
