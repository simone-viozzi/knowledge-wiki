# Noise2Noise

If the noise of some images is zero-mean, than is possible to train a de-noise NN with only noisy images.

The training is structured using pairs of noisy images, the loss is chosen based on the specific task and can be L2, L1 or L0. During the training the loss will not decrease, the task of transforming one noise to another is impossible, but the network will still learn how to de-noise images.
