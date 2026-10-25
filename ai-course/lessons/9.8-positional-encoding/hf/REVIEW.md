# Review: 9.8 Positional encoding

- Creative call: the WIP composition and `lesson.json` were complete and were kept as they were. The video moves from "dog bites man" against "man bites dog" producing the same shuffled vectors, to token plus position vectors, a learned position table and its length limit, sinusoidal waves read like clock hands, rotation by a fixed angle (with a RoPE note), and the GPT input x_t = E[token] + P[t]. TTS and alignment were regenerated in Priya.
- Measured: checker OK (shapes 6/6, sinusoidal 5/5, inputs 5/5); Hyperframes check passed with 0 errors and 1 warning; the delivery master is 1920x1080 at 30 fps and 182.8 seconds. Audio was measured and normalized, not listened to.
- Looked at: twelve composition snapshots and three frames sampled from the master. No repairs were needed.
- Kept warnings: one `gsap_callback_dom_measurement` from a shared helper; it did not affect the render.
