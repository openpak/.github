#!/bin/sh
# Self-test: the fixture has two bad columns; one allowlist line each must turn the run green.
set -e
here=$(cd "$(dirname "$0")" && pwd)
d=$(mktemp -d)
trap 'rm -rf "$d"' EXIT
cp "$here/fixture/schema.sql" "$d/"
git -C "$d" init -q && git -C "$d" add -A
if python3 -I "$here/../dedup-lint.py" "$d" >/dev/null; then echo "FAIL: fixture should be flagged"; exit 1; fi
printf 'players.display_name  # test\nsessions.email  # test\n' > "$d/.dedup-allow"
git -C "$d" add -A
python3 -I "$here/../dedup-lint.py" "$d" | grep -q "ok (2" || { echo "FAIL: allowlist ignored"; exit 1; }
printf 'sessions.email\n' > "$d/.dedup-allow"
if python3 -I "$here/../dedup-lint.py" "$d" >/dev/null; then echo "FAIL: reason-less entry accepted"; exit 1; fi
echo "dedup-lint tests ok"
