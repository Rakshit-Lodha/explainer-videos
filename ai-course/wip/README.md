# Work in progress (snapshot)

Copies of lesson folders that were part-way through the build when the snapshot was taken. The site ignores this folder; only `lessons/` is published.

To finish one, move it to `lessons/<id>/`, then follow `course.md` from whichever step is missing:
- No `lesson.json`: write the quiz and problems, then run `check_lesson.py`.
- `narration.json` but no `timing.json`: run `tts.py` and `voice.py`.
- No `hf/index.html`: write the composition.
- Everything present: check, snapshot, render, master, `otio_build.py`, `site_video.py`, `build_site.py`.

Audio, renders and vendored libraries are not included, so re-run `tts.py` (or reuse the takes if you have them) and `voice.py` before rendering; `voice.py` also copies `vendor/` into `hf/assets/lib`. Read every file before trusting it: a snapshot can catch a lesson mid-edit. Delete a folder here once its lesson lands in `lessons/`.
