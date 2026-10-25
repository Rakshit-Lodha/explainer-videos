# Review: 12.3 Policy gradients

- Creative call: the WIP snapshot had narration only, so the composition and `lesson.json` were written new. The video moves from Q-learning against direct policy adjustment (action bars rising and falling), to a policy network with softmax and the problem that sampling has no derivative, the log-derivative identity and the REINFORCE loop (Williams, 1992), onehot(a) − p as three bar groups, returns against advantages drawn as arrows, the PPO clipped objective with its ε band, and RLHF drawn as a policy-gradient loop with a KL leash. The problems are the softmax log-probability gradient (checked numerically), REINFORCE with a baseline on a three-armed bandit, and the PPO clipped objective.
- Measured: checker OK; Hyperframes check passed with 0 errors and 0 warnings; the delivery master is 1920x1080 at 30 fps and 196.5 seconds. Audio was measured and normalized, not listened to.
- Looked at: eleven composition snapshots, re-snapshots after repairs, and three frames sampled from the master.
- Repairs: the S4 group titles moved above the bars, the S5 baseline label moved right of the arrows, and the PPO note moved below the clipped line.
- Weakest shot: the S5 baseline label ends close to the right edge of the frame; it is fully legible but tight.
- Kept warnings: none.
