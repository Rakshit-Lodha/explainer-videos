---
name: sarvam-voice
description: Generate expressive, non-monotone narration with the Sarvam text-to-speech API using the Ratan voice, one take per scene, then concatenate the takes into a single timed voice track. Use after the script is approved, or whenever voiceover needs to be regenerated or re-tuned.
---

# Sarvam voice skill (Ratan, with emotion)

This is the only voice used for explainer videos; do not use ElevenLabs. Videos have no background music, so the voice track is the only audio.

## Setup
- Key: `SARVAM_API_KEY` in `/Users/rakshitlodha/Desktop/Videos/.env`. Never print it. Load it with `python-dotenv`.
- Python env: `/Users/rakshitlodha/Desktop/Videos/.venv` (has `requests`, `python-dotenv`).
- Endpoint verified in this project: `POST https://api.sarvam.ai/text-to-speech`, header `api-subscription-key`, JSON body
  `{"text", "target_language_code":"en-IN", "speaker":"ratan", "model":"bulbul:v3", "pace", "temperature"}`.
  The response is JSON with `audios`: a list of base64-encoded WAV strings. Decode `audios[0]`.
- `scripts/tts_reference.py` is the exact script used for the UPI video. Copy it into the topic folder and edit `narration.json` rather than rewriting it.

## How emotion is controlled
The API exposes no named emotion tags that were verified here, so emotion comes from three levers, tuned per scene:
1. **Take per scene.** Never send the whole script as one request; one flat take sounds monotone. One request per scene lets each have its own settings.
2. **`pace` and `temperature`.** Values that worked: pace 0.90 to 1.05, temperature 0.70 to 0.85.
   - Curious opening or reflective close: pace 0.90 to 0.95, temperature 0.80 to 0.85 (warmer, more varied).
   - Explanatory middle: pace 1.00, temperature 0.70 to 0.75 (steady, clear).
   - Building or rhythmic scene: pace 1.05, temperature 0.80.
   - Quiet, reassuring scene: pace 0.95, temperature 0.75.
3. **Punctuation in the text.** Commas, semicolons, a question mark and an em-free sentence rhythm shape intonation. Questions lift the voice; a clause set off by commas slows it. Write the narration the way it should be spoken.

Listen to at least the first and last takes before moving on. If a scene sounds flat, raise temperature by 0.05 and slow pace by 0.05, regenerate only that id (`python tts.py s3`), and re-concatenate.

## Steps
1. Read `narration.json` (`id`, `pace`, `temperature`, `text`).
2. Run `tts.py` to write `audio/<id>.wav` per scene. Print the HTTP status and first 300 characters of the body on failure; do not retry blindly.
3. Measure each take with `ffprobe -v error -show_entries format=duration -of csv=p=0`.
4. Concatenate with a gap of 0.45 s between scenes and a 1.5 s tail, using `adelay` per input and `amix=normalize=0` (see the snippet in the project history: build a filter chain `[k:a]aresample=44100,aformat=channel_layouts=mono,adelay=<ms>[ak]`, then `amix`, then `apad=whole_dur=<total>`). Write `hf/assets/voice.wav`.
5. Save `timing.json` with `starts`, `dur` and `total`. The motion-graphics scenes take their start times and durations from it, so regenerate it whenever any take changes.
6. If the total drifts past the target length, trim narration text; do not speed the audio up with ffmpeg.

## Checks
- Total duration matches the plan within a couple of seconds.
- No scene's audio is clipped; `ffmpeg -af volumedetect` max volume stays below 0 dB.
- Final mix is loudness-normalised at the very end (`loudnorm=I=-14:TP=-1.5:LRA=7`), not per take.
