# Copy-paste prompt for continuing the AI from Scratch build

Continue the "AI from Scratch" course build in `Rakshit-Lodha/explainer-videos`. You are the only builder. Work directly on `main`: fetch, check out `main`, and pull before changing anything. Commit and push after every finished lesson.

First read, in this order: `ai-course/STATUS.md`, `ai-course/course.md`, the root `CLAUDE.md`, `ai-course/README.md`, and `ai-course/wip/README.md`. The status file is the live handoff and records the exact finished count, environment, gotchas, and unverified claims. Study `lessons/1.1-vectors/` and `lessons/1.3-matrices/` as reference lessons. Before each new lesson, inspect the finished lesson immediately before it so the problem progression and visual language remain consistent. Read every file in a WIP snapshot before trusting it.

Resume at lesson **6.8-normalization** and continue strictly in course order: 6.8, 6.9, 7.1-7.4, 8.1-8.4, 9.6-9.10, 12.1-12.3, C1, C2. Do not rebuild finished lessons. Move each part-built folder from `ai-course/wip/` into `ai-course/lessons/` and continue from its first missing pipeline step. Lessons 9.10, C1 and C2 must be created from scratch.

Follow `course.md` exactly. Scripts are pre-approved. Use Sarvam `bulbul:v3` with tools default speaker Priya; never add a speaker field. Regenerate TTS and alignment for every WIP lesson. Do not print or commit the repo-root `.env`. Problems run in browser Pyodide with NumPy and must be self-contained. Module 6 extends the working autograd `Value` implementation from the previous lesson; module 9 extends the previous lesson's working NumPy GPT forward pass. Run Hyperframes `0.8.118` check until there are zero errors, take snapshots and visually inspect them, render at delivery quality, master with the exact ffmpeg command in `course.md`, then run `otio_build.py`, `site_video.py`, and `build_site.py`.

A lesson is finished only when its folder is in `lessons/`, `python3 tools/check_lesson.py lessons/<id>` prints `OK`, and `site/videos/<id>.mp4` exists. Add a short `hf/REVIEW.md`, record narration claims not verified against a primary source in `STATUS.md`, remove the corresponding WIP folder, stage the lesson folder, site MP4/JPG and `site/data/`, commit, and push to `origin main` before starting the next lesson.

When all 81 lessons are complete, rebuild the site, serve `ai-course/site` locally, verify the home page lists all 81 lessons, verify a lesson page plays video and runs a code problem, empty `ai-course/wip/` except its README, update `STATUS.md`, then commit and push `main`.
