import os
import numpy as np
from PIL import Image
import tensorflow as tf
from pathlib import Path
from typing import Tuple, List
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class DataPreprocessor:
    def __init__(self, image_size: int = 128, normalize: bool = True):
        self.image_size = image_size
        self.normalize = normalize
    
    def load_image(self, image_path: str) -> np.ndarray:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((self.image_size, self.image_size))
        img = np.array(img)
        if self.normalize:
            img = (img.astype(np.float32) - 127.5) / 127.5
        return img
    
    def load_dataset(self, dataset_path: str) -> np.ndarray:
        images = []
        valid_extensions = {'.jpg', '.jpeg', '.png'}
        
        for root, _, files in os.walk(dataset_path):
            for file in files:
                if Path(file).suffix.lower() in valid_extensions:
                    img_path = os.path.join(root, file)
                    try:
                        img = self.load_image(img_path)
                        images.append(img)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        
        return np.array(images)
    
    def create_data_generator(self, dataset_path: str, batch_size: int = 32):
        datagen = ImageDataGenerator(
            rescale=1./127.5,
            preprocessing_function=lambda x: x - 1.0,
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        generator = datagen.flow_from_directory(
            dataset_path,
            target_size=(self.image_size, self.image_size),
            batch_size=batch_size,
            class_mode=None,
            shuffle=True
        )
        
        return generator
    
    def get_dataset_statistics(self, dataset_path: str) -> dict:
        images = self.load_dataset(dataset_path)
        
        stats = {
            'total_images': len(images),
            'image_shape': images[0].shape if len(images) > 0 else None,
            'mean': np.mean(images) if len(images) > 0 else 0,
            'std': np.std(images) if len(images) > 0 else 0,
            'min': np.min(images) if len(images) > 0 else 0,
            'max': np.max(images) if len(images) > 0 else 0
        }
        
        return stats

class DataAugmentor:
    @staticmethod
    def augment_image(image: np.ndarray) -> np.ndarray:
        # Random flip
        if np.random.rand() > 0.5:
            image = np.fliplr(image)
        
        # Random rotation
        if np.random.rand() > 0.5:
            k = np.random.randint(1, 4)
            image = np.rot90(image, k)
        
        return image
    
    @staticmethod
    def augment_dataset(images: np.ndarray, factor: int = 2) -> np.ndarray:
        augmented = [images]
        
        for _ in range(factor - 1):
            aug_images = np.array([DataAugmentor.augment_image(img) for img in images])
            augmented.append(aug_images)
        
        return np.concatenate(augmented, axis=0)
