# AI from Scratch

A course of about 80 lessons, each with a 60-90 s 16:9 explainer video, a quiz and code problems. The plan is in `SYLLABUS.md`; `course.json` is the machine-readable outline.

## Standing approval
See `course.md` for the full brief. The user pre-approved lesson scripts for this course (2026-10-24): write each lesson's script and build it without waiting for sign-off. The rest of the pipeline in the root `CLAUDE.md` still applies (Sarvam voice, no music, Hyperframes).

## Per-lesson layout
```
lessons/<id>/
  narration.json   timing.json   lesson.json (quiz + problems)
  audio/  build/
  hf/              # Hyperframes project, 1920x1080
```

## Tools (run from `ai-course/`)
- `python tools/tts.py lessons/<id> [s1 ...]`: Sarvam takes per scene (needs `SARVAM_API_KEY`).
- `python tools/voice.py lessons/<id>`: builds `timing.json` and `hf/assets/voice.wav` from the takes (or a provisional word-count estimate with a silent track), copies `vendor/` into `hf/assets/lib`, and syncs scene timings into `hf/index.html`.
- `python tools/check_lesson.py lessons/<id>`: every solution passes its tests and every starter fails one.

`vendor/` holds GSAP 3.14.2 and KaTeX 0.16.11, because headless Chrome cannot reach CDNs from every environment.
