# 🖼️ Image Denoising — Comparativa de Métodos Clásicos

Proyecto de investigación y evaluación de algoritmos clásicos de **eliminación de ruido en imágenes** ([image denoising](https://en.wikipedia.org/wiki/Image_noise)), aplicados sobre datasets reales de fotografías de hotel. Se comparan métodos del estado del arte en términos de calidad de reconstrucción usando métricas estándar de la industria.

---

## ¿Qué problema resuelve?

Las imágenes digitales capturadas por sensores de cámara siempre contienen [ruido](https://en.wikipedia.org/wiki/Image_noise): variaciones aleatorias en el color o la luminosidad que degradan la calidad visual. Esto ocurre especialmente en condiciones de poca luz, sensores de bajo costo o compresión agresiva.

El objetivo es recuperar la imagen original limpia a partir de una imagen ruidosa, proceso conocido como **denoising**. Este repositorio implementa, ejecuta y evalúa tres métodos clásicos sobre un dataset propio de imágenes de hoteles (`radisson` y `anfi`).

---

## Métodos implementados

### BM3D — Block-Matching 3D
[`scripts/bm3d.py`](scripts/bm3d.py) · [`scripts/bm3d_gpu.py`](scripts/bm3d_gpu.py)

[BM3D](https://en.wikipedia.org/wiki/Block-matching_and_3D_filtering) es el algoritmo de referencia en denoising durante más de una década. Su funcionamiento en dos fases:

1. **Block-Matching**: agrupa bloques similares de la imagen en pilas 3D.
2. **Filtrado colaborativo**: aplica una transformada en el dominio 3D (típicamente [DCT](https://en.wikipedia.org/wiki/Discrete_cosine_transform) o [wavelets Bior](https://en.wikipedia.org/wiki/Biorthogonal_wavelet)) y umbralización del ruido.
3. **Agregación Wiener**: una segunda pasada refina la estimación usando la salida de la primera como referencia.

La versión GPU (`bm3d_gpu.py`) permite explorar el efecto del parámetro sigma en un rango continuo (1–40), generando resultados por nivel de ruido.

```python
sigma = (1, 40)  # rango de niveles de ruido explorados
```

---

### DCT Denoising
[`scripts/DCTdenoising.py`](scripts/DCTdenoising.py)

Método basado en filtrado local en el dominio de la [Transformada Discreta del Coseno (DCT)](https://en.wikipedia.org/wiki/Discrete_cosine_transform). Divide la imagen en bloques, los transforma al espacio frecuencial y suprime los coeficientes correspondientes al ruido mediante umbralización suave o dura.

Es más simple que BM3D pero computacionalmente eficiente y produce resultados sólidos como baseline.

```python
sigma = 20  # nivel de ruido asumido (desviación estándar del ruido gaussiano)
```

---

### NLM (Non-Local Means with Patch)
[`scripts/nlmp.py`](scripts/nlmp.py)

[Non-Local Means](https://en.wikipedia.org/wiki/Non-local_means) es un algoritmo que explota la **redundancia no local** de la imagen: en lugar de filtrar solo con píxeles vecinos, busca en toda la imagen parches similares y los promedia ponderadamente.

La variante `nlmp` (Non-Local Means with Patch) extiende esta idea usando parches más grandes para mayor robustez al ruido.

```python
# La señal ruidosa se usa tanto como referencia como entrada de filtrado
NLMeansP input.png sigma 0 input.png output.png
```

---

## Métricas de evaluación

[`scripts/evaluate_method.py`](scripts/evaluate_method.py)

Se usan dos métricas estándar en procesado de imagen:

### PSNR — Peak Signal-to-Noise Ratio
[Peak Signal-to-Noise Ratio](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio): mide la relación entre la señal máxima posible y el ruido residual. Se expresa en decibelios (dB). Valores más altos = mejor reconstrucción.

```
PSNR = 20 · log₁₀(255 / √MSE)
```

Un PSNR > 40 dB se considera excelente. Los resultados en este dataset rondan los 33–44 dB.

### SSIM — Structural Similarity Index
[Structural Similarity Index](https://en.wikipedia.org/wiki/Structural_similarity): mide la similitud perceptual entre imágenes teniendo en cuenta luminancia, contraste y estructura. Varía entre 0 y 1 (1 = imagen idéntica).

A diferencia del PSNR (basado en MSE píxel a píxel), el SSIM correlaciona mejor con la percepción humana de calidad.

---

## Resultados

### Visualización de sigma

Exploración del efecto del nivel de ruido sigma sobre la imagen denoised (BM3D GPU):

![Sigma visualization](https://github.com/qwerteleven/image-denoising/blob/main/assets/sigma_visualization.png)

---

### Comparativa visual de métodos

| Método | Ejemplo |
|--------|---------|
| Original | ![original](https://github.com/qwerteleven/image-denoising/blob/main/assets/original.png) |
| BM3D | ![bm3d](https://github.com/qwerteleven/image-denoising/blob/main/assets/bm3d.png) |
| DCT Denoising | ![dct](https://github.com/qwerteleven/image-denoising/blob/main/assets/DCTdenoising.png) |
| NLM with Patch | ![nlmp](https://github.com/qwerteleven/image-denoising/blob/main/assets/nlmp.png) |

---

### Métricas cuantitativas (PSNR / SSIM)

| DCT Denoising | NLM with Patch |
|---|---|
| ![DCT metrics](https://github.com/qwerteleven/image-denoising/blob/main/assets/DCTdenoising.json.png) | ![NLM metrics](https://github.com/qwerteleven/image-denoising/blob/main/assets/nlmp.json.png) |

**Resumen estadístico** (sobre 57 imágenes de los datasets `radisson` y `anfi`):

| Método | PSNR medio (dB) | SSIM medio |
|--------|----------------|------------|
| DCT Denoising | ~35.2 | ~0.874 |
| NLM with Patch | ~33.4 | ~0.814 |

DCT Denoising supera consistentemente a NLM en ambas métricas sobre este dataset.

---

## Estructura del proyecto

```
image-denoising/
├── scripts/
│   ├── bm3d.py              # BM3D clásico (CPU)
│   ├── bm3d_gpu.py          # BM3D con exploración de sigma (GPU)
│   ├── DCTdenoising.py      # DCT Denoising
│   ├── nlmp.py              # Non-Local Means with Patch
│   ├── evaluate_method.py   # Cálculo de PSNR y SSIM
│   ├── data_explorer.py     # Visualización de métricas
│   ├── show_img.py          # Comparación visual por imagen
│   ├── show_sigma_img.py    # Visualización del efecto sigma
│   └── change_file_extension.py  # Utilidad de conversión de formato
├── result_metadata/
│   ├── DCTdenoising.json    # Resultados PSNR/SSIM por imagen
│   └── nlmp.json
└── dataset/
    ├── radisson/            # Imágenes de hotel Radisson
    └── anfi/                # Imágenes de hotel Anfi
```

---

## Dependencias externas (IPOL)

Los métodos se ejecutan sobre binarios compilados de [IPOL (Image Processing On Line)](https://www.ipol.im/), plataforma de referencia para algoritmos de procesado de imagen reproducibles:

- **BM3D**: `ipol_methods/bm3d/build/bm3d`
- **BM3D GPU**: `ipol_methods/bm3d-gpu/build/bm3d`
- **DCT Denoising**: `ipol_methods/DCTdenoising-master/build/dctdenoising`
- **NLM with Patch**: `ipol_methods/nlmp_1.2/NLMeansP`

---

## Uso rápido

```bash
# Ejecutar DCT Denoising sobre el dataset
python scripts/DCTdenoising.py

# Evaluar resultados (genera JSON con PSNR/SSIM)
python scripts/evaluate_method.py

# Explorar resultados visualmente
python scripts/data_explorer.py

# Ver comparativa para la imagen índice N
python scripts/show_img.py N
```

---

## Conceptos clave — Referencias

| Concepto | Wikipedia |
|----------|-----------|
| Ruido en imagen | [Image noise](https://en.wikipedia.org/wiki/Image_noise) |
| BM3D | [Block-matching and 3D filtering](https://en.wikipedia.org/wiki/Block-matching_and_3D_filtering) |
| Transformada DCT | [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) |
| Non-Local Means | [Non-local means](https://en.wikipedia.org/wiki/Non-local_means) |
| PSNR | [Peak signal-to-noise ratio](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio) |
| SSIM | [Structural similarity index](https://en.wikipedia.org/wiki/Structural_similarity) |
| Wavelets Bior | [Biorthogonal wavelet](https://en.wikipedia.org/wiki/Biorthogonal_wavelet) |