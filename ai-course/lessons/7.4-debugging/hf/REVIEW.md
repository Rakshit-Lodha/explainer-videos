# Review: 7.4 Debugging a model that won't learn

- Creative call: the WIP snapshot had narration only, so the composition and `lesson.json` were written new. A six-item checklist runs down the left of every scene, ticking off as the lesson goes. The scenes show a flat loss with random knob-turning, mismatched image/label pairs after a separate shuffle, raw against scaled value ranges, the ln C start and the overfit-one-batch test, a central-difference secant against the analytic tangent, NaN causes, vanishing and exploding per-layer gradient bars, a dead ReLU layer, three silent-bug cards and small-to-full-scale runs. The problems are a numerical gradient check and a "fix the three silent bugs" training function.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings; contrast 101/101; the delivery master is 1920x1080 at 30 fps and 191.2 seconds. Audio was measured and normalized, not listened to.
- Looked at: thirteen composition snapshots, three re-snapshots after repairs, and three frames sampled from the master.
- Repairs: moved the "loss L(w)" label off its curve, spread the NaN-cause chips, put the gradient-bar title below the bars so the exploding bars cannot cover it, and moved the run-size labels outside the nested squares.
- Kept warnings: none.
