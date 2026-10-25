# Review: 7.3 Reading loss curves

- Creative call: the WIP snapshot had narration only, so the composition and `lesson.json` were written new. The video goes from a healthy curve, to a noisy mini-batch curve with its moving average (the visible lag is real EMA behaviour), three learning-rate panels ending in NaN, training against validation with the early-stopping point, underfitting and plateau panels, three starting losses against the ln 10 line, and a language-model loss spike rolled back to a checkpoint. The problems are an exponential moving average, a starting-loss check and early stopping with patience.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings; contrast 41/41; the delivery master is 1920x1080 at 30 fps and 180.4 seconds. Audio was measured and normalized, not listened to.
- Looked at: thirteen composition snapshots, four re-snapshots after repairs, and three frames sampled from the master.
- Repairs: moved labels that collided with curves (NaN, "far below", the skip-the-batches caption, the training label on the axis) and widened the ln 10 formula, which had wrapped.
- Kept warnings: none.
