from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Any
from datetime import datetime

# Input Schemas
class PredictionInput(BaseModel):
    """Schema for AQI prediction input"""
    temperature: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(..., ge=0, le=100, description="Wind speed in km/h")
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")
    pressure: float = Field(..., ge=800, le=1200, description="Atmospheric pressure in hPa")
    pm25: float = Field(..., ge=0, description="PM2.5 concentration in µg/m³")
    pm10: float = Field(..., ge=0, description="PM10 concentration in µg/m³")
    no2: float = Field(..., ge=0, description="NO2 concentration in ppb")
    so2: float = Field(..., ge=0, description="SO2 concentration in ppb")
    co: float = Field(..., ge=0, description="CO concentration in ppm")
    o3: float = Field(..., ge=0, description="O3 concentration in ppb")
    ndvi: Optional[float] = Field(None, ge=-1, le=1, description="Normalized Difference Vegetation Index")
    lst: Optional[float] = Field(None, description="Land Surface Temperature")
    population_density: Optional[float] = Field(None, ge=0, description="Population density per sq km")
    traffic_index: Optional[float] = Field(None, ge=0, le=100, description="Traffic congestion index")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of measurement")

class BatchPredictionInput(BaseModel):
    """Schema for batch predictions"""
    predictions: List[PredictionInput]

class TrainingDataPoint(BaseModel):
    """Schema for training data point"""
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float
    pressure: float
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    historical_aqi: float = Field(..., ge=0, le=500, description="Historical AQI value")
    ndvi: Optional[float] = None
    lst: Optional[float] = None
    population_density: Optional[float] = None
    traffic_index: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class TrainingRequest(BaseModel):
    """Schema for training request"""
    data: List[TrainingDataPoint]
    test_size: float = Field(0.2, ge=0.1, le=0.5)
    model_type: str = Field("both", description="Model type: 'random_forest', 'xgboost', or 'both'")

class LocationInput(BaseModel):
    """Schema for location-based queries"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(5, ge=1, le=100, description="Search radius in kilometers")

class HotspotInput(BaseModel):
    """Schema for hotspot detection"""
    locations: List[LocationInput]
    aqi_values: List[float]
    eps: float = Field(0.05, ge=0.01, le=1, description="DBSCAN epsilon parameter")
    min_samples: int = Field(5, ge=2, le=20, description="DBSCAN min_samples parameter")

# Output Schemas
class PredictionOutput(BaseModel):
    """Schema for prediction output"""
    aqi_value: float = Field(..., description="Predicted AQI value")
    aqi_category: str = Field(..., description="AQI category (Good, Satisfactory, etc.)")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    lower_bound: Optional[float] = Field(None, description="Lower confidence bound")
    upper_bound: Optional[float] = Field(None, description="Upper confidence bound")
    health_advisory: str = Field(..., description="Health advisory for current AQI")
    timestamp: datetime = Field(default_factory=datetime.now)

class BatchPredictionOutput(BaseModel):
    """Schema for batch prediction output"""
    predictions: List[PredictionOutput]
    total: int
    successful: int
    failed: int

class ModelInfo(BaseModel):
    """Schema for model information"""
    model_type: str
    cv_score: float
    r2_score: float
    rmse: float
    mae: float
    feature_count: int
    training_samples: int

class HistoryEntry(BaseModel):
    """Schema for prediction history"""
    id: str
    prediction: PredictionOutput
    input_data: PredictionInput
    created_at: datetime

class WeatherData(BaseModel):
    """Schema for weather data"""
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float
    pressure: float
    timestamp: datetime
    location: str

class AQIData(BaseModel):
    """Schema for AQI data"""
    aqi_value: float
    category: str
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    timestamp: datetime
    location: str
    latitude: float
    longitude: float

class Hotspot(BaseModel):
    """Schema for hotspot"""
    id: str
    latitude: float
    longitude: float
    severity: float = Field(..., ge=0, le=1, description="Severity score 0-1")
    point_count: int = Field(..., description="Number of points in hotspot")
    average_aqi: float
    priority_rank: int
    recommended_actions: List[str]

class Recommendation(BaseModel):
    """Schema for recommendation"""
    type: str = Field(..., description="Type of recommendation")
    priority: str = Field(..., description="Priority level: low, medium, high")
    description: str
    reason: str
    confidence: float = Field(..., ge=0, le=1)
    estimated_impact: str = Field(..., description="Estimated impact on AQI")
    implementation_cost: str = Field(..., description="Cost estimate: low, medium, high")

class FeatureImportance(BaseModel):
    """Schema for feature importance"""
    feature_name: str
    importance_score: float
    contribution_to_prediction: float
    direction: str = Field(..., description="positive or negative contribution")

class PredictionExplanation(BaseModel):
    """Schema for prediction explanation"""
    base_value: float
    prediction_value: float
    feature_importance: List[FeatureImportance]
    contributing_factors: List[str]
    model_confidence: float

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: str
    timestamp: datetime = Field(default_factory=datetime.now)

class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)
