import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Any, List, Tuple
from config import settings
from preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer

class AQIPredictor:
    """Make AQI predictions using trained models"""
    
    def __init__(self, model_name: str = 'xgboost'):
        self.model = None
        self.preprocessor = DataPreprocessor()
        self.feature_engineer = FeatureEngineer()
        self.scaler = None
        self.model_name = model_name
        self.feature_names = []
        self._load_components()
    
    def _load_components(self):
        """Load model and preprocessing components"""
        try:
            # Load model
            model_path = os.path.join(settings.model_path, f'{self.model_name}_model.joblib')
            self.model = joblib.load(model_path)
            
            # Load scaler
            scaler_path = os.path.join(settings.scaler_path, 'scaler.joblib')
            self.preprocessor.load_scaler(scaler_path)
            
            # Load encoders
            encoders_path = os.path.join(settings.scaler_path, 'encoders.joblib')
            self.preprocessor.load_encoders(encoders_path)
            
            print(f"Loaded {self.model_name} model successfully")
        except FileNotFoundError:
            print(f"Model or components not found. Please train the model first.")
    
    def preprocess_input(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess input data"""
        df = pd.DataFrame([data])
        df = self.preprocessor.encode_categorical(df, fit=False)
        df = self.preprocessor.normalize_features(df, fit=False)
        return df
    
    def predict_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make single prediction"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        df = self.preprocess_input(data)
        prediction = self.model.predict(df)
        
        # Get prediction confidence (if available)
        confidence = None
        if hasattr(self.model, 'predict_proba'):
            confidence = np.max(self.model.predict_proba(df))
        
        return {
            'aqi_value': float(prediction[0]),
            'confidence': float(confidence) if confidence else 0.0,
            'aqi_category': self._categorize_aqi(prediction[0])
        }
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make batch predictions"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        df = pd.DataFrame(data_list)
        df = self.preprocessor.encode_categorical(df, fit=False)
        df = self.preprocessor.normalize_features(df, fit=False)
        
        predictions = self.model.predict(df)
        
        results = []
        for pred in predictions:
            results.append({
                'aqi_value': float(pred),
                'aqi_category': self._categorize_aqi(pred)
            })
        
        return results
    
    def predict_with_confidence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction with confidence interval"""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        df = self.preprocess_input(data)
        prediction = self.model.predict(df)
        
        # Estimate confidence interval (±10% for now)
        lower_bound = prediction[0] * 0.9
        upper_bound = prediction[0] * 1.1
        
        return {
            'aqi_value': float(prediction[0]),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'aqi_category': self._categorize_aqi(prediction[0])
        }
    
    @staticmethod
    def _categorize_aqi(aqi_value: float) -> str:
        """Categorize AQI value"""
        if aqi_value <= 50:
            return 'Good'
        elif aqi_value <= 100:
            return 'Satisfactory'
        elif aqi_value <= 200:
            return 'Moderately Polluted'
        elif aqi_value <= 300:
            return 'Poor'
        elif aqi_value <= 400:
            return 'Very Poor'
        else:
            return 'Severe'
    
    def explain_prediction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Explain prediction using SHAP (if available)"""
        try:
            import shap
            
            df = self.preprocess_input(data)
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(df)
            
            feature_importance = {}
            for i, val in enumerate(shap_values[0]):
                feature_importance[f'feature_{i}'] = float(val)
            
            return {
                'feature_importance': feature_importance,
                'base_value': float(explainer.expected_value)
            }
        except ImportError:
            return {'error': 'SHAP not installed'}
