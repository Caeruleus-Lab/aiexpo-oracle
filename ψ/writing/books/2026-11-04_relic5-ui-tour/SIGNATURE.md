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
AIExpo Oracle signed: relic5 UI tour lesson (lesson 10)
date: 2026-11-05
README.md sha256:0841730c3e2537c5dc92bfa93529c93669ec29dfed2149d31831a31aaa968f7f
README.en.md sha256:49bb4f5bd1acf537a07ff78c16fc6032895b4799051894d65fa4a21a4116c0ca
README.b64.txt sha256:2ad4fee0e45a0367f2fdb0c7cde647d5ecfb1434485de0a293b2f8f0b900cdb1
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line**: `cd tools && bun install && bun verify.mjs` prints `VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`.
