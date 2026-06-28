# AQI Vision AI - Project Structure

```
aqi-vision-ai/
├── backend/
│   ├── app.py                      # FastAPI main application
│   ├── config.py                   # Configuration management
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── preprocessing.py        # Data preprocessing pipeline
│   │   ├── feature_engineering.py  # Feature engineering
│   │   ├── models.py               # Model training
│   │   ├── predict.py              # Prediction engine
│   │   ├── evaluate.py             # Model evaluation
│   │   ├── utils.py                # ML utilities
│   │   └── explainability.py       # SHAP explainability
│   │
│   ├── geo/
│   │   ├── __init__.py
│   │   ├── hotspots.py             # DBSCAN hotspot detection
│   │   ├── satellite.py            # Satellite imagery processing
│   │   └── tiles.py                # GeoJSON tile management
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               # API routes
│   │   ├── schemas.py              # Pydantic schemas
│   │   └── middleware.py           # Custom middleware
│   │
│   ├── recommendation/
│   │   ├── __init__.py
│   │   └── engine.py               # Recommendation logic
│   │
│   └── data/
│       ├── models/                 # Saved ML models
│       ├── scalers/                # Feature scalers
│       └── encoders/               # Label encoders
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Prediction.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Maps.jsx
│   │   │   ├── Hotspots.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── History.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── Admin.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Loading.jsx
│   │   │   │   └── ErrorBoundary.jsx
│   │   │   │
│   │   │   ├── charts/
│   │   │   │   ├── LineChart.jsx
│   │   │   │   ├── BarChart.jsx
│   │   │   │   ├── PieChart.jsx
│   │   │   │   └── RadarChart.jsx
│   │   │   │
│   │   │   ├── maps/
│   │   │   │   ├── MapContainer.jsx
│   │   │   │   ├── Heatmap.jsx
│   │   │   │   ├── Markers.jsx
│   │   │   │   └── Legend.jsx
│   │   │   │
│   │   │   └── cards/
│   │   │       ├── MetricCard.jsx
│   │   │       ├── PredictionCard.jsx
│   │   │       └── RecommendationCard.jsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAPI.js
│   │   │   ├── useGeolocation.js
│   │   │   └── useTheme.js
│   │   │
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── storage.js
│   │   │
│   │   ├── utils/
│   │   │   ├── constants.js
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   │
│   │   └── styles/
│   │       ├── globals.css
│   │       ├── animations.css
│   │       └── responsive.css
│   │
│   └── public/
│       ├── favicon.ico
│       └── manifest.json
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── nginx.conf
├── README.md
├── ARCHITECTURE.md
├── INSTALLATION.md
├── API_DOCS.md
└── DEPLOYMENT.md
```

## Component Descriptions

### Backend Components
- **ML Pipeline**: Preprocessing, feature engineering, model training & evaluation
- **Geo Analysis**: Hotspot detection using DBSCAN, satellite imagery processing
- **API Layer**: FastAPI endpoints with validation
- **Recommendation Engine**: Dynamic recommendations based on AQI levels

### Frontend Components
- **Pages**: Dashboard, Prediction, Analytics, Maps, Hotspots, Recommendations, History, Profile, Admin
- **Charts**: Multiple chart types for data visualization
- **Maps**: Interactive maps with heatmaps, markers, and GeoJSON layers
- **Hooks & Services**: Reusable logic for API calls and utilities

### Database
- PostgreSQL for persistent data storage
- Time-series data for AQI historical records

## Data Pipeline

1. Data Collection from sensors/satellites
2. Preprocessing & normalization
3. Feature engineering
4. Model training (Random Forest, XGBoost)
5. Hotspot detection
6. Recommendation generation
7. API serialization & frontend display
