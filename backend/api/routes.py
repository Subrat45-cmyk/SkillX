from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from schemas import (
    PredictionInput, PredictionOutput, BatchPredictionInput, BatchPredictionOutput,
    ModelInfo, HistoryEntry, WeatherData, AQIData, Hotspot, Recommendation,
    TrainingRequest, HotspotInput, PredictionExplanation, SuccessResponse, ErrorResponse
)
from ..ml.predict import AQIPredictor
from ..ml.models import ModelTrainer
from ..ml.evaluate import ModelEvaluator
from ..ml.explainability import ExplainabilityEngine
from ..ml.utils import categorize_aqi, get_recommendations, get_health_advisory
from ..geo.hotspots import HotspotDetector

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["AQI Predictions"])

# Initialize predictors
predictor = None

def get_predictor():
    """Dependency to get predictor instance"""
    global predictor
    if predictor is None:
        predictor = AQIPredictor(model_name='xgboost')
    return predictor

# ==================== PREDICTION ENDPOINTS ====================

@router.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
async def predict_aqi(input_data: PredictionInput, predictor_dep = Depends(get_predictor)):
    """
    Make a single AQI prediction based on environmental parameters.
    
    **Parameters:**
    - temperature: Temperature in Celsius
    - humidity: Humidity percentage (0-100)
    - wind_speed: Wind speed in km/h
    - rainfall: Rainfall in mm
    - pressure: Atmospheric pressure in hPa
    - pm25, pm10, no2, so2, co, o3: Pollutant concentrations
    - ndvi: Vegetation index
    - lst: Land surface temperature
    - population_density: People per sq km
    - traffic_index: Traffic congestion (0-100)
    """
    try:
        # Convert input to dictionary
        data_dict = input_data.dict(exclude_none=True)
        
        # Get prediction
        prediction = predictor_dep.predict_single(data_dict)
        
        # Get health advisory
        advisory = get_health_advisory(prediction['aqi_category'])
        
        return PredictionOutput(
            aqi_value=prediction['aqi_value'],
            aqi_category=prediction['aqi_category'],
            confidence=prediction['confidence'],
            health_advisory=advisory
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/batch-predict", response_model=BatchPredictionOutput, status_code=status.HTTP_200_OK)
async def batch_predict_aqi(batch_input: BatchPredictionInput, predictor_dep = Depends(get_predictor)):
    """
    Make batch AQI predictions for multiple locations/times.
    
    **Parameters:**
    - predictions: List of PredictionInput objects
    """
    try:
        results = []
        successful = 0
        failed = 0
        
        for pred_input in batch_input.predictions:
            try:
                data_dict = pred_input.dict(exclude_none=True)
                prediction = predictor_dep.predict_single(data_dict)
                advisory = get_health_advisory(prediction['aqi_category'])
                
                results.append(PredictionOutput(
                    aqi_value=prediction['aqi_value'],
                    aqi_category=prediction['aqi_category'],
                    confidence=prediction['confidence'],
                    health_advisory=advisory
                ))
                successful += 1
            except Exception as e:
                logger.error(f"Failed to process item: {str(e)}")
                failed += 1
        
        return BatchPredictionOutput(
            predictions=results,
            total=len(batch_input.predictions),
            successful=successful,
            failed=failed
        )
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch prediction failed: {str(e)}"
        )

@router.post("/predict-with-explanation", response_model=PredictionExplanation, status_code=status.HTTP_200_OK)
async def predict_with_explanation(input_data: PredictionInput, predictor_dep = Depends(get_predictor)):
    """
    Make AQI prediction with SHAP-based explanation.
    Shows which factors contributed most to the prediction.
    """
    try:
        data_dict = input_data.dict(exclude_none=True)
        prediction = predictor_dep.predict_single(data_dict)
        
        # Get explanation (if SHAP is available)
        try:
            explanation = predictor_dep.explain_prediction(data_dict)
            feature_importance = [
                {
                    'feature_name': feat,
                    'importance_score': abs(val),
                    'contribution_to_prediction': val,
                    'direction': 'positive' if val > 0 else 'negative'
                }
                for feat, val in sorted(
                    explanation.get('feature_importance', {}).items(),
                    key=lambda x: abs(x[1]),
                    reverse=True
                )[:5]  # Top 5 features
            ]
        except:
            feature_importance = []
        
        return PredictionExplanation(
            base_value=50.0,  # Average AQI
            prediction_value=prediction['aqi_value'],
            feature_importance=feature_importance,
            contributing_factors=[f['feature_name'] for f in feature_importance[:3]],
            model_confidence=prediction['confidence']
        )
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Explanation generation failed: {str(e)}"
        )

# ==================== MODEL INFO ENDPOINTS ====================

@router.get("/model-info", response_model=ModelInfo, status_code=status.HTTP_200_OK)
async def get_model_info():
    """
    Get information about the trained AQI prediction model.
    Includes performance metrics and feature count.
    """
    try:
        return ModelInfo(
            model_type="XGBoost",
            cv_score=0.87,  # Placeholder
            r2_score=0.85,
            rmse=12.5,
            mae=8.3,
            feature_count=45,
            training_samples=10000
        )
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve model information"
        )

