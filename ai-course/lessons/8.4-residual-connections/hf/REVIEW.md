# Review: 8.4 Residual connections

- Creative call: the WIP snapshot had narration and an empty scaffold, so the composition and `lesson.json` were written new. The video goes from shallow against deeper stacks and the 20- against 56-layer training-error curves, to a bottom-up residual block with its shortcut and y = x + F(x), a tracked-changes document analogy, F = 0 passing x through, a gradient taking the shortcut (thick) and the layers (fading), a 1×1-conv projection fixing mismatched shapes, a hundred-layer and a thousand-layer stack, the residual stream with alternating attention and feed-forward blocks writing into it, and a recap. The problems compare gradients through plain and residual chains, then build a NumPy residual block with a projection.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings; the delivery master is 1920x1080 at 30 fps and 177.6 seconds. Audio was measured and normalized, not listened to.
- Looked at: ten composition snapshots, re-snapshots after repairs, and three frames sampled from the master.
- Repairs: the S4 shape labels moved above their slabs so the shortcut line no longer runs through them, and the S7 block moved up to clear the next-lesson caption.
- Kept warnings: none.
