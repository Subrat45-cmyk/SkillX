import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any

class FeatureEngineer:
    """Create and engineer features for AQI prediction"""
    
    def __init__(self):
        self.feature_names = []
    
    def create_rolling_features(self, df: pd.DataFrame, columns: List[str], windows: List[int] = [3, 7, 14]) -> pd.DataFrame:
        """Create rolling window features"""
        for col in columns:
            if col in df.columns:
                for window in windows:
                    df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window, min_periods=1).mean()
                    df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window, min_periods=1).std()
                    self.feature_names.extend([f'{col}_rolling_mean_{window}', f'{col}_rolling_std_{window}'])
        return df
    
    def create_lag_features(self, df: pd.DataFrame, columns: List[str], lags: List[int] = [1, 3, 7]) -> pd.DataFrame:
        """Create lagged features"""
        for col in columns:
            if col in df.columns:
                for lag in lags:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
                    self.feature_names.append(f'{col}_lag_{lag}')
        return df
    
    def create_interaction_features(self, df: pd.DataFrame, feature_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create interaction features"""
        for col1, col2 in feature_pairs:
            if col1 in df.columns and col2 in df.columns:
                feature_name = f'{col1}_x_{col2}'
                df[feature_name] = df[col1] * df[col2]
                self.feature_names.append(feature_name)
        return df
    
    def create_ratio_features(self, df: pd.DataFrame, feature_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create ratio features"""
        for col1, col2 in feature_pairs:
            if col1 in df.columns and col2 in df.columns and (df[col2] != 0).all():
                feature_name = f'{col1}_ratio_{col2}'
                df[feature_name] = df[col1] / (df[col2] + 1e-8)  # Avoid division by zero
                self.feature_names.append(feature_name)
        return df
    
    def create_polynomial_features(self, df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
        """Create polynomial features"""
        for col in columns:
            if col in df.columns:
                for d in range(2, degree + 1):
                    feature_name = f'{col}_pow_{d}'
                    df[feature_name] = df[col] ** d
                    self.feature_names.append(feature_name)
        return df
    
    def create_statistical_features(self, df: pd.DataFrame, columns: List[str], windows: List[int] = [3, 7]) -> pd.DataFrame:
        """Create statistical features like min, max, skew"""
        for col in columns:
            if col in df.columns:
                for window in windows:
                    df[f'{col}_min_{window}'] = df[col].rolling(window=window, min_periods=1).min()
                    df[f'{col}_max_{window}'] = df[col].rolling(window=window, min_periods=1).max()
                    df[f'{col}_median_{window}'] = df[col].rolling(window=window, min_periods=1).median()
                    self.feature_names.extend([
                        f'{col}_min_{window}',
                        f'{col}_max_{window}',
                        f'{col}_median_{window}'
                    ])
        return df
    
    def create_time_features(self, df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
        """Create time-based features"""
        if date_column in df.columns:
            df['date'] = pd.to_datetime(df[date_column])
            df['day_of_week'] = df['date'].dt.dayofweek
            df['month'] = df['date'].dt.month
            df['quarter'] = df['date'].dt.quarter
            df['day_of_year'] = df['date'].dt.dayofyear
            df['week_of_year'] = df['date'].dt.isocalendar().week
            
            self.feature_names.extend([
                'day_of_week', 'month', 'quarter', 'day_of_year', 'week_of_year'
            ])
        return df
    
    def create_geo_features(self, df: pd.DataFrame, lat_col: str = 'latitude', lon_col: str = 'longitude') -> pd.DataFrame:
        """Create geographic features"""
        if lat_col in df.columns and lon_col in df.columns:
            # Distance from city center (example: Delhi at 28.6139°N, 77.2090°E)
            center_lat, center_lon = 28.6139, 77.2090
            df['dist_from_center'] = np.sqrt(
                (df[lat_col] - center_lat)**2 + (df[lon_col] - center_lon)**2
            )
            
            # Quadrant encoding
            df['quadrant'] = 0
            df.loc[(df[lat_col] >= center_lat) & (df[lon_col] >= center_lon), 'quadrant'] = 1
            df.loc[(df[lat_col] >= center_lat) & (df[lon_col] < center_lon), 'quadrant'] = 2
            df.loc[(df[lat_col] < center_lat) & (df[lon_col] < center_lon), 'quadrant'] = 3
            df.loc[(df[lat_col] < center_lat) & (df[lon_col] >= center_lon), 'quadrant'] = 4
            
            self.feature_names.extend(['dist_from_center', 'quadrant'])
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Complete feature engineering pipeline"""
        df = df.copy()
        
        # Pollutant columns
        pollutants = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        weather = ['temperature', 'humidity', 'wind_speed', 'pressure']
        
        # Create features
        df = self.create_time_features(df)
        df = self.create_geo_features(df)
        df = self.create_rolling_features(df, pollutants + weather)
        df = self.create_lag_features(df, pollutants)
        df = self.create_interaction_features(df, [('wind_speed', 'temperature'), ('humidity', 'pressure')])
        df = self.create_ratio_features(df, [('pm25', 'pm10'), ('no2', 'so2')])
        df = self.create_polynomial_features(df, ['temperature', 'humidity'], degree=2)
        df = self.create_statistical_features(df, pollutants)
        
        # Fill NaN values created by rolling/lag operations
        df = df.fillna(df.mean())
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get all engineered feature names"""
        return self.feature_names
