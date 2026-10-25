# Review: 7.2 The training loop

- Creative call: the WIP snapshot had narration only, so the composition and `lesson.json` were written new. The video moves from a four-step loop with a token circling it, to a forward pass ending in one loss number, a backward pass with W and ∂L/∂W side by side, the update rule beside a five-line PyTorch loop with `zero_grad` highlighted, shuffled mini-batches making an epoch, a loss chart with validation dots and checkpoints, and next-token targets shifted by one. The problems train a line with plain lists, then logistic regression with shuffled mini-batches in NumPy.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings; contrast 60/60; the delivery master is 1920x1080 at 30 fps and 177.3 seconds. Audio was measured and normalized, not listened to.
- Looked at: fourteen composition snapshots, a zoomed snapshot of the code panel, and five frames sampled from the masters.
- Repairs: (1) target tokens in S7 drifted off their slots when shifted, so each token now sits in a fixed-width slot that moves instead. (2) The first master showed the `zero_grad` highlight straddling two code lines; it was moved down one line and the lesson re-rendered.
- Kept warnings: none. The narration says the loop runs for "tens or hundreds of thousands of steps"; the on-screen chip says only "a very large number of steps".
