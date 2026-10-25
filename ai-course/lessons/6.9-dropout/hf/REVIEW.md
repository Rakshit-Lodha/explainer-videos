# Review: 6.9 Dropout and generalization

- Creative call: the WIP storyline was kept. Diverging train and validation curves lead to a network with neurons switching off at random, the absent-colleague analogy, inverted-dropout bookkeeping on ten bars, an ensemble of thinned networks, before-and-after loss curves, and dropout rates in language models.
- Measured: Hyperframes check passed with 0 errors and 0 warnings; the delivery master is 1920x1080 at 30 fps and 179.6 seconds. Audio was measured and normalized, not listened to.
- Looked at: thirteen composition snapshots and two rounds of three frames sampled from the mastered MP4.
- Repairs: (1) S3 left the dropped bar at zero while the caption said everyone is present at test time; all ten bars now return to their plain value of 1.0 on "every neuron takes part". (2) The S5 legend promised dashed validation lines, but the draw-on helper overwrites the dash pattern; the legend now uses colour only and sits below the plots instead of over the right-hand curve. (3) The S1 "error on new examples" label was moved clear of its curve.
- Kept warnings: none.
