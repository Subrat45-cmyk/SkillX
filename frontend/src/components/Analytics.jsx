import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import axios from 'axios';
import './Analytics.css';

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('aqi_trend');
  const [loading, setLoading] = useState(true);
  const [pollutantBreakdown, setPollutantBreakdown] = useState([]);

  useEffect(() => {
    fetchAnalytics();
  }, [selectedMetric]);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('/api/history', { params: { limit: 30 } });
      
      // Process data for analytics
      const processed = response.data.map((item) => ({
        date: new Date(item.created_at).toLocaleDateString(),
        aqi: item.prediction.aqi_value,
        pm25: item.input_data.pm25 || 0,
        pm10: item.input_data.pm10 || 0,
        no2: item.input_data.no2 || 0,
        so2: item.input_data.so2 || 0,
        co: item.input_data.co || 0,
        temperature: item.input_data.temperature,
        humidity: item.input_data.humidity,
        confidence: item.prediction.confidence * 100
      }));

      setAnalyticsData(processed);

      // Calculate pollutant breakdown
      const pollutants = [
        { name: 'PM2.5', value: response.data[0]?.input_data.pm25 || 50 },
        { name: 'PM10', value: response.data[0]?.input_data.pm10 || 80 },
        { name: 'NO₂', value: response.data[0]?.input_data.no2 || 30 },
        { name: 'SO₂', value: response.data[0]?.input_data.so2 || 15 },
        { name: 'CO', value: response.data[0]?.input_data.co * 100 || 80 }
      ];
      setPollutantBreakdown(pollutants);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setLoading(false);
    }
  };

  const renderChart = () => {
    if (!analyticsData || analyticsData.length === 0) return null;

    switch (selectedMetric) {
      case 'aqi_trend':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={analyticsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="aqi" stroke="#FF6B6B" strokeWidth={2} name="AQI" />
              <Line type="monotone" dataKey="confidence" stroke="#4ECDC4" strokeWidth={2} name="Confidence %" />
            </LineChart>
          </ResponsiveContainer>
        );
      
      case 'pollutants':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={pollutantBreakdown}>
              <PolarGrid />
              <PolarAngleAxis dataKey="name" />
              <PolarRadiusAxis />
              <Radar name="Concentration" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
              <Tooltip />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        );
      
      case 'weather_impact':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={analyticsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="temperature" stroke="#FF9800" name="Temperature (°C)" />
              <Line yAxisId="right" type="monotone" dataKey="humidity" stroke="#2196F3" name="Humidity (%)" />
            </LineChart>
          </ResponsiveContainer>
        );
      
      case 'aqi_distribution':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={analyticsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="pm25" fill="#8884d8" name="PM2.5" />
              <Bar dataKey="pm10" fill="#82ca9d" name="PM10" />
              <Bar dataKey="no2" fill="#ffc658" name="NO₂" />
            </BarChart>
          </ResponsiveContainer>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="analytics-container">
      <header className="analytics-header">
        <h1>📊 AQI Analytics & Insights</h1>
      </header>

      <section className="metrics-selector">
        <button
          className={`metric-btn ${selectedMetric === 'aqi_trend' ? 'active' : ''}`}
          onClick={() => setSelectedMetric('aqi_trend')}
        >
          📈 AQI Trend
        </button>
        <button
          className={`metric-btn ${selectedMetric === 'pollutants' ? 'active' : ''}`}
          onClick={() => setSelectedMetric('pollutants')}
        >
          🌫️ Pollutants
        </button>
        <button
          className={`metric-btn ${selectedMetric === 'weather_impact' ? 'active' : ''}`}
          onClick={() => setSelectedMetric('weather_impact')}
        >
          🌦️ Weather Impact
        </button>
        <button
          className={`metric-btn ${selectedMetric === 'aqi_distribution' ? 'active' : ''}`}
          onClick={() => setSelectedMetric('aqi_distribution')}
        >
          📊 Distribution
        </button>
      </section>

      <section className="chart-container">
        {loading ? <div className="loading">Loading analytics...</div> : renderChart()}
      </section>

      <section className="insights-grid">
        <div className="insight-card">
          <h3>🎯 Key Findings</h3>
          <ul>
            <li>PM2.5 is the primary pollutant affecting air quality</li>
            <li>AQI peaks during morning hours (6-9 AM)</li>
            <li>Weather patterns significantly impact pollution levels</li>
            <li>Traffic congestion correlates with AQI spikes</li>
          </ul>
        </div>
        <div className="insight-card">
          <h3>⚠️ Risk Factors</h3>
          <ul>
            <li>High population density areas show 40% higher AQI</li>
            <li>Industrial zones have seasonal pollution patterns</li>
            <li>Wind speed inversely affects pollutant dispersion</li>
            <li>Humidity levels impact particulate matter suspension</li>
          </ul>
        </div>
        <div className="insight-card">
          <h3>💡 Recommendations</h3>
          <ul>
            <li>Plan outdoor activities during low AQI hours</li>
            <li>Use air purifiers in high-risk areas</li>
            <li>Support tree plantation initiatives</li>
            <li>Monitor real-time AQI updates</li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default Analytics;
