
# Generative Model for Synthetic Data Synthesis Using GAN

## Overview

This project implements a **Generative Adversarial Network (GAN)** for synthetic medical image generation. The model is trained on Glioma MRI images and generates realistic synthetic images that can be used for data augmentation, research, and machine learning model development, particularly in scenarios where medical datasets are limited.

## Objectives

* Generate synthetic Glioma MRI images using Deep Learning.
* Address data scarcity in healthcare datasets.
* Improve dataset diversity for training AI models.
* Support research in medical image analysis while preserving patient privacy.

## Features

* Image preprocessing and normalization.
* GAN-based synthetic image generation.
* Convolutional Generator and Discriminator networks.
* Automatic saving of generated images.
* Visualization of synthetic outputs.
* TensorFlow/Keras implementation.

## Dataset

The model uses a Glioma MRI image dataset stored in:

```
Dataset/glioma
```

### Dataset Requirements

* Image Format: JPG, JPEG, PNG
* RGB Images
* Organized directory structure compatible with Keras `flow_from_directory()`

Example:

```
Dataset/
└── glioma/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

## Technology Stack

* Python
* TensorFlow
* Keras
* NumPy
* Matplotlib

## Model Architecture

### Generator

The Generator creates synthetic MRI images from random noise vectors.

Layers:

* Dense Layer
* Batch Normalization
* LeakyReLU
* Reshape Layer
* Conv2DTranspose Layers
* Tanh Activation

### Discriminator

The Discriminator classifies images as Real or Fake.

Layers:

* Conv2D
* LeakyReLU
* Dropout
* Flatten
* Dense Output Layer

## Training Process

1. Load and preprocess MRI images.
2. Generate random noise vectors.
3. Create synthetic images using the Generator.
4. Train Discriminator on:

   * Real Images
   * Generated Images
5. Update Generator based on Discriminator feedback.
6. Repeat for multiple epochs.

Training Parameters:

| Parameter       | Value  |
| --------------- | ------ |
| Epochs          | 50     |
| Batch Size      | 32     |
| Learning Rate   | 0.0001 |
| Noise Dimension | 100    |

## Synthetic Data Generation

After training:

1. Random noise is generated.
2. Generator produces synthetic MRI images.
3. Images are stored in:

```
Synthetic Data/
```

Generated files:

```
synthetic_image_0.png
synthetic_image_1.png
...
```

## Applications

* Medical Image Augmentation
* Rare Disease Research
* Healthcare AI Development
* Deep Learning Dataset Expansion
* Privacy-Preserving Data Sharing

## Expected Outcomes

* Increased dataset size without additional patient data collection.
* Improved training performance for machine learning models.
* Enhanced robustness and generalization of medical AI systems.

## Future Enhancements

* Implement DCGAN architecture.
* Add Conditional GAN (CGAN) support.
* Generate higher-resolution MRI scans.
* Integrate evaluation metrics such as:

  * FID (Fréchet Inception Distance)
  * SSIM (Structural Similarity Index)
  * PSNR (Peak Signal-to-Noise Ratio)
* Develop a web-based interface for synthetic image generation.

## Installation

```bash
pip install tensorflow numpy matplotlib
```

## Run the Project

```bash
python gan_synthetic_data_generation.py
```

## Disclaimer

This project is intended for educational, research, and healthcare AI development purposes. Generated images should not be used for clinical diagnosis without proper validation by medical experts.
