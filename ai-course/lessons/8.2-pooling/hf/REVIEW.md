# Review: 8.2 Pooling and feature hierarchies

- Creative call: the WIP snapshot had narration and an empty scaffold, so the composition and `lesson.json` were written new. The video goes from a pixel-exact feature map to "somewhere around here" and a compact pooled map, numbered max pooling with four coloured windows plus average pooling, a 9 wobbling inside one window while the max stays put, nested receptive-field squares on the input, a hierarchy of drawn tiles (edges, textures, parts and objects), stride-2 convolution and global average pooling, and a language-model layer stack with probing labels. The problems are pooling with lists, channel-wise pooling in NumPy, and a receptive-field calculator.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings (one info); the delivery master is 1920x1080 at 30 fps and 189.8 seconds. Audio was measured and normalized, not listened to.
- Looked at: twelve composition snapshots, re-snapshots after repairs, and three frames sampled from the master.
- Repairs: the moving 9 is marked as an intentional overlap of the cells beneath it; the edge tiles are drawn as SVG lines rather than CSS-rotated divs, which the checker misread as drifting rotations; the layer stack moved down to clear the "probing studies" label.
- Kept warnings: none.
