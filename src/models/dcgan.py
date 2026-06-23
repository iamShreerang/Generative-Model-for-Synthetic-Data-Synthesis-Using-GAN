import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class DCGAN:
    def __init__(self, image_size: int = 128, noise_dim: int = 100, channels: int = 3):
        self.image_size = image_size
        self.noise_dim = noise_dim
        self.channels = channels
        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
    
    def build_generator(self):
        model = keras.Sequential([
            layers.Dense(8 * 8 * 256, input_dim=self.noise_dim, use_bias=False),
            layers.BatchNormalization(),
            layers.LeakyReLU(0.2),
            layers.Reshape((8, 8, 256)),
            
            layers.Conv2DTranspose(128, (5, 5), strides=(2, 2), padding='same', use_bias=False),
            layers.BatchNormalization(),
            layers.LeakyReLU(0.2),
            
            layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False),
            layers.BatchNormalization(),
            layers.LeakyReLU(0.2),
            
            layers.Conv2DTranspose(32, (5, 5), strides=(2, 2), padding='same', use_bias=False),
            layers.BatchNormalization(),
            layers.LeakyReLU(0.2),
            
            layers.Conv2DTranspose(self.channels, (5, 5), strides=(2, 2), padding='same', activation='tanh')
        ], name="generator")
        
        return model
    
    def build_discriminator(self):
        model = keras.Sequential([
            layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                         input_shape=(self.image_size, self.image_size, self.channels)),
            layers.LeakyReLU(0.2),
            layers.Dropout(0.3),
            
            layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'),
            layers.LeakyReLU(0.2),
            layers.Dropout(0.3),
            
            layers.Conv2D(256, (5, 5), strides=(2, 2), padding='same'),
            layers.LeakyReLU(0.2),
            layers.Dropout(0.3),
            
            layers.Flatten(),
            layers.Dense(1, activation='sigmoid')
        ], name="discriminator")
        
        return model
    
    def save_models(self, path: str):
        self.generator.save(f"{path}_generator.h5")
        self.discriminator.save(f"{path}_discriminator.h5")
    
    def load_models(self, path: str):
        self.generator = keras.models.load_model(f"{path}_generator.h5")
        self.discriminator = keras.models.load_model(f"{path}_discriminator.h5")
