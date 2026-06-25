"""
Continue training the model for better results
"""
import tensorflow as tf
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from src.data.preprocessor import DataPreprocessor
from config.settings import settings
import os

print("Continuing model training for better image quality...")
print()

# Load existing model
model_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, "final_20260623_174545")
print(f"Loading model from: {model_path}")

gan = DCGAN(image_size=128, noise_dim=100)
gan.load_models(model_path)
print("Model loaded")
print()

# Load dataset
print("Loading glioma dataset...")
preprocessor = DataPreprocessor(image_size=128)
dataset_path = os.path.join(settings.DATASET_PATH, "glioma")
images = preprocessor.load_dataset(dataset_path)
print(f"Loaded {len(images)} images")
print()

# Create TF dataset
batch_size = 32
dataset = tf.data.Dataset.from_tensor_slices(images).batch(batch_size)

# Continue training
print("Continuing training for 50 more epochs...")
trainer = GANTrainer(gan, learning_rate=0.0002)
trainer.train(dataset, 50, batch_size, save_interval=10)

# Save model
final_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, "trained_model")
gan.save_models(final_path)
print(f"\nModel saved to: {final_path}")
print("Training complete! Generate new images from UI using 'trained_model'")
