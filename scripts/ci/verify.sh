#!/usr/bin/env bash
set -e

echo "[ci] Running full verification..."

echo "[ci] Running tests..."
make test

echo "[ci] Running smoke check..."
make smoke

echo "[ci] Checking for FIXME markers..."
if grep -R "FIXME" . \
  --include="*.gd" \
  --exclude-dir=".git" \
  --exclude-dir="node_modules" \
  --exclude-dir="scripts" \
  --exclude-dir="templates"; then
  echo "[ci] ❌ FIXME found in gameplay files"
  exit 1
fi

echo "[ci] ✅ Full verification passed."
