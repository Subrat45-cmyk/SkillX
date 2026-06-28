from typing import List, Dict, Any
from ..ml.utils import categorize_aqi, get_recommendations

class RecommendationEngine:
    """Generate recommendations based on AQI levels and environmental data"""
    
    def __init__(self):
        self.recommendations_cache = {}
    
    def generate_recommendations(self,
                                aqi_value: float,
                                location: Dict[str, float] = None,
                                environmental_data: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate comprehensive recommendations based on AQI and environmental conditions
        
        Args:
            aqi_value: Current AQI value (0-500)
            location: Optional location {'latitude', 'longitude'}
            environmental_data: Optional environmental parameters
        
        Returns:
            List of recommendations with priority, reason, and confidence
        """
        recommendations = []
        
        # Get base recommendations from utility function
        base_recs = get_recommendations(aqi_value, location.get('name') if location else None)
        
        # Enhance recommendations
        for rec in base_recs:
            enhanced_rec = {
                'type': rec['type'],
                'priority': rec['priority'],
                'description': self._get_description(rec['type'], aqi_value),
                'reason': rec['reason'],
                'confidence': rec['confidence'],
                'estimated_impact': self._estimate_impact(rec['type'], aqi_value),
                'implementation_cost': self._estimate_cost(rec['type']),
                'timeline': self._estimate_timeline(rec['type']),
                'stakeholders': self._get_stakeholders(rec['type']),
                'metrics': self._get_success_metrics(rec['type'])
            }
            recommendations.append(enhanced_rec)
        
        # Add location-specific recommendations
        if location and environmental_data:
            recommendations.extend(self._get_location_specific_recs(location, environmental_data, aqi_value))
        
        # Sort by priority and confidence
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(
            key=lambda x: (priority_order.get(x['priority'], 3), -x['confidence'])
        )
        
        return recommendations
    
    def _get_description(self, rec_type: str, aqi_value: float) -> str:
        """Get detailed description for recommendation type"""
        descriptions = {
            'tree_plantation': f"Plant trees to absorb pollutants (Target: 5000+ trees in affected area)",
            'traffic_restriction': f"Implement odd-even or traffic bans during peak hours",
            'green_buffer': f"Create 100-200m green zones around polluted areas",
            'water_sprinkling': f"Increase water sprinkling frequency to 2-3 times daily",
            'sensor_installation': f"Install additional air quality monitoring sensors",
            'industrial_emission_control': f"Enforce stricter emission standards for industries",
            'emergency_response': f"Activate emergency response protocols",
            'evacuation_warning': f"Issue evacuation warnings for vulnerable populations",
            'monitoring': f"Continue standard air quality monitoring"
        }
        return descriptions.get(rec_type, "Monitor and evaluate")
    
    def _estimate_impact(self, rec_type: str, aqi_value: float) -> str:
        """Estimate AQI reduction impact"""
        impact_ranges = {
            'tree_plantation': "Reduce AQI by 5-15% (Long-term)",
            'traffic_restriction': "Reduce AQI by 10-20% (Immediate)",
            'green_buffer': "Reduce AQI by 3-8% (Medium-term)",
            'water_sprinkling': "Reduce AQI by 2-5% (Short-term)",
            'sensor_installation': "No direct impact (Monitoring)",
            'industrial_emission_control': "Reduce AQI by 15-30% (Medium-term)",
            'emergency_response': "Varies",
            'evacuation_warning': "No direct impact (Safety)",
            'monitoring': "No direct impact"
        }
        return impact_ranges.get(rec_type, "Varies")
    
    def _estimate_cost(self, rec_type: str) -> str:
        """Estimate implementation cost"""
        costs = {
            'tree_plantation': 'medium',
            'traffic_restriction': 'low',
            'green_buffer': 'high',
            'water_sprinkling': 'low',
            'sensor_installation': 'medium',
            'industrial_emission_control': 'high',
            'emergency_response': 'medium',
            'evacuation_warning': 'low',
            'monitoring': 'low'
        }
        return costs.get(rec_type, 'medium')
    
    def _estimate_timeline(self, rec_type: str) -> str:
        """Estimate implementation timeline"""
        timelines = {
            'tree_plantation': '3-6 months',
            'traffic_restriction': 'Immediate',
            'green_buffer': '6-12 months',
            'water_sprinkling': 'Immediate',
            'sensor_installation': '1-2 months',
            'industrial_emission_control': '2-4 weeks',
            'emergency_response': 'Immediate',
            'evacuation_warning': 'Immediate',
            'monitoring': 'Ongoing'
        }
        return timelines.get(rec_type, 'Variable')
    
    def _get_stakeholders(self, rec_type: str) -> List[str]:
        """Get relevant stakeholders for implementation"""
        stakeholders = {
            'tree_plantation': ['Municipal Corporation', 'Environment Dept', 'NGOs', 'Community'],
            'traffic_restriction': ['Traffic Police', 'Transport Dept', 'Municipal Corp'],
            'green_buffer': ['Urban Development', 'Environment Dept', 'Municipal Corp'],
            'water_sprinkling': ['Municipal Corp', 'PWD', 'Street Vendors'],
            'sensor_installation': ['Environment Dept', 'CPCB', 'Tech Providers'],
            'industrial_emission_control': ['Industries', 'Pollution Control Board', 'Regulatory Dept'],
            'emergency_response': ['Disaster Management', 'Health Dept', 'Administration'],
            'evacuation_warning': ['Administration', 'Health Dept', 'Police'],
            'monitoring': ['CPCB', 'Environment Dept']
        }
        return stakeholders.get(rec_type, [])
    
    def _get_success_metrics(self, rec_type: str) -> List[str]:
        """Get success metrics for recommendation"""
        metrics = {
            'tree_plantation': ['Trees planted', 'Survival rate %', 'AQI reduction', 'Green cover %'],
            'traffic_restriction': ['Vehicles reduced %', 'AQI reduction', 'Public compliance %'],
            'green_buffer': ['Area covered sq.m', 'Vegetation density', 'AQI reduction'],
            'water_sprinkling': ['Dust settled %', 'AQI reduction', 'Frequency compliance'],
            'sensor_installation': ['Sensors deployed', 'Data accuracy', 'Coverage %'],
            'industrial_emission_control': ['Emission reduction %', 'Compliance rate', 'AQI reduction'],
            'emergency_response': ['Response time', 'Lives protected', 'Coverage %'],
            'evacuation_warning': ['People reached', 'Evacuation rate', 'Safety incidents'],
            'monitoring': ['Data points', 'Accuracy', 'Frequency']
        }
        return metrics.get(rec_type, [])
    
    def _get_location_specific_recs(self,
                                   location: Dict[str, float],
                                   env_data: Dict[str, float],
                                   aqi_value: float) -> List[Dict[str, Any]]:
        """Generate location-specific recommendations"""
        recs = []
        
        # Check for high traffic areas
        if env_data.get('traffic_index', 0) > 70:
            recs.append({
                'type': 'traffic_optimization',
                'priority': 'high',
                'description': 'Optimize traffic signal timing and implement smart traffic management',
                'reason': 'High traffic congestion detected',
                'confidence': 0.9,
                'estimated_impact': 'Reduce AQI by 8-12%',
                'implementation_cost': 'high',
                'timeline': '2-3 months',
                'stakeholders': ['Traffic Police', 'Smart City Mission'],
                'metrics': ['Traffic flow improvement %', 'Emission reduction', 'AQI change']
            })
        
        # Check for industrial areas
        if env_data.get('population_density', 0) < 500 and aqi_value > 200:
            recs.append({
                'type': 'industrial_audit',
                'priority': 'high',
                'description': 'Conduct comprehensive industrial emission audit and control',
                'reason': 'Industrial area with high pollution',
                'confidence': 0.85,
                'estimated_impact': 'Reduce AQI by 10-25%',
                'implementation_cost': 'high',
                'timeline': '1-2 months',
                'stakeholders': ['CPCB', 'Industries', 'State Pollution Board'],
                'metrics': ['Industries audited', 'Emission reduction %', 'Compliance rate']
            })
        
        return recs
