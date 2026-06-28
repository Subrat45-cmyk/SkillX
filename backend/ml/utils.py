import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any

def categorize_aqi(aqi_value: float) -> Dict[str, Any]:
    """Categorize AQI and return details"""
    categories = {
        'Good': {'range': (0, 50), 'color': '#00AA00', 'icon': '😊'},
        'Satisfactory': {'range': (51, 100), 'color': '#FFFF00', 'icon': '🙂'},
        'Moderately Polluted': {'range': (101, 200), 'color': '#FF7F00', 'icon': '😷'},
        'Poor': {'range': (201, 300), 'color': '#FF0000', 'icon': '😢'},
        'Very Poor': {'range': (301, 400), 'color': '#8B0000', 'icon': '😵'},
        'Severe': {'range': (401, 500), 'color': '#000000', 'icon': '💀'}
    }
    
    for category, details in categories.items():
        if details['range'][0] <= aqi_value <= details['range'][1]:
            return {
                'category': category,
                'color': details['color'],
                'icon': details['icon'],
                'range': details['range']
            }
    
    return {'category': 'Unknown', 'color': '#CCCCCC', 'icon': '❓', 'range': (500, float('inf'))}

def get_health_advisory(aqi_category: str) -> str:
    """Get health advisory for AQI category"""
    advisories = {
        'Good': 'Air quality is satisfactory. Enjoy outdoor activities!',
        'Satisfactory': 'Air quality is acceptable. Few may experience minor issues.',
        'Moderately Polluted': 'Sensitive groups should limit outdoor activities.',
        'Poor': 'Members of sensitive groups should avoid outdoor activities.',
        'Very Poor': 'Everyone should avoid outdoor activities. Use air purifiers indoors.',
        'Severe': 'Avoid outdoor activities. Stay indoors with windows closed.'
    }
    return advisories.get(aqi_category, 'Check air quality levels')

def calculate_air_quality_index(pollutants: Dict[str, float]) -> float:
    """Calculate AQI from individual pollutants"""
    # Breakpoints for different pollutants (simplified)
    breakpoints = {
        'pm25': [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 150), (91, 120, 151, 200), (121, 250, 201, 300), (251, float('inf'), 301, 500)],
        'pm10': [(0, 50, 0, 50), (51, 100, 51, 100), (101, 150, 101, 150), (151, 200, 151, 200), (201, 300, 201, 300), (301, float('inf'), 301, 500)],
        'no2': [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 150), (181, 280, 151, 200), (281, 400, 201, 300), (401, float('inf'), 301, 500)],
        'o3': [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 150), (169, 208, 151, 200), (209, 748, 201, 300), (749, float('inf'), 301, 500)],
    }
    
    aqi_values = []
    for pollutant, value in pollutants.items():
        if pollutant in breakpoints:
            for bp in breakpoints[pollutant]:
                if bp[0] <= value <= bp[1]:
                    aqi = bp[2] + (bp[3] - bp[2]) * (value - bp[0]) / (bp[1] - bp[0])
                    aqi_values.append(aqi)
                    break
    
    return max(aqi_values) if aqi_values else 0

def get_recommendations(aqi_value: float, location: str = None) -> List[Dict[str, Any]]:
    """Get recommendations based on AQI level"""
    recommendations = []
    
    if aqi_value > 200:
        recommendations.append({
            'type': 'tree_plantation',
            'priority': 'high',
            'description': 'Urgent need for green cover expansion',
            'reason': 'High AQI level detected',
            'confidence': 0.95
        })
        recommendations.append({
            'type': 'traffic_restriction',
            'priority': 'high',
            'description': 'Implement traffic restrictions',
            'reason': 'Emission reduction needed',
            'confidence': 0.90
        })
    
    if aqi_value > 150:
        recommendations.append({
            'type': 'green_buffer',
            'priority': 'medium',
            'description': 'Create green buffer zones',
            'reason': 'Air quality improvement',
            'confidence': 0.85
        })
        recommendations.append({
            'type': 'water_sprinkling',
            'priority': 'medium',
            'description': 'Increase water sprinkling in affected areas',
            'reason': 'Dust suppression',
            'confidence': 0.80
        })
    
    if aqi_value > 100:
        recommendations.append({
            'type': 'sensor_installation',
            'priority': 'low',
            'description': 'Install additional monitoring sensors',
            'reason': 'Better monitoring needed',
            'confidence': 0.75
        })
    
    return recommendations
