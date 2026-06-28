import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.model_selection import cross_val_score, GridSearchCV
import joblib
import json
from typing import Dict, Tuple, Any
import os
from config import settings

class ModelTrainer:
    """Train and manage ML models for AQI prediction"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.model_scores = {}
    
    def train_random_forest(self, X_train: pd.DataFrame, y_train: pd.Series, **kwargs) -> Tuple[RandomForestRegressor, Dict]:
        """Train Random Forest model"""
        params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'max_depth': kwargs.get('max_depth', 20),
            'min_samples_split': kwargs.get('min_samples_split', 5),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 2),
            'n_jobs': settings.n_jobs,
            'random_state': settings.random_state,
            'verbose': 0
        }
        
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)
        
        # Calculate cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        scores = {
            'model_type': 'Random Forest',
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'train_score': float(model.score(X_train, y_train))
        }
        
        return model, scores
    
    def train_xgboost(self, X_train: pd.DataFrame, y_train: pd.Series, **kwargs) -> Tuple[xgb.XGBRegressor, Dict]:
        """Train XGBoost model"""
        params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'max_depth': kwargs.get('max_depth', 6),
            'learning_rate': kwargs.get('learning_rate', 0.1),
            'subsample': kwargs.get('subsample', 0.8),
            'colsample_bytree': kwargs.get('colsample_bytree', 0.8),
            'random_state': settings.random_state,
            'n_jobs': settings.n_jobs,
            'verbosity': 0
        }
        
        model = xgb.XGBRegressor(**params)
        model.fit(X_train, y_train, verbose=False)
        
        # Calculate cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        scores = {
            'model_type': 'XGBoost',
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'train_score': float(model.score(X_train, y_train))
        }
        
        return model, scores
    
    def train_all_models(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict:
        """Train all models"""
        print("Training Random Forest...")
        rf_model, rf_scores = self.train_random_forest(X_train, y_train)
        self.models['random_forest'] = rf_model
        self.model_scores['random_forest'] = rf_scores
        
        print("Training XGBoost...")
        xgb_model, xgb_scores = self.train_xgboost(X_train, y_train)
        self.models['xgboost'] = xgb_model
        self.model_scores['xgboost'] = xgb_scores
        
        return self.model_scores
    
    def select_best_model(self) -> str:
        """Select best model based on CV scores"""
        best_score = -np.inf
        best_model = None
        
        for model_name, scores in self.model_scores.items():
            if scores['cv_mean'] > best_score:
                best_score = scores['cv_mean']
                best_model = model_name
        
        self.best_model = self.models[best_model]
        self.best_model_name = best_model
        
        print(f"Best model selected: {best_model} with CV score: {best_score:.4f}")
        return best_model
    
    def save_model(self, model_name: str = None, path: str = None):
        """Save trained model"""
        if model_name is None:
            model_name = self.best_model_name
        
        if path is None:
            path = os.path.join(settings.model_path, f'{model_name}_model.joblib')
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.models[model_name], path)
        print(f"Model saved to {path}")
    
    def load_model(self, model_name: str, path: str = None):
        """Load trained model"""
        if path is None:
            path = os.path.join(settings.model_path, f'{model_name}_model.joblib')
        
        self.models[model_name] = joblib.load(path)
        self.best_model = self.models[model_name]
        self.best_model_name = model_name
        print(f"Model loaded from {path}")
    
    def save_model_metadata(self, metadata: Dict, path: str = None):
        """Save model metadata"""
        if path is None:
            path = os.path.join(settings.model_path, 'metadata.json')
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(metadata, f, indent=4)
    
    def get_feature_importance(self, model_name: str = None) -> Dict:
        """Get feature importance from model"""
        if model_name is None:
            model = self.best_model
        else:
            model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            return dict(zip(range(len(model.feature_importances_)), model.feature_importances_))
        else:
            return {}
