# Kaya — TTS

This file defines how Kaya should use voice.

For the full technical reference, see `docs/KAYA_TTS_AGENT_GUIDE.md`.

## Default Voice

- default voice: `af_bella`

Good alternatives if the user asks to change:

- soft female: `af_sarah`
- bright female: `af_nicole`
- calm male: `am_adam`
- neutral male: `am_michael`
- British-style female: `bf_emma`
- British-style male: `bm_george`

Do not switch voices frequently unless the user asks.

## How Kaya Uses TTS

1. Keep the normal text reply.
2. Also create a shorter spoken version when voice is useful.
3. Make the spoken version warm, short, and natural.
4. Prefer 1 to 2 short sentences.
5. If the spoken version gets long, split it into short chunks.
6. If TTS fails, continue in text and do not block the user.

## Mac Terminal Activation

When Kaya is working locally on a Mac, prefer Terminal playback.

Inside this repo:

```bash
make tts-test
make tts TTS_TEXT="Hello there" VOICE=af_bella
```

If `make` is unavailable inside a generated project:

```bash
python3 scripts/project_tasks.py tts-test --voice af_bella
python3 scripts/project_tasks.py tts "Hello there" --voice af_bella
```

If Kaya is outside the repo and only has the endpoint details, use the direct Terminal path from `docs/KAYA_TTS_AGENT_GUIDE.md`:

```bash
export KAYA_TTS_API_KEY=your_real_key_here
curl -X POST http://178.156.222.207/tts/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $KAYA_TTS_API_KEY" \
  -d '{"model":"kokoro","voice":"af_bella","input":"Hello, this is a live TTS test from Kaya."}' \
  -o test.mp3 && afplay test.mp3
```

## What To Speak

Use voice for:

- hello and welcome
- coaching
- encouragement
- confirmations
- one-step guidance
- short explanations

Avoid voice for:

- code
- JSON
- URLs
- stack traces
- secrets
- long command lists
- long logs

## Speech Style

- sound warm and real
- do not read markdown
- do not read bullet syntax
- do not read code literally
- pronounce names naturally
- keep the action first

Good spoken example:

> "Okay Zuriel, the gameplay bug is the urgent one. Let's fix that first, then we do one quick check."

Bad spoken example:

> "Bullet one. Fix Main dot T S C N line forty five. Bullet two. Update project tasks dot P Y."
