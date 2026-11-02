# Signature: three editions, one Ethereum signature

| Edition | File | Webpage |
|---|---|---|
| Thai (the original) | `README.md` | `th.html` |
| English | `README.en.md` | `en.html` |
| AI edition of the Thai file (the default page) | `README.b64.txt` | `index.html` |

- **Signer**: AIExpo Oracle (Oracle AI)
- **Address**: `0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78` (the same key that signed the other lessons)
- **Scheme**: EIP-191 `personal_sign`
- **Everything is in** [`signature.json`](signature.json)

## What is signed

```
AIExpo Oracle signed: agy lesson (Antigravity CLI with the lessons MCP)
date: 2026-11-02
README.md sha256:b46b6df289fc2c65498c334ecc1e414c477f27f245f912c2e6d9b20ba8a50d4d
README.en.md sha256:dccf7d1b0f78ab2b533ebef14354792cdb545dae74093240c05ae62303aca8cd
README.b64.txt sha256:a1e1f21063de9a9c9783784f9f6a970a7f64682c652d6f6a241b89a78b3229f8
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
