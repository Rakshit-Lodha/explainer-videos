# Explainer-video workflow

This folder produces short narrated explainer videos (9:16, 1080x1920, 60-90 s, hard ceiling 4 minutes) in a dark-navy, amber-and-teal motion-graphics style. The first finished example is `upi/` (`How_UPI_Works.mp4`); follow its layout for new topics.

## Skills to load, in order
Load each skill with the Skill tool at the step that needs it, not all up front.

| Step | Skill | What it covers |
|---|---|---|
| 1. Script | `video-script` | Scene beats, professorial narration, approval gate. |
| 2. Voice | `sarvam-voice` | Sarvam Ratan TTS, per-scene emotion settings, timed voice track. |
| 2. Voice (alt.) | `elevenlabs-voice` | Eleven v4 in the user's cloned voice, audio-tag emotion, timestamps, A/B stability tests, retiming the composition. Use when the user supplies or wants ElevenLabs audio. |
| 3. Music | `suno-music` | Suno via Chrome, download, trim, fade, duck. |
| 4. Visuals | `/hyperframes` (shipped inside each Hyperframes project, see `<topic>/hf/AGENTS.md`) | Composition authoring, check, snapshot, render. |

If a Hyperframes skill is missing, run `npx hyperframes@0.8.118 skills update <name>`.

## Pipeline
1. **Script.** Write it with `video-script`, show it to the user, and wait for an explicit approval. Do not generate anything before that.
2. **Voice.** `narration.json` to `audio/<id>.wav` to `hf/assets/voice.wav` and `timing.json` (`sarvam-voice`), or `narration_eleven.json` to `eleven/voice.mp3` and `timing_eleven.json` (`elevenlabs-voice`). This fixes every scene's start time and duration; whichever voice is used, re-anchor the composition's beats to its sentence times.
3. **Keyframes and reference images.** `gpt-image-2.5-sunburst-2026-09-08` via `POST /v1/images/generations` (size `1024x1536`, response `b64_json`). First generate a style reference sheet, then the scene plates, always with the same style prefix (dark navy `#0a1020`, amber `#f5b942`, teal `#4fd1c5`, flat vector, no text, bloom). Use images only where illustration earns its place (e.g. an opening scene plate); diagrams are drawn in HTML.
4. **Motion graphics.** One Hyperframes composition, `hf/index.html`, one paused GSAP timeline, scene start times taken from `timing.json`.
5. **Animatic.** `render --quality draft` with the voice; show the user stills (`snapshot --at ...`) or the file and fix issues before the final render.
6. **Music.** `suno-music`, written to `hf/assets/music.wav` (a silent placeholder is fine until then).
7. **Timeline record.** Build an OpenTimelineIO file (`otio_build.py`, output `build/<topic>.otio`) from `timing.json`: video track of scenes, voice track, music track. It documents the edit; the render itself is driven by Hyperframes.
8. **Final render and master.** `render --quality delivery`, then one ffmpeg pass: `-c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=7 -c:a aac -b:a 192k -movflags +faststart`. Verify with `ffprobe` (1080x1920, duration) and sample frames.

## Environment
- Project root `/Users/rakshitlodha/Desktop/Videos`; keys in `.env`: `SARVAM_API_KEY`, `OPENAI_API_KEY`, `FAL_AI`, `GEMINI_API_KEY`, `ELEVEN_LABS_API_KEY`, `ELEVENT_LABS_VOICE_ID` (sic). Never print or commit them.
- Python venv `.venv` (opentimelineio, yt-dlp, requests, python-dotenv). Node via nvm. ffmpeg at `/opt/homebrew/bin/ffmpeg`.
- Not installed: Manim. Motion Canvas exists on npm but was not needed.
- Use the pinned CLI everywhere: `npx -y hyperframes@0.8.118 ...` (plain `npx hyperframes` tried to fetch a non-existent newer version).
- Scratch files go in the session scratchpad, deliverables in `<topic>/` and the project root.

## Hyperframes rules learned the hard way
- Animate transforms (`x`, `y`, `scale`, `rotation`, `autoAlpha`), never `left`, `top` or `width`; lint fails otherwise. For multi-step moves, track a virtual position and tween relative offsets.
- A `fromTo` whose from-state is visible renders that state from time zero. Add `immediateRender:false` for rings, ripples and anything that must stay hidden until its cue.
- No `Math.random()` or `Date.now()`; use a seeded generator for particle fields.
- Intentional overlaps and occlusions need `data-layout-allow-overlap` / `data-layout-allow-occlusion` on the element the checker names, often its inner span.
- Every created element must exist before the first seek; build DOM synchronously in the script, then register `window.__timelines["main"]`.
- Run `check` after every edit, then `snapshot --at t1,t2,...` and read the contact sheets. Look for stray elements, missing nodes and text on top of icons; the checker does not catch those.

## What not to do
- No generated video (Veo, Seedance) unless the user asks: this style is flat graphics, and generated footage clashes and costs money. `FAL_AI` exists if that changes; model availability was not tested.
- No real footage via yt-dlp unless the user asks; it is installed but was unused. If used, only Creative Commons clips and write the credits to a file.
- No short staccato narration and no number-heavy narration (see `video-script`).
- Do not speed up audio to hit a length; edit the text.
- Do not claim a domain fact the narration states (for example UPI settlement details) is verified unless it was checked against primary documentation.

## Folder layout per topic
```
<topic>/
  narration.json   timing.json   tts.py   img.py   otio_build.py
  audio/  keyframes/  music/  build/
  hf/             # Hyperframes project: index.html, assets/{voice.wav,music.wav,images}
```
Final video is copied to the project root as `How_<Topic>_Works.mp4`.
