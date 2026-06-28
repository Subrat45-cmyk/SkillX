import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from typing import Tuple, Dict, Any
import os
from config import settings

class DataPreprocessor:
    """Handle data preprocessing for AQI prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'temperature', 'humidity', 'wind_speed', 'rainfall', 'pressure',
            'pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'ndvi', 'lst',
            'population_density', 'traffic_index'
        ]
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load data from CSV"""
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        raise ValueError("Unsupported file format")
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """Handle missing values"""
        if strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'drop':
            df = df.dropna()
        return df
    
    def remove_outliers(self, df: pd.DataFrame, columns: list = None, method: str = 'iqr') -> pd.DataFrame:
        """Remove outliers using IQR or Z-score"""
        if columns is None:
            columns = self.feature_columns
        
        columns = [col for col in columns if col in df.columns]
        
        if method == 'iqr':
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(df[columns]))
            df = df[(z_scores < 3).all(axis=1)]
        
        return df
    
    def normalize_features(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Normalize features using StandardScaler"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col in self.feature_columns]
        
        if numeric_cols:
            if fit:
                df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
            else:
                df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Encode categorical variables"""
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if fit:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            else:
                if col in self.label_encoders:
                    df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def preprocess(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Complete preprocessing pipeline"""
        df = df.copy()
        df = self.handle_missing_values(df, strategy='mean')
        df = self.remove_outliers(df, method='iqr')
        df = self.encode_categorical(df, fit=fit)
        df = self.normalize_features(df, fit=fit)
        return df
    
    def split_data(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
        """Split data into train and test sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def save_scaler(self, path: str = None):
        """Save fitted scaler"""
        if path is None:
            path = os.path.join(settings.scaler_path, 'scaler.joblib')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.scaler, path)
    
    def load_scaler(self, path: str = None):
        """Load scaler"""
        if path is None:
            path = os.path.join(settings.scaler_path, 'scaler.joblib')
        self.scaler = joblib.load(path)
    
    def save_encoders(self, path: str = None):
        """Save label encoders"""
        if path is None:
            path = os.path.join(settings.scaler_path, 'encoders.joblib')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.label_encoders, path)
    
    def load_encoders(self, path: str = None):
        """Load label encoders"""
        if path is None:
            path = os.path.join(settings.scaler_path, 'encoders.joblib')
        self.label_encoders = joblib.load(path)
