#!/bin/sh
# Deploy the committed lessons to https://aiexpo.buildwithoracle.com
# Only files tracked by git at HEAD are uploaded (no node_modules, no local audit output).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
top=$(git -C "$here" rev-parse --show-toplevel)
rel=${here#"$top"/}
rm -rf "$here/dist" && mkdir -p "$here/dist"
git -C "$top" archive HEAD "$rel" | tar -x -C "$here/dist" --strip-components="$(printf '%s' "$rel" | tr -cd / | wc -c | awk '{print $1+1}')"
python3 "$here/../slides/publish.py" "$here/dist/talk"   # the talk decks at /talk/, speaker notes stripped
rm -f "$here/dist/wrangler.jsonc" "$here/dist/deploy.sh" "$here/dist/.gitignore" "$here/dist/worker.js"
echo "files: $(find "$here/dist" -type f | wc -l | tr -d ' ')"
cd "$here" && npx -y wrangler@4 deploy "$@"
