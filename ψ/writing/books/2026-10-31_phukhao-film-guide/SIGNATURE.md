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
AIExpo Oracle signed: Oracle film guide (Phukhao 9 months)
date: 2026-10-31
README.md sha256:4bb2f1d81069e757c7f1ea2afdb0ab62190c7cdb2cfb01ae227a34c4400788e8
README.en.md sha256:8023d35ebce2e2f742681fbec4d5041a1c4e62b313dda3b6f2e9d92c62ebf06f
README.b64.txt sha256:67be1af7fb4340a30f88be28d2097d6a79e71cd149bcb903c493a7584e937841
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line** ([`captures/09-verify-valid.txt`](captures/09-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:4bb2f1d81069e757c7f1ea2afdb0ab62190c7cdb2cfb01ae227a34c4400788e8
ok   README.en.md sha256:8023d35ebce2e2f742681fbec4d5041a1c4e62b313dda3b6f2e9d92c62ebf06f
ok   README.b64.txt sha256:67be1af7fb4340a30f88be28d2097d6a79e71cd149bcb903c493a7584e937841
ok   README.b64.txt decodes to README.md
recovered 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
```