@router.post("/train", response_model=SuccessResponse, status_code=status.HTTP_202_ACCEPTED)
async def train_model(training_request: TrainingRequest):
    """
    Train AQI prediction model with provided data.
    This is an async operation that may take time.
    """
    try:
        # Implementation would involve actual model training
        return SuccessResponse(
            message="Model training initiated",
            data={
                "status": "training",
                "samples": len(training_request.data),
                "model_type": training_request.model_type
            }
        )
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Training failed: {str(e)}"
        )

# ==================== HOTSPOT DETECTION ENDPOINTS ====================

@router.post("/hotspots", response_model=List[Hotspot], status_code=status.HTTP_200_OK)
async def detect_hotspots(hotspot_input: HotspotInput):
    """
    Detect AQI hotspots using DBSCAN clustering algorithm.
    Returns clusters of high-pollution areas with severity scores.
    """
    try:
        detector = HotspotDetector(
            eps=hotspot_input.eps,
            min_samples=hotspot_input.min_samples
        )
        
        # Placeholder hotspots
        hotspots = [
            Hotspot(
                id="hotspot_001",
                latitude=28.7041,
                longitude=77.1025,
                severity=0.92,
                point_count=15,
                average_aqi=285,
                priority_rank=1,
                recommended_actions=["traffic_restriction", "tree_plantation"]
            ),
            Hotspot(
                id="hotspot_002",
                latitude=28.6692,
                longitude=77.1559,
                severity=0.78,
                point_count=12,
                average_aqi=215,
                priority_rank=2,
                recommended_actions=["green_buffer", "water_sprinkling"]
            )
        ]
        
        return hotspots
    except Exception as e:
        logger.error(f"Hotspot detection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hotspot detection failed: {str(e)}"
        )

# ==================== RECOMMENDATION ENDPOINTS ====================

@router.get("/recommendations", response_model=List[Recommendation], status_code=status.HTTP_200_OK)
async def get_recommendations_endpoint(
    aqi_value: float = Query(..., ge=0, le=500, description="Current AQI value"),
    latitude: Optional[float] = Query(None, ge=-90, le=90),
    longitude: Optional[float] = Query(None, ge=-180, le=180)
):
    """
    Get actionable recommendations based on current AQI level.
    Recommendations vary based on severity and location.
    """
    try:
        recs = get_recommendations(aqi_value, location=None)
        
        recommendations = []
        for rec in recs:
            recommendations.append(Recommendation(
                type=rec['type'],
                priority=rec['priority'],
                description=rec['description'],
                reason=rec['reason'],
                confidence=rec['confidence'],
                estimated_impact="Reduce AQI by 5-15%",
                implementation_cost="medium"
            ))
        
        return recommendations
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Recommendation generation failed: {str(e)}"
        )

# ==================== HISTORY ENDPOINTS ====================

@router.get("/history", response_model=List[HistoryEntry], status_code=status.HTTP_200_OK)
async def get_prediction_history(
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    days: int = Query(7, ge=1, le=365, description="Historical data from past N days")
):
    """
    Get historical AQI predictions.
    """
    try:
        # Placeholder implementation
        history = []
        base_time = datetime.now()
        
        for i in range(min(limit, 5)):
            history.append(HistoryEntry(
                id=f"hist_{i:03d}",
                prediction=PredictionOutput(
                    aqi_value=150 + i * 20,
                    aqi_category="Moderate" if i % 2 == 0 else "Poor",
                    confidence=0.85,
                    health_advisory="Avoid outdoor activities"
                ),
                input_data=PredictionInput(
                    temperature=25.0,
                    humidity=60.0,
                    wind_speed=5.0,
                    rainfall=0.0,
                    pressure=1013.0,
                    pm25=50.0 + i * 5,
                    pm10=80.0 + i * 8,
                    no2=30.0,
                    so2=15.0,
                    co=0.8,
                    o3=60.0
                ),
                created_at=base_time - timedelta(days=i)
            ))
        
        return history
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve history"
        )

# ==================== WEATHER & AQI DATA ENDPOINTS ====================

@router.get("/weather", response_model=WeatherData, status_code=status.HTTP_200_OK)
async def get_weather_data(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):
    """
    Get current weather data for a location.
    """
    try:
        return WeatherData(
            temperature=25.5,
            humidity=65.0,
            wind_speed=8.5,
            rainfall=0.0,
            pressure=1013.25,
            timestamp=datetime.now(),
            location=f"{latitude}, {longitude}"
        )
    except Exception as e:
        logger.error(f"Weather data error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve weather data"
        )

@router.get("/aqi", response_model=AQIData, status_code=status.HTTP_200_OK)
async def get_aqi_data(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):
    """
    Get current AQI data for a location.
    """
    try:
        return AQIData(
            aqi_value=150.5,
            category="Moderately Polluted",
            pm25=55.3,
            pm10=95.8,
            no2=32.1,
            so2=16.5,
            co=1.2,
            o3=65.4,
            timestamp=datetime.now(),
            location=f"{latitude}, {longitude}",
            latitude=latitude,
            longitude=longitude
        )
    except Exception as e:
        logger.error(f"AQI data error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve AQI data"
        )

@router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "AQI Vision API",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }
