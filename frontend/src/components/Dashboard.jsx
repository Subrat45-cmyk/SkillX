import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const [predictions, setPredictions] = useState([]);
  const [currentAQI, setCurrentAQI] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [timeRange, setTimeRange] = useState('7days');
  const [aqi_history, setAQIHistory] = useState([]);

  useEffect(() => {
    fetchPredictions();
  }, [selectedLocation, timeRange]);

  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/history', {
        params: { days: timeRange === '7days' ? 7 : 30 }
      });
      setPredictions(response.data);
      
      // Set current AQI from latest prediction
      if (response.data.length > 0) {
        setCurrentAQI(response.data[0].prediction);
      }
      
      // Format for chart
      const formattedData = response.data.map((item, idx) => ({
        date: new Date(item.created_at).toLocaleDateString(),
        aqi: item.prediction.aqi_value,
        confidence: item.prediction.confidence * 100
      }));
      setAQIHistory(formattedData);
    } catch (error) {
      console.error('Error fetching predictions:', error);
    }
    setLoading(false);
  };

  const getAQIColor = (value) => {
    if (value <= 50) return '#4CAF50';      // Green - Good
    if (value <= 100) return '#8BC34A';     // Light Green - Satisfactory
    if (value <= 200) return '#FFC107';     // Yellow - Moderately Polluted
    if (value <= 300) return '#FF9800';     // Orange - Poor
    if (value <= 400) return '#F44336';     // Red - Very Poor
    return '#8B0000';                       // Dark Red - Severe
  };

  const getAQICategory = (value) => {
    if (value <= 50) return 'Good';
    if (value <= 100) return 'Satisfactory';
    if (value <= 200) return 'Moderately Polluted';
    if (value <= 300) return 'Poor';
    if (value <= 400) return 'Very Poor';
    return 'Severe';
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🌍 AQI Vision - Air Quality Dashboard</h1>
        <div className="header-controls">
          <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)} className="time-select">
            <option value="7days">Last 7 Days</option>
            <option value="30days">Last 30 Days</option>
          </select>
        </div>
      </header>

      {currentAQI && (
        <section className="aqi-card" style={{ borderLeft: `5px solid ${getAQIColor(currentAQI.aqi_value)}` }}>
          <div className="aqi-value-display">
            <div className="aqi-circle" style={{ backgroundColor: getAQIColor(currentAQI.aqi_value) }}>
              <span className="aqi-number">{currentAQI.aqi_value.toFixed(1)}</span>
            </div>
            <div className="aqi-info">
              <h2>{getAQICategory(currentAQI.aqi_value)}</h2>
              <p className="advisory">{currentAQI.health_advisory}</p>
              <p className="confidence">Confidence: {(currentAQI.confidence * 100).toFixed(1)}%</p>
            </div>
          </div>
        </section>
      )}

      <section className="charts-container">
        <div className="chart-box">
          <h3>📈 AQI Trend</h3>
          {aqi_history.length > 0 && (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={aqi_history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="aqi" stroke="#FF6B6B" name="AQI Value" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="chart-box">
          <h3>🎯 Model Confidence</h3>
          {aqi_history.length > 0 && (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={aqi_history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="confidence" fill="#4ECDC4" name="Confidence %" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>

      <section className="predictions-list">
        <h3>📋 Recent Predictions</h3>
        <div className="predictions-grid">
          {predictions.slice(0, 6).map((pred, idx) => (
            <div key={idx} className="prediction-card" style={{ borderColor: getAQIColor(pred.prediction.aqi_value) }}>
              <div className="pred-header">
                <span className="pred-date">{new Date(pred.created_at).toLocaleDateString()}</span>
                <span className="pred-category" style={{ backgroundColor: getAQIColor(pred.prediction.aqi_value) }}>
                  {getAQICategory(pred.prediction.aqi_value)}
                </span>
              </div>
              <div className="pred-value">AQI: {pred.prediction.aqi_value.toFixed(1)}</div>
              <div className="pred-confidence">Confidence: {(pred.prediction.confidence * 100).toFixed(1)}%</div>
            </div>
          ))}
        </div>
      </section>

      {loading && <div className="loading">Loading data...</div>}
    </div>
  );
};

export default Dashboard;
