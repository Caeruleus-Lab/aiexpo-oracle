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
AIExpo Oracle signed: herdr bring promote lesson
date: 2026-11-08
README.md sha256:d6165b45fbf9b696cf764afa557864c37efb14cb1c96beef246a146455aac1e3
README.en.md sha256:efc42af3cce1e517074f27c4685dc807f20ddb92e955666be1d65a5cd592ded2
README.b64.txt sha256:103c292ab1c1a5070b85d7d95a54a202c5bc5b4c68f68c4308d1e50d9c42b37b
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
