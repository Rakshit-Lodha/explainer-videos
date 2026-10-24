# Explainer-video workflow

This folder produces short narrated explainer videos (9:16, 1080x1920, 60-90 s, hard ceiling 4 minutes) in a dark-navy, amber-and-teal motion-graphics style. The first finished example is `upi/` (`How_UPI_Works.mp4`); follow its layout for new topics.

## AI from Scratch course
Work in `ai-course/` follows `ai-course/course.md` (objective, learner profile, lesson format, pipeline and status). Read it first; it overrides the 9:16 defaults above for that course.

## Skills to load, in order
Load each skill with the Skill tool at the step that needs it, not all up front.

| Step | Skill | What it covers |
|---|---|---|
| 1. Script | `video-script` | Scene beats, professorial narration, approval gate. |
| 2. Voice | `sarvam-voice` | Sarvam Ratan TTS, per-scene emotion settings, timed voice track. |
| 3. Visuals | `/hyperframes` (shipped inside each Hyperframes project, see `<topic>/hf/AGENTS.md`) | Composition authoring, check, snapshot, render. |

If a Hyperframes skill is missing, run `npx hyperframes@0.8.118 skills update <name>`.

## Pipeline
1. **Script.** Write it with `video-script`, show it to the user, and wait for an explicit approval. Do not generate anything before that.
2. **Voice.** Sarvam only (`SARVAM_API_KEY`, `sarvam-voice`): `narration.json` to `audio/<id>.wav` to `hf/assets/voice.wav` and `timing.json`. This fixes every scene's start time and duration; anchor the composition's beats to its sentence times. Do not use ElevenLabs.
3. **Keyframes and reference images.** `gpt-image-2.5-sunburst-2026-09-08` via `POST /v1/images/generations` (size `1024x1536`, response `b64_json`). First generate a style reference sheet, then the scene plates, always with the same style prefix (dark navy `#0a1020`, amber `#f5b942`, teal `#4fd1c5`, flat vector, no text, bloom). Use images only where illustration earns its place (e.g. an opening scene plate); diagrams are drawn in HTML.
4. **Motion graphics.** One Hyperframes composition, `hf/index.html`, one paused GSAP timeline, scene start times taken from `timing.json`.
5. **Animatic.** `render --quality draft` with the voice; show the user stills (`snapshot --at ...`) or the file and fix issues before the final render.
6. **Timeline record.** Build an OpenTimelineIO file (`otio_build.py`, output `build/<topic>.otio`) from `timing.json`: video track of scenes and voice track. It documents the edit; the render itself is driven by Hyperframes.
7. **Final render and master.** `render --quality delivery`, then one ffmpeg pass: `-c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=7 -c:a aac -b:a 192k -movflags +faststart`. Verify with `ffprobe` (1080x1920, duration) and sample frames.

## Environment
- Project root `/Users/rakshitlodha/Desktop/Videos`; keys in `.env`: `SARVAM_API_KEY`, `OPENAI_API_KEY`, `FAL_AI`, `GEMINI_API_KEY`. Never print or commit them.
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
- No background music: the voice is the only audio track. Do not add Suno or any other music, and do not put a music file in `hf/assets/`.
- No ElevenLabs narration; voice is always Sarvam.
- Do not speed up audio to hit a length; edit the text.
- Do not claim a domain fact the narration states (for example UPI settlement details) is verified unless it was checked against primary documentation.

## Folder layout per topic
```
<topic>/
  narration.json   timing.json   tts.py   img.py   otio_build.py
  audio/  keyframes/  build/
  hf/             # Hyperframes project: index.html, assets/{voice.wav,images}
```
Final video is copied to the project root as `How_<Topic>_Works.mp4`.
