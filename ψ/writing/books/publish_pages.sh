#!/bin/sh
# Mirror the committed lessons to a GitHub Pages repo: the same files ./deploy.sh uploads to
# https://aiexpo.buildwithoracle.com (already public there), plus the MCP Worker source under mcp/.
# GitHub Pages serves static files only, so /mcp itself stays on the Worker; the pages link to it by full URL.
# Usage: ./publish_pages.sh <checkout of the pages repo>   (commits there; push is a separate, explicit step)
set -eu
here=$(cd "$(dirname "$0")" && pwd)
out=${1:?usage: publish_pages.sh <pages repo checkout>}
top=$(git -C "$here" rev-parse --show-toplevel)
rel=${here#"$top"/}
head=$(git -C "$top" rev-parse --short HEAD)
[ -d "$out/.git" ] || { echo "not a git checkout: $out"; exit 2; }
git -C "$out" ls-files -z | (cd "$out" && xargs -0 rm -f)   # tracked files only; history keeps the old ones
git -C "$top" archive HEAD "$rel" | tar -x -C "$out" --strip-components="$(printf '%s' "$rel" | tr -cd / | wc -c | awk '{print $1+1}')"
rm -rf "$out/dist" "$out/deploy.sh" "$out/publish_pages.sh" "$out/.gitignore"
mkdir -p "$out/mcp" && mv "$out/worker.js" "$out/wrangler.jsonc" "$out/mcp/"
touch "$out/.nojekyll"   # serve every file as is (no Jekyll)
cat > "$out/mcp/README.md" <<'MD'
# AIExpo lessons MCP

Read-only MCP server for the AIExpo Oracle workshop lessons, live at **https://aiexpo.buildwithoracle.com/mcp**
(Streamable HTTP, no login). Tools: `search` (keyword + bge-m3 cosine over `chunks.json`), `fetch`, `list_lessons`,
`get_image`.

It runs as a Cloudflare Worker (`worker.js`) next to the static lessons. GitHub Pages cannot run it, so the Pages copy
of the site points at the Worker URL above. To run your own: copy the site files into `dist/` beside this folder's
`worker.js` and `wrangler.jsonc`, set your own `account_id` and route, and `npx wrangler deploy`.

Add it to a client:

```sh
claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp
```

— AIExpo Oracle (Oracle AI)
MD
find "$out" -type f -size +95M -not -path '*/.git/*' | sed 's/^/too big for GitHub: /'
git -C "$out" add -A
git -C "$out" -c core.hooksPath=/dev/null commit -q -m "site: lessons at $head (mirror of aiexpo.buildwithoracle.com)" || echo "nothing changed"
git -C "$out" log --oneline -1
