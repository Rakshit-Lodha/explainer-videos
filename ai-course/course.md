# AI from Scratch: course brief

Every session and sub-agent working on this course reads this file first and follows it. When this file disagrees with a general default, this file wins. The root `CLAUDE.md` pipeline rules (Sarvam voice, no music, Hyperframes, no generated video) still apply.

## Objective
Teach Rakshit AI from first principles, math included, until he can explain and implement the path from text to tokens, embeddings, attention, transformer blocks, logits, loss, backpropagation, training and generation. Each lesson pairs one idea with something he builds. The course is personal: it is shaped around this one learner, not a general audience.

## The learner
- **Python:** comfortable beginner to intermediate. In code he writes by hand (`2.0/Basics.ipynb`, `learning-ml/Learn.ipynb`, `zero-to-hero-python`), he writes functions, loops and list comprehensions, and turns formulas into code: norm, normalisation, dot product, cosine similarity, closed-form linear regression. Larger apps (agents, RAG, Streamlit, FastAPI) were built with AI help. He calls himself a vibe coder.
- **Gaps seen in his code:**
  - He misreads Σ notation: `sum_xy` was a nested loop instead of `zip`.
  - Exception syntax: `raise("Value error")`.
  - Dividing by a list.
  - NumPy shapes and broadcasting are not yet solid.
- **Already knows:** vectors, vector addition and scaling, norm, dot product, cosine similarity, basic NumPy, and LLM applications (prompts, embeddings APIs, RAG, agents, tools, memory, voice, evals).
- **Where he stalled before:** matrices as transformations (Week 2 of `getting-deeper-with-ml/ml-math-foundations-plan.md`).
- **How he learns:** pure math without building loses his attention, so every lesson ends in code. His time is about 4-6 hours a week (demanding job plus weekend MBA), so lessons must be resumable and never assume a daily streak. His own rule is to write the first attempt himself, so solutions stay hidden until he asks for them.
- **Start date:** 2026-10-25.

## Lesson format (every lesson)
1. **Video:** 60-90 s, 16:9 at 1920x1080. Style inspired by 3Blue1Brown without copying its branding or mascot:
   - near-black background `#0e1116` with a blue number-plane grid;
   - vectors in blue `#58c4dd` and yellow `#f5cf4a`, x/î in green `#83c167`, y/ĵ in red `#fc6255`, sums in pink `#e77fb3`;
   - math typeset with KaTeX; Newsreader for text, JetBrains Mono for numbers;
   - shapes morph rather than cut, and one idea per video;
   - a corner tag `AI FROM SCRATCH · <num> <title>`, and the last scene names the next lesson.
2. **Narration:** university-lecturer voice in flowing sentences that carry reasons, with a technical term explained by a physical analogy the moment it first appears.
   - Avoid: staccato lines, dense numbers, slogans, "let's dive in", lists of three, and anything ad-like.
   - Use: Sarvam Ratan voice (bulbul:v3), one take per scene; no music.
3. **Quiz:** 4-5 multiple-choice questions, each with an explanation. Include at least one "predict the result" question and one question that links the idea to LLMs. The quiz doubles as a test-out for lessons he already knows.
4. **Code problems:** 1-3 per lesson, run in the browser (Pyodide plus NumPy).
   - Starter code has `TODO`s, tests explain *why* an answer failed, hints unlock one at a time, and the solution is hidden behind an explicit reveal.
   - Problems start with plain Python lists and move to NumPy only once the idea is clear. Over the course they build on each other into his own autograd engine, a NumPy MLP and a small GPT.
   - Add shape-prediction drills before attention.
5. **LLM link:** one or two sentences connecting the lesson to how language models work.

## Standing approval
The user pre-approved all lesson scripts (2026-10-24): write and build each lesson without waiting for sign-off. Still report what was built, and flag any domain claim that has not been checked against a primary source.

## Curriculum
The full list is in `SYLLABUS.md`, and `course.json` is the machine-readable outline: 81 lessons in 14 modules, from Orientation (0.1-0.3) through Reinforcement learning (12.x) and two capstones. Lesson 0.3, "Reading math notation", was added for his Σ gap. Build in order. Modules 1-3 should move faster through what he already knows, and lessons on matrices as transformations (1.3, 1.4) deserve extra care because that is where he stalled before.

## Build pipeline (per lesson)
Folder `lessons/<num>-<slug>/`, following the layout of `lessons/1.1-vectors/`, which is the reference lesson. Run from `ai-course/`:
1. Write `narration.json` (6 scenes, about 250-290 words in total).
2. Write `lesson.json` (summary, key ideas, LLM link, quiz, problems), then run `python tools/check_lesson.py lessons/<id>`. It must print OK: every solution passes all tests and every starter fails at least one.
3. Generate takes with `python tools/tts.py lessons/<id>`, which needs `SARVAM_API_KEY` and network access to `api.sarvam.ai`. Without the key, skip this step and keep the provisional timing.
4. Run `python tools/voice.py lessons/<id>`. It writes `timing.json` and `hf/assets/voice.wav` (from the takes, or a silent track with estimated timing), copies `vendor/` libraries into `hf/assets/lib`, and syncs scene times into `hf/index.html`.
5. Write the composition in `hf/index.html`, reusing the helpers from 1.1: `at(sid, fraction)`, `mkArrow`, `arrowTo`, `colvec`, `cellHL` and `place`. Place beats at fractions of each scene so they survive re-timing. Load libraries from `assets/lib/` only, never a CDN.
6. In `hf/`, run `npx -y hyperframes@0.8.118 check` until it passes. Then run `snapshot --at ...` and read the contact sheets for overlaps, stray elements and text on top of arrows.
7. Render with `render --quality delivery`, then master with ffmpeg: `-c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=7 -c:a aac -b:a 192k -movflags +faststart`. Verify the result with ffprobe and sample frames.
8. Commit and push to the session's working branch. Never commit keys, audio or video.

## Course site (still to build)
A static site in `site/`:
- a lesson list showing the full syllabus, with lessons not yet built marked "coming soon";
- per lesson: a 16:9 video player, the key ideas, the LLM link, the quiz and the code problems;
- a code editor with Run tests, hints and a solution reveal;
- progress saved in the browser.

Publish it as a private claude.ai artifact. Inside the artifact the page cannot fetch from CDNs, so Pyodide 0.26.4 core and the numpy 1.26.4 wheel must be published as files next to the page, loaded lazily when he first clicks Run. Outside the artifact, fall back to `https://cdn.jsdelivr.net/pyodide/v0.26.4/full/`. If Python cannot start, show a clear message and a button that copies the code.

## Status (2026-10-24)
- **Done:**
  - lesson 1.1 composition (check passes, frames reviewed), `lesson.json` (5 quiz questions, 3 problems, checker OK), and provisional timing;
  - shared tools in `tools/` and vendored GSAP and KaTeX.
- **Next:**
  1. Generate the Sarvam voice for 1.1, re-time it and render the final video.
  2. Build and publish the course site.
  3. Build lessons 0.1-0.3, then Module 1 onward.

## Rules for sub-agents
- Read this file and `lessons/1.1-vectors/` before building a lesson.
- Do not print, log or commit any key.
- Do not change the visual style, voice or lesson format without the user's say-so.
- Keep each lesson self-contained in its folder, and report anything skipped or unverified.
