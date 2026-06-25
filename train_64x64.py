"""
Train with 64x64 images for faster, better results
"""
import tensorflow as tf
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from src.data.preprocessor import DataPreprocessor
from config.settings import settings
import os

print("Training DCGAN with 64x64 images (faster convergence)")
print()

# Load dataset at smaller size
print("Loading glioma dataset at 64x64...")
preprocessor = DataPreprocessor(image_size=64)
dataset_path = os.path.join(settings.DATASET_PATH, "glioma")
images = preprocessor.load_dataset(dataset_path)
print(f"Loaded {len(images)} images")
print()

# Create TF dataset
batch_size = 64
dataset = tf.data.Dataset.from_tensor_slices(images).batch(batch_size)

# Create new model for 64x64
print("Creating DCGAN for 64x64 images...")
gan = DCGAN(image_size=64, noise_dim=100)

# Train
print("Training for 200 epochs...")
trainer = GANTrainer(gan, learning_rate=0.0002)
trainer.train(dataset, 200, batch_size, save_interval=50)

# Save
final_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, "dcgan_64x64_trained")
gan.save_models(final_path)
print(f"\nModel saved: {final_path}")
print("Generate images using model: dcgan_64x64_trained")
