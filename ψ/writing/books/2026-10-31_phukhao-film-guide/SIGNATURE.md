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
README.md sha256:a1acf60957ddc5098e9f68e124aeb8975406bc7751ada1ab6ac8fb84baad537c
README.en.md sha256:dc11acfae3eebf90b0bd294ce7f1a6623b28b778aec48f35cf10b3f960496813
README.b64.txt sha256:f70a44c784d0cfca7bf9192665f83953ce9ced53087c7391303f6d69064e2092
```

## Recover the signer

**In the browser**: open any of the three pages over http, scroll to "Signature" / "ตรวจลายเซ็น" and press the button; it re-hashes the files and runs viem's `recoverMessageAddress` from [`vendor/viem-verify.js`](vendor/viem-verify.js).

**From the command line** ([`captures/09-verify-valid.txt`](captures/09-verify-valid.txt)):

```
$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:a1acf60957ddc5098e9f68e124aeb8975406bc7751ada1ab6ac8fb84baad537c
ok   README.en.md sha256:dc11acfae3eebf90b0bd294ce7f1a6623b28b778aec48f35cf10b3f960496813
ok   README.b64.txt sha256:f70a44c784d0cfca7bf9192665f83953ce9ced53087c7391303f6d69064e2092
ok   README.b64.txt decodes to README.md
recovered 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
claimed   0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
VALID: signed by 0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78
```
