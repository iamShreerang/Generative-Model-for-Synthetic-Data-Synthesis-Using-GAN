import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./database/synthetic_gan.db"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # Streamlit
    STREAMLIT_PORT: int = 8501
    
    # Model
    DEFAULT_MODEL: str = "dcgan"
    IMAGE_SIZE: int = 128
    BATCH_SIZE: int = 32
    EPOCHS: int = 50
    LEARNING_RATE: float = 0.0002
    NOISE_DIM: int = 100
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATASET_PATH: str = "./Dataset"
    SYNTHETIC_DATA_PATH: str = "./Synthetic Data"
    MODEL_CHECKPOINT_PATH: str = "./models/checkpoints"
    LOGS_PATH: str = "./logs"
    
    # Training
    SAVE_INTERVAL: int = 5
    SAMPLE_INTERVAL: int = 100
    MAX_UPLOAD_SIZE: int = 100
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png"
    
    # GPU
    USE_GPU: bool = True
    GPU_MEMORY_LIMIT: int = 4096
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Create necessary directories
os.makedirs(settings.DATASET_PATH, exist_ok=True)
os.makedirs(settings.SYNTHETIC_DATA_PATH, exist_ok=True)
os.makedirs(settings.MODEL_CHECKPOINT_PATH, exist_ok=True)
os.makedirs(settings.LOGS_PATH, exist_ok=True)
os.makedirs("./database", exist_ok=True)
