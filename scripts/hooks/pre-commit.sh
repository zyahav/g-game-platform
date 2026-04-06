#!/usr/bin/env bash
set -e

echo "[pre-commit] Running fast checks..."

STAGED_GD=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.gd$' || true)

if [ -n "$STAGED_GD" ]; then
  if git diff --cached -- $STAGED_GD | grep -E "FIXME"; then
    echo "[pre-commit] ❌ FIXME found in staged .gd files. Resolve before committing."
    exit 1
  fi
fi

echo "[pre-commit] ✅ Fast checks passed."
