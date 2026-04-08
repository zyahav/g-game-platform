#!/usr/bin/env bash
set -euo pipefail

TTS_ENDPOINT="${KAYA_TTS_ENDPOINT:-http://178.156.222.207/tts/v1/audio/speech}"
TTS_API_KEY="${KAYA_TTS_API_KEY:-}"
TTS_MODEL="${KAYA_TTS_MODEL:-kokoro}"
TTS_VOICE="${KAYA_TTS_VOICE:-${VOICE:-af_bella}}"
TTS_TEXT="${*:-${TTS_TEXT:-}}"

if [[ -z "${TTS_TEXT}" ]]; then
  echo "usage: scripts/kaya_tts.sh \"Text to speak\"" >&2
  echo "optional env: VOICE=af_sarah or KAYA_TTS_VOICE=af_sarah" >&2
  exit 1
fi

if [[ -z "${TTS_API_KEY}" ]]; then
  echo "KAYA_TTS_API_KEY is required. Export it for this session before using Kaya TTS." >&2
  exit 1
fi

TMP_JSON="$(mktemp /tmp/kaya-tts-request.XXXXXX.json)"
TMP_AUDIO="$(mktemp /tmp/kaya-tts-audio.XXXXXX.mp3)"
cleanup() {
  rm -f "${TMP_JSON}" "${TMP_AUDIO}"
}
trap cleanup EXIT

python3 - <<'PY' "${TMP_JSON}" "${TTS_MODEL}" "${TTS_VOICE}" "${TTS_TEXT}"
import json
import sys
payload = {
    "model": sys.argv[2],
    "voice": sys.argv[3],
    "input": sys.argv[4],
}
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump(payload, fh)
PY

curl -sS -X POST "${TTS_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${TTS_API_KEY}" \
  --data @"${TMP_JSON}" \
  -o "${TMP_AUDIO}"

afplay "${TMP_AUDIO}"
