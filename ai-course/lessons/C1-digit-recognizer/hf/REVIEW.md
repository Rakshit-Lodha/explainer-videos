# Review: C1 Digit recognizer: a NumPy MLP on MNIST

- Creative call: this capstone had no WIP snapshot, so the script, `lesson.json` and composition were written new. Visuals are built from the same 8×8 digit glyphs the exercises generate: a wall of noisy digits, flattening, one-hot labels and the train/validation split, the 784→128→10 perceptron with softmax bars, (p − y)/B as bar groups beside the backward-pass code, the training loop with a sketched accuracy curve, an illustrative confusion matrix (4↔9, 3↔5, unusual 7s), and browser against real MNIST. Because Pyodide cannot download MNIST, the problems use a deterministic synthetic 8×8 digit set: data prep, a two-layer MLP with a numerically checked backward pass, and a training loop that must exceed 97% validation accuracy (the reference reaches 98.3% in under a second).
- Measured: checker OK (prep 3/3, mlp 3/3, train 2/2); Hyperframes check passed with 0 errors and 0 warnings; the delivery master is 1920x1080 at 30 fps and 202.9 seconds. Audio was measured and normalized, not listened to.
- Looked at: twelve composition snapshots, a re-snapshot after the repair, and three frames sampled from the master.
- Repairs: the synthetic digits were made slightly less noisy (σ 0.25 → 0.2) and the training defaults raised (20 epochs, lr 0.5) so the 97% target is reliable; the large example glyph in S2 is drawn clean and unshifted so it reads clearly as a 3.
- Weakest shot: the accuracy curve and confusion matrix are labelled sketches, not measured MNIST results.
- Kept warnings: none.
