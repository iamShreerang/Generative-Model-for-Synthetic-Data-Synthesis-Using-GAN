from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import shutil
from datetime import datetime
import tensorflow as tf
import numpy as np
from src.models.dcgan import DCGAN
from src.training.trainer import GANTrainer
from src.data.preprocessor import DataPreprocessor
from src.evaluation.metrics import Evaluator
from src.utils.database import init_db, get_db, TrainingRun, EvaluationMetric
from config.settings import settings

app = FastAPI(title="Synthetic Data Generation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Global training state
training_state = {
    "is_training": False,
    "current_epoch": 0,
    "total_epochs": 0,
    "gen_loss": 0.0,
    "disc_loss": 0.0
}

class TrainingConfig(BaseModel):
    dataset_name: str
    epochs: int = 50
    batch_size: int = 32
    learning_rate: float = 0.0002
    image_size: int = 128

class GenerateRequest(BaseModel):
    num_samples: int = 16
    model_path: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Synthetic Data Generation Platform API", "status": "active"}

@app.post("/upload-dataset/")
async def upload_dataset(files: List[UploadFile] = File(...), dataset_name: str = "custom"):
    try:
        dataset_path = os.path.join(settings.DATASET_PATH, dataset_name)
        os.makedirs(dataset_path, exist_ok=True)
        
        uploaded_count = 0
        for file in files:
            if file.filename and file.filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']:
                file_path = os.path.join(dataset_path, file.filename)
                contents = await file.read()
                with open(file_path, "wb") as buffer:
                    buffer.write(contents)
                uploaded_count += 1
        
        return {"message": f"Uploaded {uploaded_count} images", "dataset_path": dataset_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

@app.get("/datasets/")
def list_datasets():
    datasets = []
    if os.path.exists(settings.DATASET_PATH):
        for name in os.listdir(settings.DATASET_PATH):
            path = os.path.join(settings.DATASET_PATH, name)
            if os.path.isdir(path):
                image_count = len([f for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))])
                datasets.append({"name": name, "image_count": image_count, "path": path})
    return {"datasets": datasets}

@app.post("/train/")
async def start_training(config: TrainingConfig, background_tasks: BackgroundTasks):
    if training_state["is_training"]:
        raise HTTPException(status_code=400, detail="Training already in progress")
    
    background_tasks.add_task(train_model, config)
    return {"message": "Training started", "config": config.dict()}

def train_model(config: TrainingConfig):
    training_state["is_training"] = True
    training_state["total_epochs"] = config.epochs
    
    try:
        # Load dataset
        preprocessor = DataPreprocessor(image_size=config.image_size)
        dataset_path = os.path.join(settings.DATASET_PATH, config.dataset_name)
        images = preprocessor.load_dataset(dataset_path)
        
        # Create TF dataset
        dataset = tf.data.Dataset.from_tensor_slices(images).batch(config.batch_size)
        
        # Create model
        gan = DCGAN(image_size=config.image_size)
        trainer = GANTrainer(gan, learning_rate=config.learning_rate)
        
        # Training callback
        def update_state(epoch, gen_loss, disc_loss):
            training_state["current_epoch"] = epoch
            training_state["gen_loss"] = float(gen_loss)
            training_state["disc_loss"] = float(disc_loss)
        
        # Train
        trainer.train(dataset, config.epochs, config.batch_size, callback=update_state)
        
        # Save final model
        model_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, f"final_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        gan.save_models(model_path)
        
    finally:
        training_state["is_training"] = False

@app.get("/training-status/")
def get_training_status():
    return training_state

@app.post("/generate/")
async def generate_samples(request: GenerateRequest):
    try:
        gan = DCGAN(image_size=settings.IMAGE_SIZE)
        
        if request.model_path:
            # Check if full path or just name
            if os.path.exists(request.model_path + "_generator.h5"):
                model_path = request.model_path
            elif os.path.exists(os.path.join(settings.MODEL_CHECKPOINT_PATH, request.model_path + "_generator.h5")):
                model_path = os.path.join(settings.MODEL_CHECKPOINT_PATH, request.model_path)
            else:
                raise HTTPException(status_code=404, detail=f"Model not found at: {request.model_path}")
            
            print(f"Loading model from: {model_path}")
            gan.load_models(model_path)
        else:
            raise HTTPException(status_code=404, detail="Model path not provided. Train a model first.")
        
        trainer = GANTrainer(gan)
        output_dir = os.path.join(settings.SYNTHETIC_DATA_PATH, datetime.now().strftime('%Y%m%d_%H%M%S'))
        trainer.save_generated_samples(output_dir, request.num_samples)
        
        return {"message": f"Generated {request.num_samples} samples", "output_dir": output_dir}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@app.get("/models/")
def list_models():
    models = []
    if os.path.exists(settings.MODEL_CHECKPOINT_PATH):
        for file in os.listdir(settings.MODEL_CHECKPOINT_PATH):
            if file.endswith('_generator.h5'):
                model_name = file.replace('_generator.h5', '')
                models.append({"name": model_name, "path": model_name})
    return {"models": models}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
