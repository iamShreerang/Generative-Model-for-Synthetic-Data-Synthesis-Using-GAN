"""
Test image generation with trained model
"""
import os
import matplotlib.pyplot as plt
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from config.settings import settings

print("=" * 60)
print("Testing Image Generation with Trained Model")
print("=" * 60)

# List available models
print("\nAvailable models:")
models = []
if os.path.exists(settings.MODEL_CHECKPOINT_PATH):
    for file in os.listdir(settings.MODEL_CHECKPOINT_PATH):
        if file.endswith('_generator.h5'):
            model_name = file.replace('_generator.h5', '')
            models.append(model_name)
            print(f"  - {model_name}")

if not models:
    print("ERROR: No trained models found!")
    print(f"Please train a model first in: {settings.MODEL_CHECKPOINT_PATH}")
    exit(1)

# Use the latest model
model_name = models[-1]
print(f"\nUsing model: {model_name}")

# Load model
print("Loading model...")
model_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, model_name)
print(f"Model path: {model_path}")

try:
    gan = DCGAN(image_size=128)
    gan.load_models(model_path)
    print("OK - Model loaded successfully")
except Exception as e:
    print(f"ERROR loading model: {e}")
    exit(1)

# Generate images
print("\nGenerating 16 synthetic images...")
try:
    trainer = GANTrainer(gan)
    output_dir = os.path.join(settings.SYNTHETIC_DATA_PATH, "test_generation")
    os.makedirs(output_dir, exist_ok=True)
    
    trainer.save_generated_samples(output_dir, num_samples=16)
    print(f"OK - Images generated successfully")
    print(f"Saved to: {output_dir}")
except Exception as e:
    print(f"ERROR generating images: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("SUCCESS! Images generated")
print("=" * 60)
print(f"\nCheck folder: {output_dir}")
print("\nIf this works, the UI should also work after restart.")
