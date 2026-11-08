// The exact text that gets signed. Browser and CLI rebuild it the same way from the three files.
export const FILES = ["README.md", "README.en.md", "README.b64.txt"];
export const TITLE = "AIExpo Oracle signed: herdr machines lesson";
export function manifest(date, hashes) {
  return [TITLE, `date: ${date}`, ...FILES.map((f) => `${f} sha256:${hashes[f]}`)].join("\n");
}
