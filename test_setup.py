"""
Test script to verify all components work correctly
"""
import sys

print("Testing Synthetic Data Generation Platform...")
print("-" * 50)

# Test 1: Import packages
print("\n1. Testing package imports...")
try:
    import tensorflow as tf
    print(f"   OK TensorFlow {tf.__version__}")
except Exception as e:
    print(f"   ERROR TensorFlow: {e}")
    sys.exit(1)

try:
    import streamlit
    print(f"   OK Streamlit installed")
except Exception as e:
    print(f"   ERROR Streamlit: {e}")
    sys.exit(1)

try:
    import fastapi
    print(f"   OK FastAPI installed")
except Exception as e:
    print(f"   ERROR FastAPI: {e}")
    sys.exit(1)

# Test 2: Import project modules
print("\n2. Testing project modules...")
try:
    from src.models.dcgan import DCGAN
    print("   OK DCGAN model")
except Exception as e:
    print(f"   ERROR DCGAN model: {e}")
    sys.exit(1)

try:
    from src.training.trainer import GANTrainer
    print("   OK GANTrainer")
except Exception as e:
    print(f"   ERROR GANTrainer: {e}")
    sys.exit(1)

try:
    from src.data.preprocessor import DataPreprocessor
    print("   OK DataPreprocessor")
except Exception as e:
    print(f"   ERROR DataPreprocessor: {e}")
    sys.exit(1)

try:
    from src.evaluation.metrics import Evaluator
    print("   OK Evaluator")
except Exception as e:
    print(f"   ERROR Evaluator: {e}")
    sys.exit(1)

try:
    from src.utils.database import init_db
    print("   OK Database")
except Exception as e:
    print(f"   ERROR Database: {e}")
    sys.exit(1)

try:
    from config.settings import settings
    print("   OK Settings")
except Exception as e:
    print(f"   ERROR Settings: {e}")
    sys.exit(1)

# Test 3: Create DCGAN model
print("\n3. Testing DCGAN model creation...")
try:
    gan = DCGAN(image_size=128, noise_dim=100)
    print("   OK Generator created")
    print("   OK Discriminator created")
except Exception as e:
    print(f"   ERROR DCGAN creation: {e}")
    sys.exit(1)

# Test 4: Test model outputs
print("\n4. Testing model outputs...")
try:
    import numpy as np
    noise = np.random.normal(0, 1, (1, 100))
    output = gan.generator.predict(noise, verbose=0)
    assert output.shape == (1, 128, 128, 3)
    print(f"   OK Generator output shape: {output.shape}")
except Exception as e:
    print(f"   ERROR Generator test: {e}")
    sys.exit(1)

try:
    fake_image = np.random.normal(0, 1, (1, 128, 128, 3))
    output = gan.discriminator.predict(fake_image, verbose=0)
    assert output.shape == (1, 1)
    print(f"   OK Discriminator output shape: {output.shape}")
except Exception as e:
    print(f"   ERROR Discriminator test: {e}")
    sys.exit(1)

# Test 5: Initialize database
print("\n5. Testing database initialization...")
try:
    init_db()
    print("   OK Database initialized")
except Exception as e:
    print(f"   ERROR Database: {e}")
    sys.exit(1)

# Test 6: Check folders
print("\n6. Checking project folders...")
import os
folders = ['Dataset', 'Synthetic Data', 'models/checkpoints', 'database', 'logs']
for folder in folders:
    if os.path.exists(folder):
        print(f"   OK {folder}/")
    else:
        print(f"   Creating {folder}/")
        os.makedirs(folder, exist_ok=True)

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)
print("\nReady to start the application!")
print("\nNext steps:")
print("1. Start API: python -m uvicorn src.api.main:app --port 8000")
print("2. Start Frontend: streamlit run frontend/app.py")
print("3. Or use: run.bat")
