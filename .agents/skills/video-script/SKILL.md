---
name: video-script
description: Write a narrated explainer-video script (60-90 s, 9:16) as scene beats with narration, emotion tags and visual direction, then get user approval before any asset is generated. Use whenever the user asks for an explainer video, a script for one, or a new topic in the existing explainer style.
---

# Video script skill

Produces the single artifact everything downstream depends on: `<topic>/narration.json` plus a human-readable script the user approves. Nothing (TTS, images, motion graphics) is generated until the user says the script is approved. Approval has been refused twice in this project for scripts that were confusing or the wrong depth, so the confirmation step is not optional.

## Inputs to settle first
- Topic and the audience's starting point. Default audience: someone who is comfortable with technology but has never seen the internals.
- Target length. Default 60-90 s. Hard ceiling set by the user: 4 minutes; the style reference runs about 66 s.
- A style reference, if the user supplies one. Extract frames with `ffmpeg -vf "fps=1/4,scale=480:-1,tile=4x5"` and read the contact sheet; a social-media link usually cannot be fetched or played headlessly, so ask for the file.

## Structure that has worked
One continuous visual story where each scene hands its object to the next (waveform becomes spectrogram becomes stars; a payment message becomes a sealed capsule becomes a ledger). Roughly six scenes:
1. A concrete scene the viewer recognises, ending on the question the video answers.
2. The first abstraction (what the thing really is).
3 to 5. One mechanism per scene, each motivated by the limitation of the previous one.
6. A short payoff line and a visual "resolved" state.

Every scene gets: id (`s1`..), narration text, an emotion tag, a visual description, and which tool renders it.

## Voice of the narration
Write as a top-tier university lecturer speaking to curious adults: connected, flowing sentences that carry a reason ("because", "so that", "which is why"), precise vocabulary, a single clear idea per scene. Explain a technical term at the moment it is first needed, using a physical analogy, then use the term normally.

Avoid, because the user has rejected them explicitly:
- Staccato fragments and punchy one-line paragraphs.
- Dense numbers. Use a number only when the visual shows it.
- Slogan closers, "Here's the thing", "Let's dive in", rhetorical lists of three.
- Anything that sounds like a product ad.

Technical depth is a dial the user has moved both ways: "super confusing" for too much math at once, then "make it technical". Settle it by naming the mechanisms (alias directory, switch, PIN encryption, net settlement) and explaining each in one plain sentence, not by adding formulas.

## Length budgeting
Measure, do not guess. Generate the Sarvam audio for the draft, read durations with ffprobe, then trim or extend. In this project 286 words at Ratan's tuned pace came to 85 s, which is faster than the usual 150 words per minute.

## Output format shown to the user
For each scene: title with time range, bracketed emotion, one italic line of visual direction, then the narration in a block quote. Finish with a short list of build notes: tools per scene, what is being skipped and why, anything unverified. Ask for approval in one sentence.

## After approval
Write `narration.json` as a list of `{"id","pace","temperature","text"}` and hand off to the `sarvam-voice` skill. Fact-check any domain claims against primary documentation before locking the narration, and say so in the build notes if that has not been done.
