"""
Quick demo - Generate synthetic images without full training
This creates a simple untrained model and generates samples
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from src.models.dcgan import DCGAN
from config.settings import settings

print("=" * 50)
print("Quick Demo - Generating Synthetic Images")
print("=" * 50)
print()

# Create output directory
output_dir = os.path.join(settings.SYNTHETIC_DATA_PATH, "demo_samples")
os.makedirs(output_dir, exist_ok=True)

# Create DCGAN model (untrained)
print("Creating DCGAN model...")
gan = DCGAN(image_size=128, noise_dim=100)
print("OK - Model created")

# Generate random noise
print("\nGenerating synthetic images...")
num_samples = 16
noise = np.random.normal(0, 1, (num_samples, 100))

# Generate images
generated_images = gan.generator.predict(noise, verbose=0)

# Denormalize from [-1, 1] to [0, 1]
generated_images = (generated_images + 1) / 2.0

# Save individual images
print(f"\nSaving {num_samples} images to: {output_dir}")
for i, img in enumerate(generated_images):
    img_path = os.path.join(output_dir, f"demo_image_{i+1:03d}.png")
    plt.imsave(img_path, img)

print(f"OK - Saved {num_samples} images")

# Create a grid visualization
print("\nCreating grid visualization...")
fig, axes = plt.subplots(4, 4, figsize=(10, 10))
fig.suptitle('Generated Synthetic Images (Untrained Model)', fontsize=16)

for i, ax in enumerate(axes.flat):
    if i < num_samples:
        ax.imshow(generated_images[i])
        ax.axis('off')

grid_path = os.path.join(output_dir, "demo_grid.png")
plt.tight_layout()
plt.savefig(grid_path, dpi=150, bbox_inches='tight')
print(f"OK - Grid saved to: {grid_path}")

print("\n" + "=" * 50)
print("Demo Complete!")
print("=" * 50)
print(f"\nImages saved to: {output_dir}")
print("\nNOTE: These are from an UNTRAINED model (random noise)")
print("For realistic images, you need to train the model first.")
print("\nTo train:")
print("1. Go to Training page")
print("2. Use dataset: glioma")
print("3. Set epochs: 50")
print("4. Click Start Training")
