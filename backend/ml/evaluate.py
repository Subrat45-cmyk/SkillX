import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Tuple, Any
import json
import os
from config import settings

class ModelEvaluator:
    """Evaluate model performance"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_metrics(self, y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate evaluation metrics"""
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        metrics = {
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'mape': float(mape),
            'mse': float(mse)
        }
        
        return metrics
    
    def evaluate_model(self, model, X_test: pd.DataFrame, y_test: pd.Series, model_name: str = 'model') -> Dict:
        """Evaluate model on test set"""
        y_pred = model.predict(X_test)
        metrics = self.calculate_metrics(y_test, y_pred)
        
        self.metrics[model_name] = metrics
        return metrics
    
    def compare_models(self, models: Dict, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """Compare multiple models"""
        comparison = {}
        
        for model_name, model in models.items():
            metrics = self.evaluate_model(model, X_test, y_test, model_name)
            comparison[model_name] = metrics
        
        return comparison
    
    def generate_confusion_matrix(self, y_true: pd.Series, y_pred: np.ndarray, labels: list = None):
        """Generate confusion matrix for classification"""
        from sklearn.metrics import confusion_matrix
        
        cm = confusion_matrix(y_true, y_pred)
        return cm.tolist()
    
    def generate_classification_report(self, y_true: pd.Series, y_pred: np.ndarray):
        """Generate classification report"""
        from sklearn.metrics import classification_report
        
        report = classification_report(y_true, y_pred, output_dict=True)
        return report
    
    def save_metrics(self, model_name: str, metrics: Dict, path: str = None):
        """Save metrics to file"""
        if path is None:
            path = os.path.join(settings.model_path, f'{model_name}_metrics.json')
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(metrics, f, indent=4)
    
    def print_metrics(self, metrics: Dict):
        """Print metrics in readable format"""
        print("\n=== Model Evaluation Metrics ===")
        for metric_name, metric_value in metrics.items():
            print(f"{metric_name.upper()}: {metric_value:.4f}")
        print("="*32)
