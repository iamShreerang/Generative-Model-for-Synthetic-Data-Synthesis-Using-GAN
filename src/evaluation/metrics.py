import numpy as np
from scipy import linalg
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import tensorflow as tf

class Evaluator:
    @staticmethod
    def calculate_fid(real_images, generated_images):
        """Calculate Frechet Inception Distance"""
        mu1, sigma1 = np.mean(real_images, axis=0), np.cov(real_images, rowvar=False)
        mu2, sigma2 = np.mean(generated_images, axis=0), np.cov(generated_images, rowvar=False)
        
        ssdiff = np.sum((mu1 - mu2) ** 2)
        covmean = linalg.sqrtm(sigma1.dot(sigma2))
        
        if np.iscomplexobj(covmean):
            covmean = covmean.real
        
        fid = ssdiff + np.trace(sigma1 + sigma2 - 2 * covmean)
        return fid
    
    @staticmethod
    def calculate_ssim(real_images, generated_images):
        """Calculate Structural Similarity Index"""
        ssim_scores = []
        for real, gen in zip(real_images, generated_images):
            score = ssim(real, gen, data_range=1.0, channel_axis=2)
            ssim_scores.append(score)
        return np.mean(ssim_scores)
    
    @staticmethod
    def calculate_psnr(real_images, generated_images):
        """Calculate Peak Signal-to-Noise Ratio"""
        psnr_scores = []
        for real, gen in zip(real_images, generated_images):
            score = psnr(real, gen, data_range=1.0)
            psnr_scores.append(score)
        return np.mean(psnr_scores)
    
    @staticmethod
    def evaluate_all(real_images, generated_images):
        """Run all evaluation metrics"""
        real_flat = real_images.reshape(len(real_images), -1)
        gen_flat = generated_images.reshape(len(generated_images), -1)
        
        return {
            'fid': Evaluator.calculate_fid(real_flat, gen_flat),
            'ssim': Evaluator.calculate_ssim(real_images, generated_images),
            'psnr': Evaluator.calculate_psnr(real_images, generated_images)
        }
