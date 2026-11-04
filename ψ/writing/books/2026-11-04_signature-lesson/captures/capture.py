"""Every command of the signature lesson, run for real on m5, 4 Nov 2026. Each file: the command, then what it printed.
The real key is never read or printed here: steps 06-07 sign a COPY of a lesson with a fresh demo key made in /tmp.
Usage: python3 captures/capture.py [NN ...]        AIExpo Oracle (Oracle AI), 2026-11-04."""
import pathlib, subprocess, sys

C = pathlib.Path(__file__).resolve().parent
BOOKS = C.parent.parent
REAL = BOOKS / "2026-11-04_relic5-install"
DEMO = "/tmp/sig-demo"

def run(cmd, cwd=None, cut=40):
    p = subprocess.run(["zsh", "-c", cmd], cwd=cwd, capture_output=True, text=True, timeout=300)
    out = (p.stdout + p.stderr).rstrip().split("\n")
    if len(out) > cut: out = out[:cut] + [f"... ({len(out) - cut} more lines cut)"]
    return out, p.returncode

def step(nn, slug, cmd, cwd=None, shown=None, cut=40):
    if only and nn not in only: return
    out, rc = run(cmd, cwd, cut)
    tail = [] if rc == 0 else [f"(exit {rc})"]
    (C / f"{nn}-{slug}.txt").write_text("\n".join([f"$ {shown or cmd}"] + out + tail).rstrip() + "\n", encoding="utf-8")
    print(nn, slug, len(out), "lines rc", rc)

only = sys.argv[1:]
step("01", "files", "ls -1 README.md README.en.md README.b64.txt signature.json SIGNATURE.md tools/ vendor/ && echo && cat tools/manifest.mjs", cwd=REAL,
     shown="ls README.md README.en.md README.b64.txt signature.json SIGNATURE.md tools/ vendor/ && cat tools/manifest.mjs")
step("02", "hashes", "shasum -a 256 README.md README.en.md README.b64.txt && echo && python3 -c \"import json; [print(v, ' ', k) for k, v in json.load(open('signature.json'))['files'].items()]\"", cwd=REAL,
     shown="shasum -a 256 README.md README.en.md README.b64.txt      # then the same three from signature.json")
step("03", "signature-json", "cat signature.json", cwd=REAL)
step("04", "verify-real", "bun verify.mjs", cwd=REAL / "tools", shown="cd tools && bun verify.mjs")
step("05", "eip191", """bun -e '
import { hashMessage, toBytes, recoverMessageAddress } from "viem";
import { readFileSync } from "node:fs";
const s = JSON.parse(readFileSync("../signature.json", "utf8"));
const m = toBytes(s.message);
console.log("message bytes      ", m.length);
console.log("prefix             ", JSON.stringify("\\x19Ethereum Signed Message:\\n" + m.length));
console.log("keccak256(prefix+m)", hashMessage(s.message));
console.log("signature r        ", s.signature.slice(0, 66));
console.log("signature s        ", "0x" + s.signature.slice(66, 130));
console.log("signature v        ", parseInt(s.signature.slice(130), 16));
console.log("recovered address  ", await recoverMessageAddress({ message: s.message, signature: s.signature }));
'""", cwd=REAL / "tools", shown="bun -e '… hashMessage, recoverMessageAddress from viem …'   # EIP-191 by hand")
step("06", "demo-sign", f"""rm -rf {DEMO} && mkdir -p {DEMO} && cp -R README.md README.en.md tools {DEMO}/ && cd {DEMO}/tools && bun -e '
import {{ generatePrivateKey, privateKeyToAccount }} from "viem/accounts";
import {{ writeFileSync }} from "node:fs";
const k = generatePrivateKey(); const a = privateKeyToAccount(k);
writeFileSync("/tmp/sig-demo-key.json", JSON.stringify({{ address: a.address, private_key: k }}), {{ mode: 0o600 }});
console.log("demo address", a.address, "(private key kept in /tmp/sig-demo-key.json, 0600, not shown)");
' && bun sign.mjs /tmp/sig-demo-key.json | tail -2 && bun verify.mjs | tail -3""", cwd=REAL,
     shown="cp -R README.md README.en.md tools /tmp/sig-demo/ && cd /tmp/sig-demo/tools\n$ bun -e '…generatePrivateKey…'   # a fresh demo key, never the real one\n$ bun sign.mjs /tmp/sig-demo-key.json && bun verify.mjs")
step("07", "tamper", f"cd {DEMO} && sed -i '' 's/relic5/relic6/' README.en.md && cd tools && bun verify.mjs",
     shown="sed -i '' 's/relic5/relic6/' README.en.md      # change one word in the English edition\n$ bun verify.mjs")
step("08", "wrong-claim", f"""cd {DEMO} && cp ../2026-11-04_relic5-install/README.en.md . 2>/dev/null; cp {REAL}/README.en.md . && python3 -c "
import json; s = json.load(open('signature.json')); s['address'] = '0xaBF18fdb07fB05e75832CAB954BE2eE92D155f78'; json.dump(s, open('signature.json', 'w'), indent=2)" && cd tools && bun verify.mjs""",
     shown="cp <the real README.en.md back> && edit signature.json: claim the AIExpo Oracle address instead of the demo one\n$ bun verify.mjs")
step("09", "key-file", "ls -l ~/.oracle-net/oracles/aiexpo-oracle.json | awk '{print $1, $NF}'; git -C " + str(BOOKS) + " check-ignore -q ~/.oracle-net 2>/dev/null; echo 'in the repo: no (it lives in ~/.oracle-net, outside every checkout)'",
     shown="ls -l ~/.oracle-net/oracles/aiexpo-oracle.json      # permissions only, never the content")
