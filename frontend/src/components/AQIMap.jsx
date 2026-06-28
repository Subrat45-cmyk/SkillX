import React, { useState, useEffect } from 'react';
import MapGL, { Marker, Popup, NavigationControl, GeolocateControl } from '@react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './AQIMap.css';
import axios from 'axios';

const AQIMap = () => {
  const [viewport, setViewport] = useState({
    latitude: 28.7041,
    longitude: 77.1025,
    zoom: 11
  });
  const [hotspots, setHotspots] = useState([]);
  const [selectedHotspot, setSelectedHotspot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/streets-v11');

  useEffect(() => {
    fetchHotspots();
  }, []);

  const fetchHotspots = async () => {
    try {
      const response = await axios.post('/api/hotspots', {
        locations: [
          { latitude: 28.7041, longitude: 77.1025, radius_km: 5 },
          { latitude: 28.6692, longitude: 77.1559, radius_km: 5 }
        ],
        aqi_values: [285, 215],
        eps: 0.05,
        min_samples: 5
      });
      setHotspots(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching hotspots:', error);
      setLoading(false);
    }
  };

  const getHotspotColor = (severity) => {
    if (severity > 0.8) return '#8B0000';
    if (severity > 0.6) return '#FF4500';
    if (severity > 0.4) return '#FFA500';
    return '#FFD700';
  };

  const getMarkerSize = (severity) => {
    return 20 + severity * 20;
  };

  return (
    <div className="aqi-map-container">
      <header className="map-header">
        <h1>🗺️ AQI Hotspot Map</h1>
        <div className="map-controls">
          <button 
            onClick={() => setMapStyle('mapbox://styles/mapbox/streets-v11')}
            className="style-btn active"
          >
            Streets
          </button>
          <button 
            onClick={() => setMapStyle('mapbox://styles/mapbox/satellite-v9')}
            className="style-btn"
          >
            Satellite
          </button>
        </div>
      </header>

      <MapGL
        {...viewport}
        width="100%"
        height="600px"
        mapStyle={mapStyle}
        onViewportChange={setViewport}
        mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
      >
        <GeolocateControl />
        <NavigationControl />

        {hotspots.map((hotspot) => (
          <React.Fragment key={hotspot.id}>
            <Marker
              latitude={hotspot.latitude}
              longitude={hotspot.longitude}
            >
              <div
                className="marker"
                style={{
                  backgroundColor: getHotspotColor(hotspot.severity),
                  width: getMarkerSize(hotspot.severity),
                  height: getMarkerSize(hotspot.severity),
                  borderRadius: '50%',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 'bold',
                  fontSize: '12px'
                }}
                onClick={() => setSelectedHotspot(hotspot)}
              >
                {hotspot.priority_rank}
              </div>
            </Marker>
          </React.Fragment>
        ))}

        {selectedHotspot && (
          <Popup
            latitude={selectedHotspot.latitude}
            longitude={selectedHotspot.longitude}
            onClose={() => setSelectedHotspot(null)}
            closeButton={true}
          >
            <div className="popup-content">
              <h3>{selectedHotspot.id}</h3>
              <p><strong>AQI:</strong> {selectedHotspot.average_aqi.toFixed(1)}</p>
              <p><strong>Severity:</strong> {(selectedHotspot.severity * 100).toFixed(1)}%</p>
              <p><strong>Points:</strong> {selectedHotspot.point_count}</p>
              <p><strong>Priority:</strong> #{selectedHotspot.priority_rank}</p>
              <div className="recommendations">
                <strong>Actions:</strong>
                <ul>
                  {selectedHotspot.recommended_actions?.map((action, idx) => (
                    <li key={idx}>{action.replace(/_/g, ' ')}</li>
                  ))}
                </ul>
              </div>
            </div>
          </Popup>
        )}
      </MapGL>

      <section className="hotspots-list">
        <h3>🔥 Top Hotspots</h3>
        <div className="hotspots-grid">
          {hotspots.map((hotspot) => (
            <div
              key={hotspot.id}
              className="hotspot-card"
              style={{ borderLeft: `5px solid ${getHotspotColor(hotspot.severity)}` }}
              onClick={() => setSelectedHotspot(hotspot)}
            >
              <div className="hotspot-rank">#{hotspot.priority_rank}</div>
              <h4>{hotspot.id}</h4>
              <p><strong>AQI:</strong> {hotspot.average_aqi.toFixed(1)}</p>
              <p><strong>Severity:</strong> {(hotspot.severity * 100).toFixed(1)}%</p>
              <p><strong>Points:</strong> {hotspot.point_count}</p>
            </div>
          ))}
        </div>
      </section>

      {loading && <div className="loading">Loading map data...</div>}
    </div>
  );
};

export default AQIMap;
