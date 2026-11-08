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
AIExpo Oracle signed: herdr machines lesson
date: 2026-11-08
README.md sha256:763d2847959770abcb65c04c15d03b9ffea94b8020909b8e0e9892005213031e
README.en.md sha256:244b0b1c414923ab12ea9e976ff9b2ff9b8039775b778e6a8d94631274c1b2f8
README.b64.txt sha256:6fa763bfc560ff50ec07f54c01895d94e30e3039c90b7a99a3ced3736459adf3
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
