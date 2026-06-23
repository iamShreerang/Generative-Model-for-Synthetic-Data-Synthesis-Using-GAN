# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Synthetic Data Generation Platform API",
  "status": "active"
}
```

---

### Upload Dataset
```http
POST /upload-dataset/
```

**Parameters:**
- `files`: List of image files (multipart/form-data)
- `dataset_name`: String (query parameter)

**Response:**
```json
{
  "message": "Uploaded 50 images",
  "dataset_path": "./Dataset/my_dataset"
}
```

---

### List Datasets
```http
GET /datasets/
```

**Response:**
```json
{
  "datasets": [
    {
      "name": "glioma",
      "image_count": 826,
      "path": "./Dataset/glioma"
    }
  ]
}
```

---

### Start Training
```http
POST /train/
```

**Request Body:**
```json
{
  "dataset_name": "glioma",
  "epochs": 50,
  "batch_size": 32,
  "learning_rate": 0.0002,
  "image_size": 128
}
```

**Response:**
```json
{
  "message": "Training started",
  "config": {
    "dataset_name": "glioma",
    "epochs": 50,
    "batch_size": 32,
    "learning_rate": 0.0002,
    "image_size": 128
  }
}
```

---

### Get Training Status
```http
GET /training-status/
```

**Response:**
```json
{
  "is_training": true,
  "current_epoch": 25,
  "total_epochs": 50,
  "gen_loss": 0.8234,
  "disc_loss": 0.6721
}
```

---

### Generate Images
```http
POST /generate/
```

**Request Body:**
```json
{
  "num_samples": 16,
  "model_path": "./models/checkpoints/epoch_50"
}
```

**Response:**
```json
{
  "message": "Generated 16 samples",
  "output_dir": "./Synthetic Data/20240101_120000"
}
```

---

### List Trained Models
```http
GET /models/
```

**Response:**
```json
{
  "models": [
    {
      "name": "epoch_50",
      "path": "./models/checkpoints/epoch_50"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Training already in progress"
}
```

### 404 Not Found
```json
{
  "detail": "Model not found. Train a model first."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error message here"
}
```

---

## Example Usage

### Python Requests

```python
import requests

# Upload dataset
files = [('files', open('image1.jpg', 'rb'))]
response = requests.post(
    'http://localhost:8000/upload-dataset/?dataset_name=my_dataset',
    files=files
)
print(response.json())

# Start training
config = {
    "dataset_name": "my_dataset",
    "epochs": 50,
    "batch_size": 32,
    "learning_rate": 0.0002,
    "image_size": 128
}
response = requests.post('http://localhost:8000/train/', json=config)
print(response.json())

# Check status
response = requests.get('http://localhost:8000/training-status/')
print(response.json())

# Generate images
generate_config = {
    "num_samples": 16,
    "model_path": "./models/checkpoints/epoch_50"
}
response = requests.post('http://localhost:8000/generate/', json=generate_config)
print(response.json())
```

### cURL

```bash
# Health check
curl http://localhost:8000/

# List datasets
curl http://localhost:8000/datasets/

# Start training
curl -X POST http://localhost:8000/train/ \
  -H "Content-Type: application/json" \
  -d '{"dataset_name":"glioma","epochs":50,"batch_size":32,"learning_rate":0.0002,"image_size":128}'

# Training status
curl http://localhost:8000/training-status/

# Generate images
curl -X POST http://localhost:8000/generate/ \
  -H "Content-Type: application/json" \
  -d '{"num_samples":16,"model_path":"./models/checkpoints/epoch_50"}'
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation with:
- Try it out functionality
- Request/response schemas
- Authentication testing
- Real-time testing
