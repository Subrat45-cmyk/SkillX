import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from typing import List, Dict, Tuple, Any
import json
import os
from config import settings

class HotspotDetector:
    """Detect AQI hotspots using DBSCAN clustering"""
    
    def __init__(self, eps: float = 0.05, min_samples: int = 5):
        """
        Initialize hotspot detector
        
        Args:
            eps: DBSCAN epsilon parameter (radial distance in km/111 for lat-lon)
            min_samples: Minimum samples in neighborhood for core point
        """
        self.eps = eps
        self.min_samples = min_samples
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine')
        self.hotspots = []
    
    def detect_hotspots(self, 
                       locations: List[Tuple[float, float]], 
                       aqi_values: List[float]) -> List[Dict[str, Any]]:
        """
        Detect hotspots from location and AQI data
        
        Args:
            locations: List of (latitude, longitude) tuples
            aqi_values: List of corresponding AQI values
        
        Returns:
            List of hotspot dictionaries with clustering info
        """
        if len(locations) != len(aqi_values):
            raise ValueError("Locations and AQI values must have same length")
        
        # Convert to radians for haversine metric
        locations_rad = np.array(locations) * np.pi / 180
        
        # Perform clustering
        labels = self.dbscan.fit_predict(locations_rad)
        
        # Group data by cluster
        clusters = {}
        for idx, (label, (lat, lon), aqi) in enumerate(zip(labels, locations, aqi_values)):
            if label not in clusters:
                clusters[label] = {'locations': [], 'aqi_values': [], 'indices': []}
            clusters[label]['locations'].append((lat, lon))
            clusters[label]['aqi_values'].append(aqi)
            clusters[label]['indices'].append(idx)
        
        # Remove noise points (label == -1)
        if -1 in clusters:
            del clusters[-1]
        
        # Generate hotspot info
        hotspots = []
        for cluster_id, cluster_data in clusters.items():
            if len(cluster_data['locations']) >= self.min_samples:
                hotspot = self._generate_hotspot_info(
                    cluster_id,
                    cluster_data['locations'],
                    cluster_data['aqi_values'],
                    cluster_data['indices']
                )
                hotspots.append(hotspot)
        
        # Sort by severity
        hotspots.sort(key=lambda x: x['severity'], reverse=True)
        
        # Add priority ranks
        for i, hotspot in enumerate(hotspots):
            hotspot['priority_rank'] = i + 1
        
        self.hotspots = hotspots
        return hotspots
    
    def _generate_hotspot_info(self, 
                              cluster_id: int,
                              locations: List[Tuple[float, float]],
                              aqi_values: List[float],
                              indices: List[int]) -> Dict[str, Any]:
        """
        Generate detailed information for a hotspot cluster
        """
        locations_array = np.array(locations)
        center_lat = locations_array[:, 0].mean()
        center_lon = locations_array[:, 1].mean()
        
        aqi_array = np.array(aqi_values)
        avg_aqi = aqi_array.mean()
        max_aqi = aqi_array.max()
        min_aqi = aqi_array.min()
        std_aqi = aqi_array.std()
        
        # Calculate severity score (0-1)
        severity = min(1.0, max_aqi / 500.0)
        
        # Generate hotspot ID
        hotspot_id = f"hotspot_{cluster_id:03d}"
        
        # Get recommendations based on AQI level
        recommendations = self._get_recommendations_for_hotspot(avg_aqi)
        
        return {
            'id': hotspot_id,
            'cluster_id': int(cluster_id),
            'latitude': float(center_lat),
            'longitude': float(center_lon),
            'severity': float(severity),
            'point_count': len(locations),
            'average_aqi': float(avg_aqi),
            'max_aqi': float(max_aqi),
            'min_aqi': float(min_aqi),
            'std_aqi': float(std_aqi),
            'affected_indices': indices,
            'recommended_actions': recommendations,
            'radius_km': self._calculate_cluster_radius(locations),
            'geojson': self._generate_geojson(locations, center_lat, center_lon)
        }
    
    def _calculate_cluster_radius(self, locations: List[Tuple[float, float]]) -> float:
        """
        Calculate approximate radius of cluster
        """
        locations_array = np.array(locations)
        center = locations_array.mean(axis=0)
        distances = np.sqrt(((locations_array - center) ** 2).sum(axis=1))
        # Convert degrees to km (approximate)
        radius_km = distances.max() * 111
        return float(radius_km)
    
    def _get_recommendations_for_hotspot(self, avg_aqi: float) -> List[str]:
        """
        Get action recommendations based on average AQI
        """
        recommendations = []
        
        if avg_aqi > 300:
            recommendations.extend(['traffic_restriction', 'emergency_response', 'evacuation_warning'])
        elif avg_aqi > 200:
            recommendations.extend(['traffic_restriction', 'tree_plantation', 'industrial_emission_control'])
        elif avg_aqi > 150:
            recommendations.extend(['green_buffer_zone', 'water_sprinkling', 'tree_plantation'])
        elif avg_aqi > 100:
            recommendations.extend(['sensor_installation', 'air_quality_monitoring', 'tree_plantation'])
        else:
            recommendations.append('monitoring')
        
        return recommendations
    
    def _generate_geojson(self, 
                         locations: List[Tuple[float, float]],
                         center_lat: float,
                         center_lon: float) -> Dict[str, Any]:
        """
        Generate GeoJSON representation of hotspot
        """
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(center_lon), float(center_lat)]
            },
            'properties': {
                'point_count': len(locations)
            }
        }
    
    def save_hotspots(self, path: str = None):
        """
        Save detected hotspots to JSON file
        """
        if path is None:
            path = os.path.join(settings.model_path, 'hotspots.json')
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Convert to serializable format
        hotspots_serializable = []
        for hotspot in self.hotspots:
            hotspot_copy = hotspot.copy()
            hotspot_copy['severity'] = float(hotspot_copy['severity'])
            hotspot_copy['average_aqi'] = float(hotspot_copy['average_aqi'])
            hotspots_serializable.append(hotspot_copy)
        
        with open(path, 'w') as f:
            json.dump(hotspots_serializable, f, indent=4)
    
    def get_hotspots_geojson(self) -> Dict[str, Any]:
        """
        Return hotspots as GeoJSON FeatureCollection
        """
        features = []
        for hotspot in self.hotspots:
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [hotspot['longitude'], hotspot['latitude']]
                },
                'properties': {
                    'id': hotspot['id'],
                    'severity': hotspot['severity'],
                    'aqi': hotspot['average_aqi'],
                    'priority': hotspot['priority_rank'],
                    'point_count': hotspot['point_count']
                }
            })
        
        return {
            'type': 'FeatureCollection',
            'features': features
        }
