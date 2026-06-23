"""
Simple training script for quick model training without API
"""
import tensorflow as tf
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from src.data.preprocessor import DataPreprocessor
from config.settings import settings
import os

def train_simple():
    print("🚀 Starting GAN Training...")
    
    # Configuration
    DATASET_NAME = "glioma"
    IMAGE_SIZE = 128
    EPOCHS = 50
    BATCH_SIZE = 32
    LEARNING_RATE = 0.0002
    
    # Load dataset
    print(f"📁 Loading dataset: {DATASET_NAME}")
    preprocessor = DataPreprocessor(image_size=IMAGE_SIZE)
    dataset_path = os.path.join(settings.DATASET_PATH, DATASET_NAME)
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        return
    
    images = preprocessor.load_dataset(dataset_path)
    print(f"✅ Loaded {len(images)} images")
    
    # Create TensorFlow dataset
    dataset = tf.data.Dataset.from_tensor_slices(images).batch(BATCH_SIZE)
    
    # Create model
    print("🏗️ Building DCGAN model...")
    gan = DCGAN(image_size=IMAGE_SIZE)
    
    # Create trainer
    trainer = GANTrainer(gan, learning_rate=LEARNING_RATE)
    
    # Train
    print("🎯 Starting training...")
    trainer.train(
        dataset=dataset,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        save_interval=10
    )
    
    # Generate samples
    print("🎨 Generating sample images...")
    output_dir = os.path.join(settings.SYNTHETIC_DATA_PATH, "training_samples")
    trainer.save_generated_samples(output_dir, num_samples=16)
    
    print(f"✅ Training complete! Samples saved to {output_dir}")

if __name__ == "__main__":
    train_simple()
