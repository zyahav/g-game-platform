# KAYA TTS Agent Guide

Last updated: 2026-04-07

This guide is for agents that need to speak to users through the KAYA TTS service, not only respond in text.

## Purpose

Use this document as the standard reference for any agent that should generate spoken responses for students or end users.

The goal is:

- keep the main answer in text
- create a shorter spoken version when voice is useful
- play or return audio quickly
- avoid reading technical content aloud verbatim

## Endpoint

Use:

- Remote: `http://178.156.222.207/tts/v1/audio/speech`
- From inside the VM: `http://127.0.0.1/tts/v1/audio/speech`

## Authentication

Send this HTTP header:

```text
X-API-Key: <KAYA_TTS_API_KEY>
```

Keep the real key out of git. Provide it at runtime through the environment or paste it into the live student/coach session only when needed.

## Default Request

Use these defaults unless there is a reason to override them:

- `model`: `kokoro`
- `voice`: `af_bella`
- `response_format`: `mp3`
- `stream`: `true`

## How To Choose A Voice

Set the `voice` field in the JSON request body.

Example:

```json
{
  "model": "kokoro",
  "voice": "af_bella",
  "input": "Hello, I can now speak with you.",
  "response_format": "mp3",
  "stream": true
}
```

If you want one stable default voice for all student agents, use:

- `af_bella`

That is the current recommended default because it is clear, natural, and already used as the default throughout this guide.

Good alternatives:

- `af_sarah`
- `af_nicole`
- `af_sky`
- `am_adam`
- `am_michael`
- `bf_emma`
- `bm_george`
- `bm_lewis`

## Verified Voice List On KAYA

The following voice IDs were verified directly from the installed Kokoro voice files on KAYA on 2026-04-07.

Total installed voices: `67`

### `af_*`

- `af_alloy`
- `af_aoede`
- `af_bella`
- `af_heart`
- `af_jadzia`
- `af_jessica`
- `af_kore`
- `af_nicole`
- `af_nova`
- `af_river`
- `af_sarah`
- `af_sky`
- `af_v0`
- `af_v0bella`
- `af_v0irulan`
- `af_v0nicole`
- `af_v0sarah`
- `af_v0sky`

### `am_*`

- `am_adam`
- `am_echo`
- `am_eric`
- `am_fenrir`
- `am_liam`
- `am_michael`
- `am_onyx`
- `am_puck`
- `am_santa`
- `am_v0adam`
- `am_v0gurney`
- `am_v0michael`

### `bf_*`

- `bf_alice`
- `bf_emma`
- `bf_lily`
- `bf_v0emma`
- `bf_v0isabella`

### `bm_*`

- `bm_daniel`
- `bm_fable`
- `bm_george`
- `bm_lewis`
- `bm_v0george`
- `bm_v0lewis`

### Other installed voices

- `ef_dora`
- `em_alex`
- `em_santa`
- `ff_siwis`
- `hf_alpha`
- `hf_beta`
- `hm_omega`
- `hm_psi`
- `if_sara`
- `im_nicola`
- `jf_alpha`
- `jf_gongitsune`
- `jf_nezumi`
- `jf_tebukuro`
- `jm_kumo`
- `pf_dora`
- `pm_alex`
- `pm_santa`
- `zf_xiaobei`
- `zf_xiaoni`
- `zf_xiaoxiao`
- `zf_xiaoyi`
- `zm_yunjian`
- `zm_yunxi`
- `zm_yunxia`
- `zm_yunyang`

## Voice Selection Policy

For consistency across student agents, pick one default and keep it stable.

Recommended baseline:

- default voice: `af_bella`

If you want a different house voice, choose one of these and use it everywhere:

- warm female: `af_bella`
- soft female: `af_sarah`
- bright female: `af_nicole`
- calm male: `am_adam`
- neutral male: `am_michael`
- British-style female: `bf_emma`
- British-style male: `bm_george`

Unless there is a strong reason to vary voices per student, do not switch voices frequently. Consistency usually feels more natural.

## Basic Request Format

```json
{
  "model": "kokoro",
  "voice": "af_bella",
  "input": "Hello, I can now speak with you.",
  "response_format": "mp3",
  "stream": true
}
```

## Curl Example

```bash
curl -X POST http://178.156.222.207/tts/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $KAYA_TTS_API_KEY" \
  -d '{"model":"kokoro","voice":"af_bella","input":"Hello, I am your study assistant, and I can now speak with you in real time.","response_format":"mp3","stream":true}' \
  -o /tmp/student-tts.mp3
```

On macOS:

```bash
afplay /tmp/student-tts.mp3
```

## Mac Terminal Quick Start

If you are on a Mac and just want to hear Kaya speak from Terminal, use one of these two paths.

### Option A — Fastest direct test from any folder

This does not depend on the repo. It generates the audio file and plays it immediately.

```bash
export KAYA_TTS_API_KEY=your_real_key_here
curl -X POST http://178.156.222.207/tts/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $KAYA_TTS_API_KEY" \
  -d '{"model":"kokoro","voice":"af_bella","input":"Hello, this is a live TTS test from Kaya."}' \
  -o test.mp3 && afplay test.mp3
```

