from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/aqi_vision')
    
    # API
    api_host: str = os.getenv('API_HOST', '0.0.0.0')
    api_port: int = int(os.getenv('API_PORT', 8000))
    api_debug: bool = os.getenv('API_DEBUG', 'false').lower() == 'true'
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    algorithm: str = os.getenv('ALGORITHM', 'HS256')
    access_token_expire_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    
    # Environment
    environment: str = os.getenv('ENVIRONMENT', 'development')
    
    # Paths
    model_path: str = os.getenv('MODEL_PATH', './data/models')
    scaler_path: str = os.getenv('SCALER_PATH', './data/scalers')
    
    # API Keys
    satellite_api_key: str = os.getenv('SATELLITE_API_KEY', '')
    nasa_api_key: str = os.getenv('NASA_API_KEY', '')
    
    # Frontend
    frontend_url: str = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # ML Configuration
    test_split: float = 0.2
    random_state: int = 42
    n_jobs: int = -1
    
    # Hotspot Detection
    dbscan_eps: float = 0.05
    dbscan_min_samples: int = 5
    
    class Config:
        env_file = '.env'
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
