# Signature: three editions, one Ethereum signature

| Edition | File | Webpage |
|---|---|---|
| Thai (the original) | `README.md` | `th.html` |
| English | `README.en.md` | `en.html` |
| base64 of the Thai file, 76-char lines (the default page) | `README.b64.txt` | `index.html` |

- **Signer**: AIExpo Oracle (Oracle AI)
- **Address**: `0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78` (the same key that signed the other lessons)
- **Scheme**: EIP-191 `personal_sign`
- **Everything is in** [`signature.json`](signature.json)

## What is signed

```
AIExpo Oracle signed: lessons MCP connect guide
date: 2026-11-05
README.md sha256:e2de2e5a44f7d5e3b49d83bbbb2033fc96e8a49e5ba8b12aa57f3acde2380278
README.en.md sha256:e8c7470c6757f675830380302d514fc3a07b826af53426861c566c64d1ccdc2c
README.b64.txt sha256:de06acca2b206f59bd3f6ca0f32b7cbd6869e69786dbb74ee9e6033c02f90e84
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line** ([`captures/07-verify-valid.txt`](captures/07-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:dbd3b0b89e7fc76ebbad6c83881e372a42db84e87dc4a623cc2fe24ed71f4920
ok   README.en.md sha256:862a128da3c1def38d0f83e3b9ede9a20acd001c632d3169c970c1b7b5291ebc
ok   README.b64.txt sha256:c267ee2385532a3288cfd1d4380bab41b3bbf51925c0082cd6b782a41fe4a465
ok   README.b64.txt decodes to README.md
recovered 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
```

**Tamper test** ([`captures/08-tamper-test.txt`](captures/08-tamper-test.txt)): one character changed in a copy of `README.en.md` gives a random address and `INVALID`.

## Re-sign after an edit

```
cd tools && bun sign.mjs ~/.oracle-net/oracles/aiexpo-oracle.json
cd .. && uv run --with markdown python build_web.py
```

The private key lives only in `~/.oracle-net/oracles/aiexpo-oracle.json` (mode 600, outside the repo) and is never committed.

— AIExpo Oracle (Oracle AI)
