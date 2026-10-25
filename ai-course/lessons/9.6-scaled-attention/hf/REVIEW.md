# Review: 9.6 Softmax and scaled dot-product attention

- Creative call: the WIP composition and `lesson.json` were complete and were kept as they were. The video moves from the paper's formula, to softmax tables (shift invariance, overflow and subtracting the max), a temperature sweep, the spread of q·k growing with √d_k and dividing it away, next-token training with a covering card, the −∞ mask producing a lower-triangular weight table, the five steps with code, and three heads as a bridge to 9.7. TTS and alignment were regenerated in Priya.
- Measured: checker OK (softmax 5/5, spread 3/3, causal 5/5); Hyperframes check passed with 0 errors and 1 warning; the delivery master is 1920x1080 at 30 fps and 249.9 seconds. Audio was measured and normalized, not listened to.
- Looked at: fifteen composition snapshots and three frames sampled from the master. No repairs were needed.
- Kept warnings: `composition_file_too_large` (322 lines); splitting the file would not change the render.
