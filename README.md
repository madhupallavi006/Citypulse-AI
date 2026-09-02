# CITYPULSE AI
> **A Predictive Urban Traffic Orchestration Platform**
> *"Predict congestion before it happens, not after."*

[![GitHub Repository](https://img.shields.io/badge/GitHub-madhupallavi006%2FCitypulse--AI-blue?logo=github)](https://github.com/madhupallavi006/Citypulse-AI)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-emerald?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-sky?logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple?logo=vite)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Pytest 100% Passed](https://img.shields.io/badge/Tests-38%2F38%20Passed-brightgreen?logo=pytest)](file:///C:/Users/Madhu/.gemini/antigravity-ide/brain/e72295fb-f57b-4248-9938-b08be0e9eeb2/walkthrough.md)

---

## 🌟 Executive Summary
CityPulse AI is a complete predictive urban traffic management platform designed to transform city traffic control centers from reactive congestion managers into proactive AI orchestrators.

Instead of reacting after gridlock occurs, CityPulse AI combines real-time synthetic traffic telemetry, Machine Learning risk forecasting (Random Forest & Gradient Boosting), Unsupervised Anomaly Isolation (Isolation Forest), NetworkX Graph Route Optimization, RAG Standard Operating Procedures, Dual LLM Assistance, Multi-Agent AI System Collaboration, Explainable AI (SHAP/counterfactuals), and an interactive Leaflet Live Traffic Map.

---

## 📊 Core Engine Modules & Capabilities

### 1. Synthetic Dataset & SQLite Telemetry Engine
- **55,104 Synthetic Observations**: Generated across 42 road corridors (Expressway, Outer Ring Road, CBD, Metro) spanning 14 days of realistic diurnal commute patterns.
- **SQLite Storage**: Persistent local database (`data/citypulse.db`) seeding 42 road segments, 20 intersection nodes, telemetry observations, and active disruption incidents.
- **Stateful Live Traffic Simulator**: Dynamic real-time simulator supporting rain mode, traffic multiplier scaling, and incident overrides.

### 2. Machine Learning Congestion Risk Engine
- **Model Comparison**: Trained both **Random Forest Classifier** and **Gradient Boosting Classifier** on 44,083 training samples and 11,021 test samples.
- **Top Model Performance (Random Forest)**:
  - **Accuracy**: `99.90%`
  - **Precision**: `99.90%`
  - **Recall**: `99.56%`
  - **F1-Score**: `99.73%`
  - **ROC-AUC**: `1.0000`
- **Real-Time ML Inference**: Predicts 15–30 minute congestion probability forecasts and 0–100 risk scores.

### 3. Isolation Forest Unsupervised Anomaly Detection
- Identifies outlier telemetry patterns without hardcoded rules:
  - `Sudden Speed Drop & Bottleneck`
  - `Abnormal Road Occupancy Spike`
  - `Sudden Traffic Density Surge`
  - `Accident-like Pattern` & `Road Closure`

### 4. NetworkX Road Graph & Predicted-Congestion Route Optimization
- **City Graph**: 20 Intersection Nodes (`J01`–`J20`) with geographic coordinates and 42 Directed Edges.
- **Smart Edge Weight Costing**: Dynamically computes edge costs incorporating physical travel time, current speed, disruption penalties, and **ML predicted congestion risk** 15–30 minutes ahead.
- **Dijkstra & A* Pathfinding**: Calculates standard shortest paths vs CityPulse congestion-aware paths, outputting ETAs, risk levels, and estimated time saved.

### 5. Emergency Green Corridor & Public Transport Priority
- **Emergency Dispatch**: Automated fastest safe pathing for Ambulances, Fire Trucks, and Police units with signal pre-emption sequences (`GREEN_OVERRIDE`) across affected intersections.
- **Public Transit Bus Priority**: Monitors bus schedule delays and recommends temporary signal green extensions (+12s) or red-phase truncations (-8s).
- *Safety Boundary Limitation*: All traffic signal pre-emptions and green corridor activations are simulated recommendations only.

### 6. Digital Twin & What-If Scenario Engine
- Interactive scenario modeler evaluating baseline vs simulated citywide metrics across:
  - Rain Intensity (0–100%)
  - Special Event Demand Multipliers (1.0x–3.0x)
  - Active Road Closures
  - Signal Timing Overrides (-15s to +30s)
  - Transit Surge Factors

### 7. RAG Knowledge Base & Dual LLM Operator Assistant
- **RAG Knowledge Base**: Structured SOP corpus (`data/traffic_sops.json`) indexed into TF-IDF vector space (`models/rag_index.joblib`) for cosine similarity document retrieval.
- **Dual LLM Provider Support**: Google Gemini API (`GEMINI_API_KEY`) and Groq API (`GROQ_API_KEY`).
- **100% Functional Rule-Based Fallback Engine**: Guarantees full chat assistant operation even without an LLM API key.

### 8. Multi-Agent AI System (5 Specialized Agents)
- **Traffic Monitor Agent**: Audits telemetry and Isolation Forest anomalies.
- **Congestion Predictor Agent**: Executes ML inference forecasting 15–30 min congestion probabilities.
- **Route Optimizer Agent**: Computes NetworkX Dijkstra congestion-bypass paths.
- **Incident Response Agent**: Queries RAG SOP knowledge base and manages emergency pre-emption.
- **Signal Orchestrator Agent**: Synthesizes agent inputs into dynamic green phase timing recommendations.
- **Collaboration Pipeline**: Executed sequentially (`Monitor -> Predictor -> Optimizer -> Response -> Orchestrator`).

### 9. Explainable AI (XAI) & Counterfactual Reasoning
- Decomposes black-box ML risk scores into percentage feature contributions (Speed Deficit, Occupancy, Density, Rain, Incidents).
- Generates natural language explanation summaries.
- Evaluates Counterfactual What-If scenarios (*"If average speed increases by +12 km/h, congestion risk score drops from 82/100 to 36/100"*).

### 10. One-Click Interactive Demo Presets
- Top Header Quick Launcher pills for 4 pre-configured demo scenarios:
  1. `Morning Peak Commute` (1.8x traffic multiplier across CBD)
  2. `Monsoon Heavy Rain` (85% rain intensity, speed limits throttled)
  3. `Ambulance Green Wave` (Rapid trauma dispatch with 7 pre-emption junctions)
  4. `Stadium Event Surge` (2.5x traffic surge around Kalinga Stadium with NetworkX rerouting)

---

## 🛠️ Project Structure

```
Citypulse-AI/
├── backend/
│   ├── api/                 # FastAPI API Routers (traffic, incidents, routes, emergency, simulation, chat, agents, demo)
│   ├── agents/              # Multi-Agent AI System (5 Specialized Agents & Collaboration Engine)
│   ├── database/            # SQLite Database Connection & Models
│   ├── ml/                  # Machine Learning (Feature Engineering, Training, Evaluation, Inference, Anomaly Detection, XAI)
│   ├── rag/                 # RAG Ingestion & Cosine Similarity Retriever
│   ├── services/            # Backend Service Layer
│   ├── simulation/         # Stateful Traffic Simulator Engine & NetworkX Road Graph
│   └── main.py              # FastAPI Server Entry Point
├── data/                    # Synthetic Traffic Dataset & SOP Knowledge Corpus
├── frontend/                # React 18 + Vite + Tailwind CSS + Leaflet Control Center
│   ├── src/
│   │   ├── components font/ # Header, Sidebar, KPICards
│   │   ├── pages/           # 8 Control Center Views (Overview, LiveTraffic, Predictions, Incidents, Emergency, DigitalTwin, XAI, Assistant)
│   │   └── services/        # Frontend API Axios Client
├── models/                  # Trained ML Artifacts (congestion_model.joblib, rag_index.joblib)
├── tests/                   # Automated Pytest Test Suite (38/38 Tests Passed)
├── .env.example             # Environment Variable Template
├── requirements.txt         # Python Backend Dependencies
└── README.md                # Technical Documentation
```

---

## 🚀 Quickstart & Local Installation Guide

### Prerequisites
- Python 3.10+ (Python 3.14 supported)
- Node.js 18+ & npm

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/madhupallavi006/Citypulse-AI.git
cd Citypulse-AI

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate      # On Windows
# source venv/bin/activate   # On Linux/macOS

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI backend server
$env:PYTHONPATH='.'; .\venv\Scripts\python backend/main.py
```
FastAPI server runs at: `http://localhost:8000` (Docs: `http://localhost:8000/docs`)

### 2. Frontend Setup
```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend Control Center runs at: `http://localhost:5173`

---

## 🧪 Automated Testing

The project includes an automated Pytest suite covering database initialization, stateful simulation, ML model inference, Isolation Forest anomaly detection, NetworkX graph routing, emergency pre-emption, digital twin What-If modeler, RAG retrieval, multi-agent collaboration, Explainable AI, and one-click demo presets.

```bash
# Run pytest test suite
$env:PYTHONPATH='.'; .\venv\Scripts\pytest
====================== 38 passed, 1 warning in 38.53s =======================
```

---

## 🔒 Safety Boundary Directive
> **IMPORTANT**: CityPulse AI is designed exclusively as an intelligent decision-support and simulation platform. The system does **NOT** directly control physical traffic lights, emergency infrastructure, or real-world traffic signals. All signal timing pre-emptions and green corridor activations are simulated recommendations only.

---

## 📜 License & Author
- **Repository**: [https://github.com/madhupallavi006/Citypulse-AI](https://github.com/madhupallavi006/Citypulse-AI)
- **Author**: Madhu Pallavi (`madhupallavi006`)
