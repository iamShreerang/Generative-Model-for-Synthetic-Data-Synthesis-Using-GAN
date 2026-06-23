from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.settings import settings

Base = declarative_base()

class TrainingRun(Base):
    __tablename__ = "training_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String, nullable=False)
    dataset_name = Column(String, nullable=False)
    epochs = Column(Integer, nullable=False)
    batch_size = Column(Integer, nullable=False)
    learning_rate = Column(Float, nullable=False)
    noise_dim = Column(Integer, nullable=False)
    image_size = Column(Integer, nullable=False)
    status = Column(String, default="initialized")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    generator_loss = Column(Float, nullable=True)
    discriminator_loss = Column(Float, nullable=True)
    model_path = Column(String, nullable=True)
    config = Column(JSON, nullable=True)

class GeneratedImage(Base):
    __tablename__ = "generated_images"
    
    id = Column(Integer, primary_key=True, index=True)
    training_run_id = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)
    epoch = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EvaluationMetric(Base):
    __tablename__ = "evaluation_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    training_run_id = Column(Integer, nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    epoch = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=False)
    image_count = Column(Integer, nullable=False)
    image_size = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    dataset_metadata = Column(JSON, nullable=True)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
