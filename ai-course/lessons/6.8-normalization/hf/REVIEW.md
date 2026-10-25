# Review: 6.8 Normalization

- Creative call: the WIP storyline was kept. A drifting distribution is pulled into a standard band, then grading on a curve becomes the formula, then batch norm (columns) and layer norm (rows) on the same grid, a rough-versus-smooth loss landscape, and a pre-norm transformer block with RMSNorm.
- Measured: Hyperframes check passed with 0 errors and 2 lint warnings; contrast passed 94/94; the delivery master is 1920x1080 at 30 fps and 189.8 seconds. Audio was measured and normalized, not listened to.
- Looked at: thirteen composition snapshots and three frames sampled from the mastered MP4.
- Repair: in S6 the GPT-2 pre-norm note now sits above the RMSNorm formula, so the text reads in the order the narration speaks it.
- Kept warnings: two `gsap_callback_dom_measurement` warnings come from the shared `mkArrow`/`morphF` helpers, which this lesson does not call to measure anything at seek time.
