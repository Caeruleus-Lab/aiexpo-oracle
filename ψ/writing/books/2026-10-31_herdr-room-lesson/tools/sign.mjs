// Usage: bun sign.mjs <key.json>   (key file: { address, private_key }; never commit it)
// 1. writes README.b64.txt = base64 of README.md (76-char lines)
// 2. hashes the three editions, builds the manifest, signs it (EIP-191 personal_sign)
// 3. writes signature.json
import { privateKeyToAccount } from "viem/accounts";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FILES, manifest } from "./manifest.mjs";
const book = join(dirname(fileURLToPath(import.meta.url)), "..");
const key = JSON.parse(readFileSync(process.argv[2], "utf8"));
const b64 = readFileSync(join(book, "README.md")).toString("base64").replace(/(.{76})/g, "$1\n").trimEnd() + "\n";
writeFileSync(join(book, "README.b64.txt"), b64);
const hashes = Object.fromEntries(FILES.map((f) => [f, createHash("sha256").update(readFileSync(join(book, f))).digest("hex")]));
const date = new Date().toISOString().slice(0, 10);
const message = manifest(date, hashes);
const account = privateKeyToAccount(key.private_key);
const signature = await account.signMessage({ message });
const out = { signer: "AIExpo Oracle (Oracle AI)", address: account.address, scheme: "EIP-191 personal_sign", date, files: hashes, message, signature };
writeFileSync(join(book, "signature.json"), JSON.stringify(out, null, 2) + "\n");
console.log(message); console.log("address  ", account.address); console.log("signature", signature);
