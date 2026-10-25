# Review: C2 Tiny GPT: a character-level transformer

- Creative call: this capstone had no WIP snapshot, so the script, `lesson.json` and composition were written new. The video moves from the course GPT writing noise, to a text corpus encoded as integer ids, the train/validation split, input and target windows shifted by one, (B, T, V) logits scored by cross-entropy with L₀ ≈ ln V, the training loop with sketched train and validation curves, a bigram table against a transformer, invented sample texts showing the progression from symbols to dialogue, and the whole path of the course as a closing diagram. The browser problems build next-character batches, the sequence cross-entropy, and a trained bigram model with sampling. A PyTorch script that trains the full tiny GPT locally or in Colab is included in the third problem as optional reading; it was syntax-checked but not run, because PyTorch is not installed here.
- Measured: checker OK (batches 3/3, seq-loss 3/3, bigram 3/3); Hyperframes check passed with 0 errors and 0 warnings; the delivery master is 1920x1080 at 30 fps and 202.1 seconds. Audio was measured and normalized, not listened to.
- Looked at: twelve composition snapshots and three frames sampled from the master.
- Repairs: the corpus panel was widened after the checker reported clipped text, and the closing path diagram's arrow code was rewritten.
- Weakest shot: the loss curves are sketches and the sample texts are invented for illustration; both are labelled as such on screen.
- Kept warnings: none.
