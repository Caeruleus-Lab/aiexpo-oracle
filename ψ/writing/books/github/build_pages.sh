#!/bin/sh
# Build the GitHub Pages copy of the lessons into a folder (default /tmp/aiexpo-lessons-pages).
# Same files as ./deploy.sh sends to Cloudflare (only what git tracks at HEAD), minus the Cloudflare config,
# plus .nojekyll, the stdio MCP server (github/mcp/server.mjs) and its package.json at the root.
# Then: commit that folder to Caeruleus-Lab/aiexpo-lessons main; Pages serves the root of main.
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
out=${1:-/tmp/aiexpo-lessons-pages}
top=$(git -C "$here" rev-parse --show-toplevel)
rel=${here#"$top"/}
mkdir -p "$out"
# keep the target repo's .git; replace everything else
find "$out" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git -C "$top" archive HEAD "$rel" | tar -x -C "$out" --strip-components="$(printf '%s' "$rel" | tr -cd / | wc -c | awk '{print $1+1}')"
rm -f "$out/wrangler.jsonc" "$out/deploy.sh" "$out/.gitignore"
mv "$out/github/package.json" "$out/package.json"
chmod +x "$out/github/mcp/server.mjs"
mkdir -p "$out/mcp" && mv "$out/github/mcp/server.mjs" "$out/mcp/server.mjs"
mv "$out/worker.js" "$out/mcp/worker.js"   # the hosted endpoint's source, for reference
rm -rf "$out/github"
# Nat, 5 Nov ("put in like some dir"): the build scripts go in tools/ so the root shows lessons and pages first.
# They are reference copies here; they run from the source repo (ψ/writing/books), where they sit next to index.html.
mkdir -p "$out/tools"
for f in build_index.py build_chunks.py build_media.py build_og.py build_skills_full.py check_site.py og_meta.py site_links.py video_html.py; do
  [ -f "$out/$f" ] && mv "$out/$f" "$out/tools/$f"
done
touch "$out/.nojekyll"
echo "files: $(find "$out" -type f ! -path '*/.git/*' | wc -l | tr -d ' ')  size: $(du -sh "$out" | cut -f1)"
