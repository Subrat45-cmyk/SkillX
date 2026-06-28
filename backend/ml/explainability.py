import shap
import numpy as np
import pandas as pd
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class ExplainabilityEngine:
    """Generate SHAP-based explanations for predictions"""
    
    def __init__(self, model, X_train: pd.DataFrame):
        self.model = model
        self.explainer = shap.TreeExplainer(model)
        self.X_train = X_train
        self.shap_values = None
    
    def explain_prediction(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Generate SHAP explanation for a single prediction"""
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary/multi-class, use positive class
        
        explanation = {
            'base_value': float(self.explainer.expected_value),
            'feature_importance': {},
            'feature_contributions': []
        }
        
        # Get feature importance
        for i, (feature, shap_val) in enumerate(zip(X.columns, shap_values[0])):
            explanation['feature_importance'][feature] = float(shap_val)
            explanation['feature_contributions'].append({
                'feature': feature,
                'shap_value': float(shap_val),
                'feature_value': float(X.iloc[0, i]),
                'direction': 'positive' if shap_val > 0 else 'negative'
            })
        
        # Sort by absolute shap value
        explanation['feature_contributions'].sort(
            key=lambda x: abs(x['shap_value']),
            reverse=True
        )
        
        return explanation
    
    def get_feature_importance(self, num_features: int = 10) -> Dict[str, float]:
        """Get global feature importance"""
        shap_values = self.explainer.shap_values(self.X_train)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Calculate mean absolute SHAP values
        mean_shap = np.abs(shap_values).mean(axis=0)
        
        feature_importance = {}
        for i, feature in enumerate(self.X_train.columns):
            feature_importance[feature] = float(mean_shap[i])
        
        # Sort and return top features
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return dict(sorted_features[:num_features])
    
    def generate_summary_plot(self) -> str:
        """Generate SHAP summary plot as base64 image"""
        shap_values = self.explainer.shap_values(self.X_train)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, self.X_train, show=False)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return image_base64
    
    def generate_force_plot(self, X: pd.DataFrame, index: int = 0) -> str:
        """Generate SHAP force plot as HTML"""
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        force_plot = shap.force_plot(
            self.explainer.expected_value,
            shap_values[index],
            X.iloc[index],
            show=False
        )
        
        return force_plot.to_html()
