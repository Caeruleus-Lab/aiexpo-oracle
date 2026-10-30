const task = await taskSpace("tutorial: ego lite guide");
const page = task.page("p1");
await page.goto("https://example.com");
await page.waitForLoadState();
console.log({ taskSpaceId: task.spaceId, page: page.label, title: await page.title() });
console.log(await page.snapshot());
