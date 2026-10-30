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
date: 2026-10-30
README.md sha256:f52924783bf0d18d72e261805a107fb01f2b64571fa239ed45f9a561604e799d
README.en.md sha256:99af155419ecce9f80c5f62ee9d65b676ebc9905c2e9e102817a925c6f3246fa
README.b64.txt sha256:40f6d51546ac34b995343b32628bbbb4489a61a1dba25e9b13f4035c5402e3e0
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line** ([`captures/07-verify-valid.txt`](captures/07-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:f52924783bf0d18d72e261805a107fb01f2b64571fa239ed45f9a561604e799d
ok   README.en.md sha256:99af155419ecce9f80c5f62ee9d65b676ebc9905c2e9e102817a925c6f3246fa
ok   README.b64.txt sha256:40f6d51546ac34b995343b32628bbbb4489a61a1dba25e9b13f4035c5402e3e0
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
