import pytest
import numpy as np
from src.models.dcgan import DCGAN

def test_dcgan_creation():
    gan = DCGAN(image_size=128, noise_dim=100)
    assert gan.generator is not None
    assert gan.discriminator is not None

def test_generator_output_shape():
    gan = DCGAN(image_size=128, noise_dim=100)
    noise = np.random.normal(0, 1, (1, 100))
    output = gan.generator.predict(noise, verbose=0)
    assert output.shape == (1, 128, 128, 3)

def test_discriminator_output_shape():
    gan = DCGAN(image_size=128, noise_dim=100)
    fake_image = np.random.normal(0, 1, (1, 128, 128, 3))
    output = gan.discriminator.predict(fake_image, verbose=0)
    assert output.shape == (1, 1)
