// Usage: bun verify.mjs   — recompute the hashes, rebuild the manifest, recover the signer.
import { recoverMessageAddress } from "viem";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FILES, manifest } from "./manifest.mjs";
const book = join(dirname(fileURLToPath(import.meta.url)), "..");
const sig = JSON.parse(readFileSync(join(book, "signature.json"), "utf8"));
let ok = true;
const hashes = {};
for (const f of FILES) {
  hashes[f] = createHash("sha256").update(readFileSync(join(book, f))).digest("hex");
  const same = hashes[f] === sig.files[f]; ok &&= same;
  console.log(`${same ? "ok  " : "DIFF"} ${f} sha256:${hashes[f]}`);
}
const decoded = Buffer.from(readFileSync(join(book, "README.b64.txt"), "utf8").replace(/\s+/g, ""), "base64");
const b64same = decoded.equals(readFileSync(join(book, "README.md"))); ok &&= b64same;
console.log(`${b64same ? "ok  " : "DIFF"} README.b64.txt decodes to README.md`);
const message = manifest(sig.date, hashes);
const recovered = await recoverMessageAddress({ message, signature: sig.signature });
const match = recovered.toLowerCase() === sig.address.toLowerCase(); ok &&= match;
console.log(`recovered ${recovered}`); console.log(`claimed   ${sig.address}`);
console.log(ok ? "VALID: signed by " + sig.address : "INVALID"); process.exit(ok ? 0 : 1);
