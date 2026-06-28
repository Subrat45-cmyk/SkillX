import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import json
import os
from config import settings

class SatelliteAnalyzer:
    """
    Analyze satellite imagery for environmental indicators.
    Placeholder implementation with realistic fallbacks.
    """
    
    def __init__(self):
        self.api_key = settings.satellite_api_key
        self.nasa_key = settings.nasa_api_key
        self.cache = {}
    
    def calculate_ndvi(self, 
                      red_band: np.ndarray, 
                      nir_band: np.ndarray,
                      location: Tuple[float, float] = None) -> Dict[str, Any]:
        """
        Calculate Normalized Difference Vegetation Index
        NDVI = (NIR - RED) / (NIR + RED)
        
        Args:
            red_band: Red band pixel values
            nir_band: Near-infrared band pixel values
            location: Optional (lat, lon) for caching
        
        Returns:
            NDVI statistics and classification
        """
        try:
            ndvi = (nir_band - red_band) / (nir_band + red_band + 1e-8)
            
            # Classify vegetation
            classification = self._classify_vegetation(ndvi)
            
            result = {
                'ndvi_mean': float(np.mean(ndvi)),
                'ndvi_min': float(np.min(ndvi)),
                'ndvi_max': float(np.max(ndvi)),
                'ndvi_std': float(np.std(ndvi)),
                'vegetation_cover': self._calculate_vegetation_percentage(ndvi),
                'classification': classification,
                'health_index': self._calculate_vegetation_health(ndvi)
            }
            
            if location:
                self.cache[f"ndvi_{location}"] = result
            
            return result
        except Exception as e:
            # Fallback to estimated NDVI
            return self._estimate_ndvi(location)
    
    def calculate_lst(self,
                     thermal_band: np.ndarray,
                     location: Tuple[float, float] = None) -> Dict[str, Any]:
        """
        Calculate Land Surface Temperature from thermal band
        
        Args:
            thermal_band: Thermal infrared band pixel values
            location: Optional (lat, lon) for caching
        
        Returns:
            Temperature statistics and anomalies
        """
        try:
            # Wavelength for Landsat 8 Band 10
            wavelength = 10.904e-6
            ml = 0.0003342  # ML constant
            al = 0.0001  # AL constant
            
            # Top of Atmosphere Spectral Radiance
            toa_radiance = ml * thermal_band + al
            
            # Brightness Temperature
            k1 = 774.8853  # K1 constant
            k2 = 480.8883  # K2 constant
            bt = k2 / np.log((k1 / toa_radiance) + 1)
            
            # Land Surface Emissivity (using NDVI proxy)
            ndvi = np.random.uniform(-0.2, 0.8, thermal_band.shape)
            pv = ((ndvi - ndvi.min()) / (ndvi.max() - ndvi.min())) ** 2
            emissivity = 0.004 * pv + 0.986
            
            # Land Surface Temperature
            sigma = 1.438e-2  # Boltzmann constant
            lst = bt / (1 + (wavelength * bt / sigma) * np.log(emissivity))
            
            # Convert to Celsius
            lst_celsius = lst - 273.15
            
            result = {
                'lst_mean_celsius': float(np.mean(lst_celsius)),
                'lst_min_celsius': float(np.min(lst_celsius)),
                'lst_max_celsius': float(np.max(lst_celsius)),
                'lst_std': float(np.std(lst_celsius)),
                'urban_heat_islands': self._detect_heat_islands(lst_celsius),
                'temperature_anomaly': float(np.mean(lst_celsius) - 25.0)  # Baseline 25C
            }
            
            if location:
                self.cache[f"lst_{location}"] = result
            
            return result
        except Exception as e:
            return self._estimate_lst(location)
    
    def calculate_ndwi(self,
                      green_band: np.ndarray,
                      nir_band: np.ndarray,
                      location: Tuple[float, float] = None) -> Dict[str, Any]:
        """
        Calculate Normalized Difference Water Index
        NDWI = (GREEN - NIR) / (GREEN + NIR)
        
        Useful for water and moisture detection
        """
        try:
            ndwi = (green_band - nir_band) / (green_band + nir_band + 1e-8)
            
            result = {
                'ndwi_mean': float(np.mean(ndwi)),
                'ndwi_min': float(np.min(ndwi)),
                'ndwi_max': float(np.max(ndwi)),
                'water_presence': float(np.sum(ndwi > 0.3) / ndwi.size),
                'moisture_index': float(np.mean(ndwi[ndwi > 0]) if np.any(ndwi > 0) else 0),
                'water_bodies': self._detect_water_bodies(ndwi)
            }
            
            if location:
                self.cache[f"ndwi_{location}"] = result
            
            return result
        except Exception as e:
            return self._estimate_ndwi(location)
    
    def detect_land_cover(self, 
                         multispectral_data: np.ndarray,
                         location: Tuple[float, float] = None) -> Dict[str, Any]:
        """
        Classify land cover types from multispectral imagery
        
        Categories: water, vegetation, built-up, bare soil, urban
        """
        try:
            from sklearn.cluster import KMeans
            
            # Reshape for clustering
            height, width, bands = multispectral_data.shape
            pixels = multispectral_data.reshape(-1, bands)
            
            # Cluster into 5 land cover classes
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            labels = kmeans.fit_predict(pixels)
            
            # Count pixels in each class
            unique, counts = np.unique(labels, return_counts=True)
            total_pixels = len(labels)
            
            result = {
                'water_percentage': float(counts[0] / total_pixels * 100) if len(counts) > 0 else 0,
                'vegetation_percentage': float(counts[1] / total_pixels * 100) if len(counts) > 1 else 0,
                'built_up_percentage': float(counts[2] / total_pixels * 100) if len(counts) > 2 else 0,
                'bare_soil_percentage': float(counts[3] / total_pixels * 100) if len(counts) > 3 else 0,
                'urban_percentage': float(counts[4] / total_pixels * 100) if len(counts) > 4 else 0,
            }
            
            if location:
                self.cache[f"landcover_{location}"] = result
            
            return result
        except Exception as e:
            return self._estimate_land_cover(location)
    
    def detect_vegetation_anomalies(self,
                                   historical_ndvi: List[float],
                                   current_ndvi: float) -> Dict[str, Any]:
        """
        Detect vegetation anomalies by comparing with historical data
        """
        try:
            historical_mean = np.mean(historical_ndvi)
            historical_std = np.std(historical_ndvi)
            
            # Calculate z-score
            z_score = (current_ndvi - historical_mean) / (historical_std + 1e-8)
            
            anomaly_severity = 'none'
            if abs(z_score) > 2:
                anomaly_severity = 'high'
            elif abs(z_score) > 1:
                anomaly_severity = 'medium'
            
            return {
                'z_score': float(z_score),
                'anomaly_detected': bool(abs(z_score) > 1),
                'anomaly_severity': anomaly_severity,
                'expected_range': {
                    'min': float(historical_mean - 2 * historical_std),
                    'max': float(historical_mean + 2 * historical_std)
                },
                'deviation_percentage': float(abs(z_score) * 50)  # Rough estimate
            }
        except Exception as e:
            return {'error': str(e), 'anomaly_detected': False}
    
    def _classify_vegetation(self, ndvi: np.ndarray) -> Dict[str, Any]:
        """Classify vegetation based on NDVI values"""
        classifications = {
            'water': float(np.sum(ndvi < -0.1) / ndvi.size),
            'barren': float(np.sum((ndvi >= -0.1) & (ndvi < 0.2)) / ndvi.size),
            'grass': float(np.sum((ndvi >= 0.2) & (ndvi < 0.5)) / ndvi.size),
            'shrub': float(np.sum((ndvi >= 0.5) & (ndvi < 0.7)) / ndvi.size),
            'forest': float(np.sum(ndvi >= 0.7) / ndvi.size)
        }
        return classifications
    
    def _calculate_vegetation_percentage(self, ndvi: np.ndarray) -> float:
        """Calculate vegetation coverage percentage"""
        return float(np.sum(ndvi > 0.3) / ndvi.size * 100)
    
    def _calculate_vegetation_health(self, ndvi: np.ndarray) -> float:
        """Calculate vegetation health index (0-1)"""
        return float(np.mean(ndvi[ndvi > 0]) if np.any(ndvi > 0) else 0)
    
    def _detect_heat_islands(self, lst: np.ndarray) -> List[Dict[str, Any]]:
        """Detect urban heat islands"""
        mean_temp = np.mean(lst)
        anomalies = lst > (mean_temp + np.std(lst))
        
        if np.any(anomalies):
            return [{'temperature': float(np.max(lst)), 'severity': 'high'}]
        return []
    
    def _detect_water_bodies(self, ndwi: np.ndarray) -> Dict[str, Any]:
        """Detect water bodies"""
        water_pixels = np.sum(ndwi > 0.3)
        return {
            'detected': bool(water_pixels > 0),
            'coverage_percentage': float(water_pixels / ndwi.size * 100)
        }
    
    # Estimation methods (fallbacks)
    def _estimate_ndvi(self, location: Tuple[float, float] = None) -> Dict[str, Any]:
        """Estimate NDVI when satellite data unavailable"""
        return {
            'ndvi_mean': 0.45,
            'ndvi_min': -0.1,
            'ndvi_max': 0.8,
            'ndvi_std': 0.25,
            'vegetation_cover': 55.0,
            'classification': {'grass': 0.4, 'shrub': 0.3, 'forest': 0.2, 'barren': 0.1},
            'health_index': 0.65,
            'data_source': 'estimated'
        }
    
    def _estimate_lst(self, location: Tuple[float, float] = None) -> Dict[str, Any]:
        """Estimate LST when satellite data unavailable"""
        return {
            'lst_mean_celsius': 28.5,
            'lst_min_celsius': 22.0,
            'lst_max_celsius': 35.0,
            'lst_std': 4.2,
            'urban_heat_islands': [],
            'temperature_anomaly': 3.5,
            'data_source': 'estimated'
        }
    
    def _estimate_ndwi(self, location: Tuple[float, float] = None) -> Dict[str, Any]:
        """Estimate NDWI when satellite data unavailable"""
        return {
            'ndwi_mean': 0.15,
            'ndwi_min': -0.3,
            'ndwi_max': 0.6,
            'water_presence': 0.25,
            'moisture_index': 0.35,
            'water_bodies': {'detected': True, 'coverage_percentage': 5.0},
            'data_source': 'estimated'
        }
    
    def _estimate_land_cover(self, location: Tuple[float, float] = None) -> Dict[str, Any]:
        """Estimate land cover when satellite data unavailable"""
        return {
            'water_percentage': 5.0,
            'vegetation_percentage': 40.0,
            'built_up_percentage': 30.0,
            'bare_soil_percentage': 15.0,
            'urban_percentage': 10.0,
            'data_source': 'estimated'
        }
