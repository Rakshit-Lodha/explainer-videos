# Explainer-video workflow

Claude Code skills and per-topic projects for short narrated explainer videos (9:16, 1080x1920, 60-90 s) in a dark-navy, amber-and-teal motion-graphics style. See [CLAUDE.md](CLAUDE.md) for the full pipeline.

## Skills
Located in `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex copy):

| Skill | Purpose |
|---|---|
| `video-script` | Scene beats, narration, emotion tags, approval gate |
| `sarvam-voice` | Sarvam Ratan TTS, per-scene takes, timed voice track |

Voice is always Sarvam, and videos have no background music. The `elevenlabs-voice` and `suno-music` skills remain in the folder from earlier videos but are not part of the pipeline.

Visuals are built with [Hyperframes](https://www.npmjs.com/package/hyperframes) (`npx -y hyperframes@0.8.118`).

## Topics
`upi/`, `suno/`, `greatwork/`, `festina/`, `hbp_trailer/`, `voxel-castle/`: scripts, narration, timing and Hyperframes compositions. Rendered media, audio and images are not committed; regenerate them with each topic's scripts.

## Setup
Create `.env` with `SARVAM_API_KEY`, `OPENAI_API_KEY`, `FAL_AI`, `GEMINI_API_KEY`. Python deps: `opentimelineio requests python-dotenv`.
