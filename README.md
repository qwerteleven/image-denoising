# 🖼️ Image Denoising — Comparison of Classical Methods

Research and evaluation project of classic image denoising algorithms applied to real datasets of hotel photographs. State-of-the-art methods are compared in terms of reconstruction quality using industry-standard metrics.

---

## What problem does it solve?

Digital images captured by camera sensors always contain image noise: random variations in color or brightness that degrade visual quality. This occurs especially in low-light conditions, with low-cost sensors, or with aggressive compression.

The goal is to recover the original clean image from a noisy image, a process known as denoising. This repository implements, runs, and evaluates three classic methods on its own dataset of hotel images (Radisson and Anfi).

---

## Implemented Methods

### BM3D — 3D Block-Matching
[`scripts/bm3d.py`](scripts/bm3d.py) · [`scripts/bm3d_gpu.py`](scripts/bm3d_gpu.py)

[BM3D](https://en.wikipedia.org/wiki/Block-matching_and_3D_filtering) has been the benchmark algorithm for denoising for over a decade. It operates in two phases:

1. **Block-Matching**: groups similar blocks of the image into 3D stacks.

2. **Collaborative Filtering**: Applies a transform to the 3D domain (typically a Discrete Cosine Transform [DCT](https://en.wikipedia.org/wiki/Discrete_cosine_transform) or Bior wavelets [https://en.wikipedia.org/wiki/Biorthogonal_wavelet]) and noise thresholding.

3. **Wiener Aggregation**: A second pass refines the estimate using the output of the first pass as a reference.

The GPU version (`bm3d_gpu.py`) allows exploring the effect of the sigma parameter over a continuous range (1–40), generating results by noise level.

```python
sigma = (1, 40) # range of noise levels explored
```

---

### DCT Denoising
[`scripts/DCTdenoising.py`](scripts/DCTdenoising.py)

A method based on local filtering in the Discrete Cosine Transform (DCT) domain. It divides the image into blocks, transforms them into the frequency space, and suppresses the corresponding noise coefficients using soft or hard thresholding.

It is simpler than BM3D but computationally efficient and produces solid baseline results.


```python
sigma = 20 # assumed noise level (standard deviation of Gaussian noise)
```

---

### NLM (Non-Local Means with Patch)
[`scripts/nlmp.py`](scripts/nlmp.py)

[Non-Local Means](https://en.wikipedia.org/wiki/Non-local_means) is an algorithm that exploits the **non-local redundancy** of the image: instead of filtering only with neighboring pixels, it searches the entire image for similar patches and averages them using a weighted average.

The `nlmp` (Non-Local Means with Patch) variant extends this idea by using larger patches for greater robustness to noise.


```python
# The noisy signal is used both as a reference and as a filtering input
NLMeansP input.png sigma 0 input.png output.png
```

---

## Evaluation Metrics

[`scripts/evaluate_method.py`](scripts/evaluate_method.py)

Two standard metrics are used in image processing:

### PSNR — Peak Signal-to-Noise Ratio
[Peak Signal-to-Noise Ratio](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio): measures the ratio between the maximum possible signal and the residual noise. It is expressed in decibels (dB). Higher values ​​= better reconstruction.

```
PSNR = 20 · log₁₀(255 / √MSE)
```

A PSNR > 40 dB is considered excellent. The results in this dataset range from 33–44 dB.

### SSIM — Structural Similarity Index
[Structural Similarity Index](https://en.wikipedia.org/wiki/Structural_similarity): measures the perceptual similarity between images, taking into account luminance, contrast, and structure. It ranges from 0 to 1 (1 = identical image).

Unlike PSNR (based on pixel-by-pixel MSE), SSIM correlates better with human perception of quality.

---

## Results

### Sigma Visualization

Exploring the effect of sigma noise level on the denoised image (BM3D GPU):

![Sigma visualization](https://github.com/qwerteleven/image-denoising/blob/main/assets/sigma_visualization.png)

---

### Visual Comparison of Methods

| Method | Example |

|--------|---------|
| Original | ![original](https://github.com/qwerteleven/image-denoising/blob/main/assets/original.png) |
| BM3D | ![bm3d](https://github.com/qwerteleven/image-denoising/blob/main/assets/bm3d.png) |
| DCT Denoising | ![dct](https://github.com/qwerteleven/image-denoising/blob/main/assets/DCTdenoising.png) |
| NLM with Patch | ![nlmp](https://github.com/qwerteleven/image-denoising/blob/main/assets/nlmp.png) |

---

### Quantitative metrics (PSNR/SSIM)

| DCT Denoising | NLM with Patch |
|---|---|
| ![DCT metrics](https://github.com/qwerteleven/image-denoising/blob/main/assets/DCTdenoising.json.png) | ![NLM metrics](https://github.com/qwerteleven/image-denoising/blob/main/assets/nlmp.json.png) |

**Statistical summary** (on 57 images from the `radisson` and `anfi` datasets):

| Method | Average PSNR (dB) | Medium SSIM |
|--------|----------------|-------------|
| DCT Denoising | ~35.2 | ~0.874 |
| NLM with Patch | ~33.4 | ~0.814 |

DCT Denoising consistently outperforms NLM in both metrics on this dataset.

---

## Project Structure

```
image-denoising/
├── scripts/
│ ├── bm3d.py # Classic BM3D (CPU)
│ ├── bm3d_gpu.py # BM3D with sigma scanning (GPU)
│ ├── DCTdenoising.py # DCT Denoising
│ ├── nlmp.py # Non-Local Means with Patch
│ ├── evaluate_method.py # Calculation of PSNR and SSIM
│ ├── data_explorer.py # Visualization of metrics
│ ├── show_img.py # Visual comparison by image
│ ├── show_sigma_img.py # Visualization of the sigma effect
│ └── change_file_extension.py # Format conversion utility
├── result_metadata/
│ ├── DCTdenoising.json # PSNR/SSIM results per image
│ └── nlmp.json
└── dataset/
├── radisson/ # Radisson hotel images
└── anfi/ # Anfi hotel images
```

---

## External Dependencies (IPOL)

The methods are executed on compiled binaries from IPOL (Image Processing On Line) (https://www.ipol.im/), a reference platform for image processing algorithms. reproducible:

- **BM3D**: `ipol_methods/bm3d/build/bm3d`
- **BM3D GPU**: `ipol_methods/bm3d-gpu/build/bm3d`
- **DCT Denoising**: `ipol_methods/DCTdenoising-master/build/dctdenoising`
- **NLM with Patch**: `ipol_methods/nlmp_1.2/NLMeansP`

---

## Quick use

```bash
# Run DCT Denoising on the dataset
python scripts/DCTdenoising.py

# Evaluate results (generates JSON with PSNR/SSIM)
python scripts/evaluate_method.py

# Explore results visually
python scripts/data_explorer.py

# See comparison for image index N
python scripts/show_img.py N
```

---

## Key concepts — References

| Concept | Wikipedia |
|----------|-----------|
| Noise in image | [Image noise](https://en.wikipedia.org/wiki/Image_noise) |
| BM3D | [Block-matching and 3D filtering](https://en.wikipedia.org/wiki/Block-matching_and_3D_filtering) |
| DCT Transform | [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) |
| Non-Local Means | [Non-local means](https://en.wikipedia.org/wiki/Non-local_means) |
| PSNR | [Peak signal-to-noise ratio](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio) |
| SSIM | [Structural similarity index](https://en.wikipedia.org/wiki/Structural_similarity) |
| Wavelets Bior | [Biorthogonal wavelet](https://en.wikipedia.org/wiki/Biorthogonal_wavelet) |
