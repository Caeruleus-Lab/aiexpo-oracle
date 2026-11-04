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
AIExpo Oracle signed: digital signature lesson (lesson 12)
date: 2026-11-04
README.md sha256:86bf069c5d25f691ace9103ffd7b0713d460a3b36f22563974b366ee30c445da
README.en.md sha256:2ce26390d788e84700795307cead16a1f09ed1ea024bcccc7cb7c6b3960057ab
README.b64.txt sha256:aade69233fb49b8e72646ca2b3db44d2cb63714ae1b6e51a2cd4d59618658007
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