If you are already in a folder like:

```text
/Users/zyahav/Documents/dev/178.156.149.111
```

then this is enough:

```bash
afplay test.mp3
```

### Option B — Repo helper command

Inside the platform repo:

```bash
cd /Users/zyahav/farm-game
export KAYA_TTS_API_KEY=your_real_key_here
make tts-test
```

Or speak custom text:

```bash
cd /Users/zyahav/farm-game
export KAYA_TTS_API_KEY=your_real_key_here
make tts TTS_TEXT="Hey Zuriel, let's fix the gameplay bug first." VOICE=af_bella
```

Available voices include:

- `af_bella`
- `af_sarah`
- `af_nicole`
- `am_adam`
- `am_michael`
- `bf_emma`
- `bm_george`

### Generated Project Helper

Generated student projects should also support:

```bash
export KAYA_TTS_API_KEY=your_real_key_here
make tts-test
make tts TTS_TEXT="Hello there" VOICE=af_bella
python3 scripts/project_tasks.py tts "Hello there" --voice af_bella
```

## Recommended Agent Behavior On Mac

When an agent is working locally on a Mac:

1. Prefer `make tts-test` for a quick sanity check.
2. Prefer `make tts TTS_TEXT="..." VOICE=...` for normal voice playback.
3. Fall back to direct `curl ... && afplay ...` only when working outside the repo.
4. Do not use GUI players when Terminal playback is enough.

## Agent Policy

Agents that use KAYA TTS should follow these rules:

1. Keep the normal text response.
2. Create a separate spoken version when audio is helpful.
3. Keep spoken output short, natural, and easy to follow.
4. Do not read raw code, JSON, URLs, stack traces, or long logs aloud.
5. If the answer is long, summarize it for speech instead of reading it word for word.
6. If TTS fails, continue with text and do not block the user.

## When To Use TTS

Use TTS for:

- coaching
- encouragement
- onboarding
- short explanations
- confirmations
- step-by-step guidance
- accessibility support

Avoid TTS for:

- large code blocks
- raw terminal output
- JSON
- long lists of commands
- secret values
- content that is too long to listen to comfortably

## Speech Style Rules

The spoken version should:

- sound warm and natural
- stay short, ideally 1 to 2 sentences per chunk
- avoid markdown and bullet formatting
- avoid special characters and code syntax
- avoid reading punctuation literally unless needed
- use natural pronunciation

Example:

- Say `Kaya`
- Do not say `K-A-Y-A`

If pronunciation may be wrong, rewrite the text phonetically before sending it to TTS.

## Real-Time TTS Flow

When the agent wants to speak in real time, it should:

1. Generate the text response.
2. Create a shorter spoken version.
3. Split long spoken content into short chunks.
4. Send the first chunk to TTS immediately.
5. Start playback as soon as the first chunk is ready.
6. Continue generating and playing later chunks without blocking the conversation.
7. Fall back to text-only if audio generation fails.

## Recommended Spoken Chunk Rules

- Aim for 1 to 2 sentences per chunk.
- Keep chunks under about 200 characters when possible.
- Prefer complete thoughts over arbitrary splits.
- If a message includes actions, speak the most important action first.

## Suggested System Instruction For Other Agents

```text
You can speak to the user using the KAYA TTS service.

TTS endpoint:
- Remote: http://178.156.222.207/tts/v1/audio/speech
- Local on the VM: http://127.0.0.1/tts/v1/audio/speech

Authentication:
- Send header X-API-Key: <KAYA_TTS_API_KEY>

Default TTS settings:
- model: kokoro
- voice: af_bella
- response_format: mp3
- stream: true

Behavior rules:
- Keep the normal text answer.
- Create a shorter spoken version when voice is helpful.
- Use TTS for short coaching, onboarding, encouragement, confirmations, and guided help.
- Do not read code blocks, JSON, URLs, stack traces, or long logs aloud.
- If a response is long, summarize it for speech.
- Speak naturally and warmly.
- Keep spoken chunks short.
- Pronounce names naturally, for example say Kaya, not K-A-Y-A.
- If TTS fails, continue in text without blocking the user.
```

## Minimal Pseudocode

```text
text_reply = generate_text_reply()
spoken_reply = shorten_for_speech(text_reply)

if spoken_reply is not empty:
    for chunk in split_into_short_chunks(spoken_reply):
        call_tts(chunk)
        play_or_return_audio(chunk)
else:
    return text_reply
```

## Health Check

```bash
curl http://178.156.222.207/health
```

Expected response:

```text
ok
```

## Self-Test Command

```bash
curl -X POST http://178.156.222.207/tts/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $KAYA_TTS_API_KEY" \
  -d '{"model":"kokoro","voice":"af_bella","input":"Hello, this is a live TTS test from Kaya.","response_format":"mp3","stream":true}' \
  -o /tmp/kaya-tts-test.mp3 && afplay /tmp/kaya-tts-test.mp3
```

## Notes

- This guide is intentionally practical and copy-paste friendly.
- If you later rotate the API key or change the endpoint, update this file first so other agents have one source of truth.
