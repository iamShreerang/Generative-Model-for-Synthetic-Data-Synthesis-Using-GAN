import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tqdm import tqdm

class GANTrainer:
    def __init__(self, gan_model, learning_rate: float = 0.0002):
        self.gan = gan_model
        self.generator = gan_model.generator
        self.discriminator = gan_model.discriminator
        
        self.gen_optimizer = keras.optimizers.Adam(learning_rate, beta_1=0.5)
        self.disc_optimizer = keras.optimizers.Adam(learning_rate, beta_1=0.5)
        self.cross_entropy = keras.losses.BinaryCrossentropy()
        
        self.gen_loss_history = []
        self.disc_loss_history = []
        
    def discriminator_loss(self, real_output, fake_output):
        real_loss = self.cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = self.cross_entropy(tf.zeros_like(fake_output), fake_output)
        return real_loss + fake_loss
    
    def generator_loss(self, fake_output):
        return self.cross_entropy(tf.ones_like(fake_output), fake_output)
    
    @tf.function
    def train_step(self, real_images, noise):
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            generated_images = self.generator(noise, training=True)
            real_output = self.discriminator(real_images, training=True)
            fake_output = self.discriminator(generated_images, training=True)
            
            gen_loss = self.generator_loss(fake_output)
            disc_loss = self.discriminator_loss(real_output, fake_output)
        
        gen_gradients = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
        disc_gradients = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)
        
        self.gen_optimizer.apply_gradients(zip(gen_gradients, self.generator.trainable_variables))
        self.disc_optimizer.apply_gradients(zip(disc_gradients, self.discriminator.trainable_variables))
        
        return gen_loss, disc_loss
    
    def train(self, dataset, epochs: int, batch_size: int, save_interval: int = 5, 
              checkpoint_dir: str = "./models/checkpoints", callback=None):
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        for epoch in range(epochs):
            epoch_gen_loss, epoch_disc_loss = [], []
            
            for real_images in tqdm(dataset, desc=f"Epoch {epoch+1}/{epochs}"):
                if real_images.shape[0] != batch_size:
                    continue
                
                noise = tf.random.normal([batch_size, self.gan.noise_dim])
                gen_loss, disc_loss = self.train_step(real_images, noise)
                
                epoch_gen_loss.append(gen_loss.numpy())
                epoch_disc_loss.append(disc_loss.numpy())
            
            avg_gen_loss = np.mean(epoch_gen_loss)
            avg_disc_loss = np.mean(epoch_disc_loss)
            
            self.gen_loss_history.append(avg_gen_loss)
            self.disc_loss_history.append(avg_disc_loss)
            
            print(f"Epoch {epoch+1}: G_loss: {avg_gen_loss:.4f}, D_loss: {avg_disc_loss:.4f}")
            
            if (epoch + 1) % save_interval == 0:
                self.gan.save_models(os.path.join(checkpoint_dir, f"epoch_{epoch+1}"))
            
            if callback:
                callback(epoch + 1, avg_gen_loss, avg_disc_loss)
    
    def generate_samples(self, num_samples: int = 16):
        noise = tf.random.normal([num_samples, self.gan.noise_dim])
        generated_images = self.generator(noise, training=False)
        return ((generated_images + 1) / 2.0).numpy()
    
    def save_generated_samples(self, output_dir: str, num_samples: int = 16):
        os.makedirs(output_dir, exist_ok=True)
        samples = self.generate_samples(num_samples)
        
        for i, sample in enumerate(samples):
            sample = np.clip(sample, 0, 1)
            sample_uint8 = (sample * 255).astype(np.uint8)
            from PIL import Image
            Image.fromarray(sample_uint8).save(os.path.join(output_dir, f"synthetic_image_{i}.png"))
        
        return output_dir
