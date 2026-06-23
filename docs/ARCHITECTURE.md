# System Architecture

## Overview

The Synthetic Data Generation Platform follows a clean, modular architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│                      (Streamlit Web UI)                      │
│  ┌─────────┬──────────┬──────────┬──────────┬────────────┐ │
│  │  Home   │ Dataset  │ Training │ Generate │ Evaluation │ │
│  └─────────┴──────────┴──────────┴──────────┴────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST API
┌────────────────────────┴────────────────────────────────────┐
│                         API Layer                            │
│                       (FastAPI Backend)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoints: /upload, /train, /generate, /status      │  │
│  └──────────────────────────────────────────────────────┘  │
└──┬─────────┬─────────┬──────────┬──────────┬───────────────┘
   │         │         │          │          │
   ▼         ▼         ▼          ▼          ▼
┌─────┐ ┌────────┐ ┌────────┐ ┌─────────┐ ┌─────────┐
│Data │ │ Model  │ │Training│ │Evaluate │ │Database │
│Layer│ │ Layer  │ │ Layer  │ │ Layer   │ │ Layer   │
└─────┘ └────────┘ └────────┘ └─────────┘ └─────────┘
```

## Layers

### 1. Frontend Layer (Streamlit)
- **Location**: `frontend/app.py`
- **Purpose**: User interface and interaction
- **Components**:
  - Home dashboard
  - Dataset manager
  - Training interface
  - Generation interface
  - Evaluation dashboard

### 2. API Layer (FastAPI)
- **Location**: `src/api/main.py`
- **Purpose**: REST API endpoints and business logic
- **Endpoints**:
  - Dataset upload
  - Training control
  - Status monitoring
  - Image generation
  - Model management

### 3. Model Layer
- **Location**: `src/models/dcgan.py`
- **Purpose**: Deep learning model definitions
- **Components**:
  - DCGAN Generator
  - DCGAN Discriminator
  - Model persistence

### 4. Training Layer
- **Location**: `src/training/trainer.py`
- **Purpose**: Training logic and optimization
- **Features**:
  - Training loop
  - Loss calculation
  - Checkpoint management
  - Progress tracking

### 5. Data Layer
- **Location**: `src/data/preprocessor.py`
- **Purpose**: Data loading and preprocessing
- **Functions**:
  - Image loading
  - Normalization
  - Data augmentation
  - Dataset statistics

### 6. Evaluation Layer
- **Location**: `src/evaluation/metrics.py`
- **Purpose**: Model evaluation
- **Metrics**:
  - FID Score
  - SSIM
  - PSNR

### 7. Database Layer
- **Location**: `src/utils/database.py`
- **Purpose**: Data persistence
- **Tables**:
  - training_runs
  - generated_images
  - evaluation_metrics
  - datasets
  - activity_logs

## Data Flow

### Training Flow
```
1. User uploads dataset → Frontend
2. Frontend sends to API → /upload-dataset/
3. API stores in Dataset/ folder
4. User configures training → Frontend
5. Frontend triggers training → /train/
6. API creates DCGAN model
7. Trainer loads dataset
8. Training loop executes
9. Checkpoints saved periodically
10. Status updates via /training-status/
11. Frontend polls and displays progress
```

### Generation Flow
```
1. User selects model → Frontend
2. User sets num_samples → Frontend
3. Frontend requests generation → /generate/
4. API loads trained model
5. Generator creates synthetic images
6. Images saved to Synthetic Data/
7. API returns output directory
8. Frontend displays results
```

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **ML/DL**: TensorFlow 2.15, Keras
- **Database**: SQLite with SQLAlchemy ORM
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib
- **HTTP Client**: Requests library

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (ready)

## Design Patterns

### 1. Repository Pattern
Database access through centralized repository in `database.py`

### 2. Service Layer Pattern
Business logic in API layer, separate from models

### 3. Factory Pattern
Model creation through configuration

### 4. Observer Pattern
Training status updates via polling

### 5. Singleton Pattern
Database connection management

## Security Considerations

1. **Input Validation**: File type and size checks
2. **SQL Injection**: SQLAlchemy parameterized queries
3. **Path Traversal**: Restricted file paths
4. **Rate Limiting**: (To be implemented)
5. **Authentication**: (To be implemented)

## Scalability

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Background task processing

### Vertical Scaling
- GPU acceleration support
- Batch processing
- Efficient tensor operations

## Deployment Architecture

### Development
```
localhost:8000 → API
localhost:8501 → Frontend
```

### Production (Docker)
```
Container 1: API (Port 8000)
Container 2: Frontend (Port 8501)
Shared Volumes: Dataset, Models, Database
```

### Cloud (AWS Example)
```
EC2/ECS → Docker Containers
S3 → Dataset Storage
RDS → Database (optional)
CloudWatch → Logging
```

## Configuration Management

- Environment variables via `.env`
- Settings managed by `config/settings.py`
- Pydantic validation
- Default values provided

## Error Handling

1. **Frontend**: Try-catch with user-friendly messages
2. **API**: HTTPException with status codes
3. **Training**: Graceful failure with state reset
4. **Database**: Transaction rollback on errors

## Logging Strategy

- **Application Logs**: `logs/app.log`
- **Training Logs**: Console output
- **API Logs**: Uvicorn access logs
- **Error Logs**: `logs/error.log`

## Testing Strategy

- **Unit Tests**: Individual functions
- **Integration Tests**: API endpoints
- **End-to-End Tests**: Complete workflows
- **Performance Tests**: Training speed, memory usage

## Future Enhancements

1. **Model Versioning**: MLflow integration
2. **Experiment Tracking**: Weights & Biases
3. **Advanced Models**: StyleGAN, ProGAN
4. **Real-time Updates**: WebSocket for training
5. **Authentication**: JWT-based auth
6. **Cloud Storage**: S3/Azure Blob integration
7. **Distributed Training**: Multi-GPU support
8. **API Rate Limiting**: Redis-based limiter
