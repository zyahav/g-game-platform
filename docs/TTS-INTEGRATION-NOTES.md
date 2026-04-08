# TTS Integration Notes

**Date:** April 7, 2026  
**Status:** Working for manual short speech. Automatic full-reply speech is not solved yet.

## Goal

Let Kaya speak to the student in a short, clean, natural way during the session.

The desired product is:

- full text reply for reading
- short spoken summary for listening
- no raw technical metadata spoken aloud

## What We Tested

### 1. Direct KAYA TTS endpoint

Confirmed working.

Mac terminal test:

```bash
export KAYA_TTS_API_KEY=your_real_key_here
curl -X POST http://178.156.222.207/tts/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $KAYA_TTS_API_KEY" \
  -d '{"model":"kokoro","voice":"af_bella","input":"Hello, this is a live TTS test from Kaya."}' \
  -o test.mp3 && afplay test.mp3
```

Result:

- works
- clean
- reliable

### 2. Repo helper commands

Confirmed working.

Platform repo:

```bash
make tts-test
make tts TTS_TEXT="Hello there" VOICE=af_bella
```

Generated project:

```bash
make tts-test
make tts TTS_TEXT="Hello there" VOICE=af_bella
python3 scripts/project_tasks.py tts "Hello there" --voice af_bella
```

Result:

- works
- good for manual short Kaya speech
- suitable for tonight's session

### 3. Codex global notify hook

Tested through:

- `~/.codex/config.toml`
- `/Users/zyahav/codex-notify.sh`

Findings:

- Codex notify events do not provide a clean final assistant reply
- the raw payload may contain:
  - thread ids
  - cwd paths
  - internal metadata
  - numbers and machine text
- using the notify hook as if it were a real reply reader produces bad student-facing speech

Result:

- not suitable for full automatic student speech
- only suitable for short event-based phrases

## Current Working Decision For Tonight

Use:

- manual short Kaya TTS for important moments

Do not use:

- automatic full-reply TTS from the current notify hook

Safe spoken pattern:

- short completion
- short encouragement
- short next-step line

Examples:

- "Nice. We finished this step."
- "Now send this to our advisor."
- "We fixed the two important bugs. Next we test the flow."

## Current Notify Hook Policy

The global notify hook has been cleaned so it:

- speaks a short phrase for:
  - approval
  - error
  - finished
- stays silent for noisy generic machine updates

This is acceptable as a light event notifier.
It is not the same thing as full conversational TTS.

## What Is Still Missing

We still do not have a reliable automatic path for:

- every final assistant reply
- a clean spoken summary derived from the real answer

That requires a better bridge than the notify hook.

## Recommended Future Architecture

### Short-term future option

Use a small Codex CLI wrapper around:

- `codex exec`

Flow:

1. send the prompt to Codex CLI
2. capture the real text response
3. derive a short `spoken_summary`
4. send only `spoken_summary` to Kaya TTS
5. play audio automatically

Why this is promising:

- cleaner than notify payloads
- easier to prototype than a deeper protocol integration

### Long-term stronger option

Use a structured integration around:

- `codex proto`

Why:

- better control over message boundaries
- better control over when a reply is complete
- better place to attach a spoken-summary field

## Recommendation

For tonight:

- keep manual short TTS
- keep the cleaned notify hook as a lightweight event voice only
- do not attempt to force full automatic speech through the current notify hook

After tonight:

- prototype a standalone Codex CLI wrapper using `codex exec`
- only move to `codex proto` if richer control is needed
