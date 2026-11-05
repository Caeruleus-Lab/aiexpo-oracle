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
AIExpo Oracle signed: herdr ⌘J ⌘L lesson
date: 2026-11-05
README.md sha256:aa0a805995802e2cf28cb1196dfd635afb7e152478b3a5652e0e4999dfbd1f9d
README.en.md sha256:c913bf96c0c518bb7f13cc6fc0f407c19e06663431b41067b008496575df9862
README.b64.txt sha256:082aec93272a7912fd7a57c81109286f6c6cc643fc45f4031c82fad67c126867
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
