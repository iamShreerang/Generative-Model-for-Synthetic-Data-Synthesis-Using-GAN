"""
Generate synthetic images using your trained model
Model: final_20260623_174545
"""
import os
import matplotlib.pyplot as plt
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from config.settings import settings

print("=" * 60)
print("Generating Synthetic Images from Trained Model")
print("=" * 60)
print()

# Model path
model_name = "final_20260623_174545"
model_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, model_name)

print(f"Model: {model_name}")
print(f"Path: {model_path}")
print()

# Check if model exists
gen_path = f"{model_path}_generator.h5"
disc_path = f"{model_path}_discriminator.h5"

if not os.path.exists(gen_path):
    print(f"ERROR: Generator not found at {gen_path}")
    exit(1)

if not os.path.exists(disc_path):
    print(f"ERROR: Discriminator not found at {disc_path}")
    exit(1)

print("OK - Model files found")
print()

# Load model
print("Loading trained DCGAN model...")
gan = DCGAN(image_size=128, noise_dim=100)
gan.load_models(model_path)
print("OK - Model loaded successfully")
print()

# Generate samples
print("Generating synthetic images...")
num_samples = 16
trainer = GANTrainer(gan)
samples = trainer.generate_samples(num_samples)
print(f"OK - Generated {num_samples} images")
print()

# Save images
output_dir = os.path.join(settings.SYNTHETIC_DATA_PATH, "generated_from_trained")
os.makedirs(output_dir, exist_ok=True)

print(f"Saving images to: {output_dir}")
for i, sample in enumerate(samples):
    img_path = os.path.join(output_dir, f"synthetic_{i+1:03d}.png")
    plt.imsave(img_path, sample)

print(f"OK - Saved {num_samples} images")
print()

# Create grid
print("Creating visualization grid...")
fig, axes = plt.subplots(4, 4, figsize=(12, 12))
fig.suptitle('Generated Synthetic Images (Trained Model)', fontsize=16)

for i, ax in enumerate(axes.flat):
    if i < num_samples:
        ax.imshow(samples[i])
        ax.axis('off')
        ax.set_title(f'Image {i+1}', fontsize=8)

grid_path = os.path.join(output_dir, "generated_grid.png")
plt.tight_layout()
plt.savefig(grid_path, dpi=150, bbox_inches='tight')
print(f"OK - Grid saved to: {grid_path}")
print()

print("=" * 60)
print("SUCCESS! Images Generated")
print("=" * 60)
print(f"\nLocation: {output_dir}")
print(f"Total images: {num_samples}")
print(f"\nOpen folder to view results:")
print(f"  {output_dir}")
