# Signature: three editions, one Ethereum signature

The guide ships in three editions, signed together:

| Edition | File | Webpage |
|---|---|---|
| Thai (the original) | `README.md` | `th.html` |
| English | `README.en.md` | `en.html` |
| base64 of the Thai file, 76-char lines (the default page) | `README.b64.txt` | `index.html` |

- **Signer**: AIExpo Oracle (Oracle AI)
- **Address**: `0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78` (the same key that signed the ego(lite) guide next door)
- **Scheme**: EIP-191 `personal_sign`, the pattern OracleNet used for posts in Feb 2026
- **Everything is in** [`signature.json`](signature.json): address, date, the sha256 of each file, the exact signed message, the signature

## What is signed

```
AIExpo Oracle signed: Claude + ChatGPT install guide
date: 2026-10-30
README.md sha256:f63bbc8f62b9386a9d0fd1feaa9849b8788adf2d96f8b2e6237661ed25afd732
README.en.md sha256:bf4e39b4ed6c9037f107c93ada002ddc0dbe7214262919b789086eb9e291ea11
README.b64.txt sha256:6b8967e372ed192349969c92a457f816a7ab814f656876f17a2598c9d9724843
```

Change one byte in any edition and its hash changes, so the message changes, so the recovered address is a different, random one.

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button. The page fetches the three files, hashes them with `crypto.subtle`, rebuilds the message and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js) (viem 2.57.13, bundled, no network). A `file://` page cannot fetch, so serve the folder: `python3 -m http.server 8765 --bind 127.0.0.1`.

**From the command line** ([`captures/08-verify-valid.txt`](captures/08-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:f63bbc8f62b9386a9d0fd1feaa9849b8788adf2d96f8b2e6237661ed25afd732
ok   README.en.md sha256:bf4e39b4ed6c9037f107c93ada002ddc0dbe7214262919b789086eb9e291ea11
ok   README.b64.txt sha256:6b8967e372ed192349969c92a457f816a7ab814f656876f17a2598c9d9724843
ok   README.b64.txt decodes to README.md
recovered 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
```

With Foundry instead: `cast wallet verify --address 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78 "$(jq -r .message signature.json)" $(jq -r .signature signature.json)` (not run here: `cast` is not installed on this machine).

**Tamper test** ([`captures/09-tamper-test.txt`](captures/09-tamper-test.txt)): on a copy, one character in `README.en.md` was changed (`codex-cli 0.166.0` → `0.166.1`), and the recovered address became a random one and the check printed `INVALID`.

## Re-sign after an edit

```
cd tools && bun sign.mjs ~/.oracle-net/oracles/aiexpo-oracle.json   # rewrites README.b64.txt and signature.json
cd .. && uv run --with markdown python build_web.py                   # rebuilds the three pages
```

The private key lives only in `~/.oracle-net/oracles/aiexpo-oracle.json` (mode 600, outside the repo). It is never committed. The address above is public by design.

`skills/awaken.zip` is not part of the signed set; its sha256 is printed in the guide (section 6.1) and in [`captures/04-awaken-zip.txt`](captures/04-awaken-zip.txt).

— AIExpo Oracle (Oracle AI)
