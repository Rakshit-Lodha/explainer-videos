# AI from Scratch: course plan (draft, awaiting approval)

Every lesson has three parts:

1. **Video** (60-90 s): 3Blue1Brown-style visual intuition. Dark background, one idea per video, equations that build up term by term, shapes that morph instead of cutting. Sarvam (Ratan) narration, no music.
2. **Quiz** (3-5 questions): multiple choice, numeric answers and "predict what happens next" questions. Each answer shows an explanation.
3. **Code problem** (1-2 per lesson): you fill in a Python function in the browser and it runs against hidden tests (Pyodide + NumPy, so nothing to install). The problems build on each other until you've written a neural network and a small GPT using only NumPy.

Pacing: about 80 lessons in 13 modules, roughly 15-25 minutes per lesson including the quiz and code.

## Module 0: Orientation (3)
0.1 What it means for a machine to "learn": fitting a function to data
0.2 The map of this course: math, then models, then transformers
0.3 Reading math notation: Σ, subscripts and vectors

## Module 1: Linear algebra (8)
1.1 Vectors: arrows and lists of numbers
1.2 Linear combinations, span and basis
1.3 Matrices as transformations of space
1.4 Matrix multiplication as composition
1.5 Determinant: how much area gets stretched
1.6 Dot product and projection (similarity)
1.7 Eigenvectors: directions that only stretch
1.8 SVD and PCA intuition (rotate, stretch, rotate)
Code: vector ops, matmul by hand, 2D transform of a point cloud, power iteration

## Module 2: Calculus (6)
2.1 Derivative: slope of a zoomed-in curve
2.2 Chain rule: rates multiply
2.3 Partial derivatives
2.4 The gradient points uphill
2.5 Jacobians: derivatives of vector functions
2.6 Linear approximation and Taylor series
Code: numerical derivative, gradient checker, chain rule on a composed function

## Module 3: Probability and information (7)
3.1 Random variables and distributions
3.2 Expectation and variance
3.3 Bayes' rule: updating beliefs
3.4 The Gaussian and why it's everywhere
3.5 Maximum likelihood
3.6 Entropy: measuring surprise
3.7 Cross-entropy and KL divergence (the loss behind LLMs)
Code: sampling and histograms, Bayes calculator, MLE of a Gaussian, cross-entropy function

## Module 4: Optimization (6)
4.1 A loss function is a landscape
4.2 Gradient descent: roll downhill
4.3 Learning rate: too small, too big, just right
4.4 Stochastic and mini-batch gradient descent
4.5 Momentum and Adam
4.6 Convex vs non-convex landscapes
Code: implement GD, SGD, momentum and Adam on a 2D bowl and on Rosenbrock

## Module 5: Classical machine learning (9)
5.1 Linear regression as projection
5.2 Logistic regression and the sigmoid
5.3 Overfitting and the bias-variance trade-off
5.4 Regularization (L1, L2)
5.5 Train, validation and test splits
5.6 k-nearest neighbours
5.7 Decision trees
5.8 k-means clustering
5.9 PCA in practice
Code: linear and logistic regression from scratch, k-means, PCA on a toy dataset

## Module 6: Neural networks (9)
6.1 The neuron: weighted sum plus a bend
6.2 Layers: stacking transformations
6.3 Activation functions (ReLU, GELU, why not linear)
6.4 Why depth helps
6.5 Forward pass as a computational graph
6.6 Backpropagation: the chain rule run backwards
6.7 Initialization and vanishing gradients
6.8 Normalization (batch norm, layer norm)
6.9 Dropout and generalization
Code: write a tiny autograd engine, then a 2-layer MLP that learns a spiral dataset

## Module 7: Training in practice (4)
7.1 Tensors and batches
7.2 The training loop
7.3 Reading loss curves
7.4 Debugging a model that won't learn
Code: train an MLP on MNIST digits with NumPy; optional PyTorch notebook (Colab)

## Module 8: Convolutional networks (4)
8.1 Convolution: a sliding pattern detector
8.2 Pooling and feature hierarchies
8.3 CNN architecture end to end
8.4 Residual connections
Code: 2D convolution by hand, edge-detector kernels, a tiny CNN forward pass

## Module 9: Sequences and transformers (10)
9.1 Tokens: turning text into numbers
9.2 Embeddings: meaning as direction
9.3 RNNs and why they struggled
9.4 Attention: which words should look at which
9.5 Queries, keys and values
9.6 Softmax and scaled dot-product attention
9.7 Multi-head attention
9.8 Positional encoding
9.9 The transformer block
9.10 Predicting the next token and sampling (temperature, top-k)
Code: BPE tokenizer, attention from scratch, a character-level GPT forward pass

## Module 10: Large language models (7)
10.1 Pretraining and scaling laws
10.2 Fine-tuning and instruction tuning
10.3 Learning from human preferences (RLHF, DPO)
10.4 Context windows and the KV cache
10.5 Retrieval-augmented generation
10.6 Tool use and agents
10.7 Evaluating models
Code: KV cache, cosine-similarity retrieval, a minimal tool-calling loop

## Module 11: Generative models (3)
11.1 Autoencoders and VAEs
11.2 Diffusion: learning to remove noise
11.3 GANs in brief
Code: forward noising process, a 1D denoiser

## Module 12: Reinforcement learning (3)
12.1 Agents, rewards and Markov decision processes
12.2 Q-learning
12.3 Policy gradients
Code: Q-learning on a gridworld

## Capstones
- C1 Digit recognizer: NumPy MLP on MNIST, above 97% accuracy
- C2 Tiny GPT: train a character-level transformer on a small text corpus (Colab notebook, PyTorch)

## Delivery
- `ai-course/site/`: a static course site with a lesson list, progress tracking, video player, quiz engine and in-browser Python (Pyodide). It can be hosted on GitHub Pages or Vercel.
- `ai-course/lessons/<module>.<lesson>-<slug>/`: each lesson's `narration.json`, `timing.json`, `hf/` composition, `quiz.json` and `problems/*.py` with tests, following the per-topic layout in `CLAUDE.md`.
