#!/usr/bin/env bash
# Download the ego(lite) DMG and verify it read-only. Never runs anything from the image.
# Usage: fetch-verify.sh [dest-dir]   (default ~/Downloads/ego-lite-<date>)
set -euo pipefail
[ "$(uname -s)" = Darwin ] || { echo "macOS only here. Windows (beta): https://lite.ego.app/download"; exit 2; }
ARCH=$(uname -m)
if [ "$ARCH" != arm64 ]; then
  echo "This script only knows the Apple Silicon URL (verified 2026-10-30)."
  echo "On $ARCH, download from https://lite.ego.app/download — the page picks the right build."; exit 2
fi
URL="https://cdn.ego.app/setup/macos/arm64/egolite.dmg"
DEST="${1:-$HOME/Downloads/ego-lite-$(date +%Y%m%d)}"
mkdir -p "$DEST"; DMG="$DEST/egolite.dmg"
echo "\$ curl -fL -o egolite.dmg $URL"
curl -fL --progress-bar -o "$DMG" "$URL"
echo; echo "\$ ls -lh egolite.dmg"; ls -lh "$DMG" | awk '{print $5, "egolite.dmg"}'
echo; echo "\$ shasum -a 256 egolite.dmg"; shasum -a 256 "$DMG" | awk '{print $1"  egolite.dmg"}'
MNT=$(mktemp -d /tmp/egolite-mnt.XXXX)
trap 'hdiutil detach "$MNT" >/dev/null 2>&1 || true' EXIT
hdiutil attach -nobrowse -readonly -mountpoint "$MNT" "$DMG" >/dev/null 2>&1
APP=$(ls -d "$MNT"/*.app | head -1)
echo; echo "\$ version inside"; defaults read "$APP/Contents/Info.plist" CFBundleShortVersionString
echo; echo "\$ codesign"; codesign -dv --verbose=2 "$APP" 2>&1 | grep -E '^(Identifier|TeamIdentifier|Authority=Developer ID Application)'
echo; echo "\$ spctl -a -vv"; OUT=$(spctl -a -vv "$APP" 2>&1); echo "$OUT" | sed "s|$MNT|<dmg>|"
TEAM=$(codesign -dv "$APP" 2>&1 | sed -n 's/^TeamIdentifier=//p')
echo
if echo "$OUT" | grep -q accepted && [ "$TEAM" = JGQLC6YQYJ ]; then
  echo "VERIFIED: notarized, signed by team JGQLC6YQYJ (CITRO LABS). DMG at $DMG"
else
  echo "NOT VERIFIED: do not install. Team=$TEAM"; exit 1
fi
