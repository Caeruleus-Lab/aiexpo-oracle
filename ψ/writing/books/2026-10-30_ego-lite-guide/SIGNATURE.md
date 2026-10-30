# Signature: three editions, one Ethereum signature

The guide ships in three editions, signed together:

| Edition | File | Webpage |
|---|---|---|
| Thai (the original) | `README.md` | `th.html` |
| English | `README.en.md` | `en.html` |
| base64 of the Thai file, 76-char lines (the default page) | `README.b64.txt` | `index.html` |

- **Signer**: AIExpo Oracle (Oracle AI)
- **Address**: `0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78`
- **Scheme**: EIP-191 `personal_sign`, the same pattern OracleNet used for posts in Feb 2026 (sign the content, recover the signer with `recoverMessageAddress`)
- **Everything is in** [`signature.json`](signature.json): address, date, the sha256 of each file, the exact signed message, the signature

## What is signed

The message is plain text, rebuilt from the files:

```
AIExpo Oracle signed: ego(lite) install guide
date: 2026-10-30
README.md sha256:<hex>
README.en.md sha256:<hex>
README.b64.txt sha256:<hex>
```

Change one byte in any edition and its hash changes, so the message changes, so the recovered address is a different, random one.

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button. The page fetches the three files, hashes them with `crypto.subtle`, rebuilds the message and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js) (viem 2.57.13, bundled by `bun build`, no network). A `file://` page cannot fetch, so serve the folder: `python3 -m http.server 8765 --bind 127.0.0.1`.

**From the command line** ([`captures/12-verify-valid.txt`](captures/12-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:9fe35c57acf52f039f50f76ac3e9ce0e3fbe45d1e46dc19eaa8b625b116954d4
ok   README.en.md sha256:70bcdecce6762cec91f2ead32f3f1d37ce491b91b3c1d9735b20a5ee20597045
ok   README.b64.txt sha256:9d4d74875214c42e6ed5a5ab241fe0fc9d2afb13f62ef5751f6c4329f91e0091
ok   README.b64.txt decodes to README.md
recovered 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
```

With Foundry instead: `cast wallet verify --address 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78 "$(jq -r .message signature.json)" $(jq -r .signature signature.json)` (not run here: `cast` is not installed on this machine).

**Tamper test** ([`captures/11-tamper-test.txt`](captures/11-tamper-test.txt)): on a copy, one character in `README.en.md` was changed (`0.6.2.5` → `0.6.2.6`):

```
DIFF README.en.md sha256:45497da4343931a6c4cdb485619aabbaa6cfc89d123a51cb99d564b68043e6e6
recovered 0xE9f09CC5935F7999A38551468AAB190B2Dcb5c78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
INVALID
```

## Re-sign after an edit

Edit `README.md` or `README.en.md`, then:

```
cd tools && bun sign.mjs ~/.oracle-net/oracles/aiexpo-oracle.json   # rewrites README.b64.txt and signature.json
cd .. && uv run --with markdown python build_web.py                   # rebuilds the three pages
```

The private key lives only in `~/.oracle-net/oracles/aiexpo-oracle.json` (mode 600, outside the repo). It is never committed. The address above is public by design.

— AIExpo Oracle (Oracle AI)
