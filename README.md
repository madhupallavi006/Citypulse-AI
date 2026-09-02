# CITYPULSE AI
### A Predictive Urban Traffic Orchestration Platform

> **"PREDICT CONGESTION BEFORE IT HAPPENS, NOT AFTER."**

[![GitHub Repository](https://img.shields.io/badge/GitHub-madhupallavi006%2FCitypulse--AI-blue?logo=github)](https://github.com/madhupallavi006/Citypulse-AI)
[![Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20ML%20%7C%20RAG-orange)](#technology-stack)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-brightgreen)](#project-status)

---

> **IMPORTANT SAFETY LIMITATION**  
> CityPulse AI is a prototype / simulation platform created for demonstration purposes.  
> **The system NEVER directly controls real-world traffic lights, emergency infrastructure, public infrastructure, or physical devices.**  
> Traffic signal control and emergency corridor actions are simulated recommendations only.

---

## 🌆 1. Project Overview

CityPulse AI is an advanced intelligent urban traffic orchestration system. Traditional navigation and traffic management systems react to congestion *after* bottlenecks develop. CityPulse AI aims to predict hyper-local traffic congestion **15–30 minutes in advance**, enabling traffic control operators to execute preventive routing, signal adjustments, and emergency corridors before Gridlock occurs.

The system combines:
- **Machine Learning (ML)** for predictive congestion modeling (Random Forest, Gradient Boosting, XGBoost)
- **Explainable AI (XAI)** for feature importance and SHAP-driven prediction rationale
- **Unsupervised Anomaly Detection** (Isolation Forest) for sudden disruptions
- **Graph-based Route Optimization** (NetworkX Dijkstra / A*) taking predicted congestion into account
- **Multi-Agent AI Framework** (Prediction, Route, Emergency, Transit, Incident, & Operations Agents)
- **RAG & LLM AI Assistant** (ChromaDB + LangChain) for intelligent natural language operator support
- **Interactive Smart City Digital Twin** for scenario simulation and traffic propagation modeling

---

## 🚨 2. Problem Statement

Modern urban corridors suffer from sudden and hyper-local traffic disruptions caused by:
- VIP movements & scheduled public events
- Unplanned road construction & lane closures
- Rainwater logging and localized flooding
- Vehicle breakdowns & accidents
- Traffic signal outages

CityPulse AI forecasts congestion risk scores (0–100) and provides real-time preventive operational recommendations.

---

## 🏗️ 3. High-Level Architecture

```
DATA SOURCES (IoT / CCTV / Weather / GPS)
     |
     v
DATA INGESTION & FEATURE ENGINEERING
     |
     +----------------------+----------------------+
     |                      |                      |
     v                      v                      v
ML PREDICTION         ANOMALY DETECTION      DIGITAL TWIN
     |                      |                      |
     +----------+-----------+                      |
                |                                  |
                v                                  v
       CONGESTION RISK                    GRAPH ROUTE ENGINE
                |                                  |
                +-----------------+----------------+
                                  |
                                  v
                         MULTI-AGENT SYSTEM
       (Traffic | Route | Emergency | Transit | Incident | Ops)
                                  |
                                  v
                             RAG + LLM
                                  |
                                  v
                        EXPLAINABLE AI (XAI)
                                  |
                                  v
                     CITYPULSE CONTROL CENTER UI
```

---

## 🛠️ 4. Technology Stack

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS (Dark Smart City Theme)
- **Data Visualization**: Recharts
- **Mapping**: Leaflet / React-Leaflet + OpenStreetMap
- **Icons & HTTP**: Lucide React, Axios

### Backend
- **Framework**: Python 3.14 + FastAPI + Uvicorn
- **Data & Validation**: Pydantic v2, Pandas, NumPy
- **Graph Engine**: NetworkX

### AI / ML / RAG
- **Predictive ML**: Scikit-Learn (Random Forest, Gradient Boosting), XGBoost
- **Explainability**: SHAP / Feature Importance
- **Vector DB & RAG**: ChromaDB, LangChain
- **LLM Integration**: OpenAI / Compatible API with rule-based fallback

### Storage
- **Application DB**: SQLite
- **Vector Storage**: ChromaDB

---

## 📁 5. Project Structure

```
Citypulse-AI/
├── backend/
│   ├── main.py                  # FastAPI Application Entrypoint
│   ├── api/                     # REST API Routes
│   │   ├── traffic.py           # Traffic & Risk Endpoints
│   │   ├── incidents.py         # Incidents & Anomalies
│   │   ├── routes.py            # Route Optimization Endpoints
│   │   ├── emergency.py         # Emergency Corridor Endpoints
│   │   ├── simulation.py        # Digital Twin & Scenarios
│   │   └── chat.py              # LLM & RAG Chat Endpoints
│   ├── ml/                      # Machine Learning Pipeline
│   ├── agents/                  # Multi-Agent Architecture
│   ├── rag/                     # RAG & ChromaDB Ingestion
│   ├── simulation/              # Digital Twin Simulation Logic
│   ├── database/                # SQLite Database Schemas & Access
│   └── services/                # Business Logic & Orchestration
├── frontend/
│   ├── src/
│   │   ├── components/          # Navigation, Header, KPI Cards
│   │   ├── pages/               # 8 Dedicated Control Center Views
│   │   │   ├── Overview.jsx
│   │   │   ├── LiveTraffic.jsx
│   │   │   ├── Predictions.jsx
│   │   │   ├── Incidents.jsx
│   │   │   ├── EmergencyCorridor.jsx
│   │   │   ├── DigitalTwin.jsx
│   │   │   ├── ExplainableAI.jsx
│   │   │   └── AIAssistant.jsx
│   │   ├── services/            # Axios API Gateway
│   │   ├── App.jsx              # Master Layout & Tab Router
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── data/                        # SQLite & ChromaDB Storage
├── models/                      # Trained ML Models
├── tests/                       # Automated API & Integration Tests
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚡ 6. Quick Start & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### Backend Setup
```bash
# Navigate to project root
cd Citypulse-AI

# Create virtual environment (optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI backend server
uvicorn backend.main:app --reload --port 8000
```
Backend API will be available at: `http://localhost:8000`  
Interactive API Docs (Swagger): `http://localhost:8000/docs`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Launch Vite development server
npm run dev
```
Frontend Control Center will be available at: `http://localhost:5173`

---

## ⚙️ 7. Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key configurations:
- `LLM_API_KEY`: API Key for OpenAI or compatible LLM provider. *(If omitted, CityPulse AI automatically uses built-in rule-based fallback explanations).*
- `PORT`: Backend port (default `8000`).

---

## 🚦 8. Project Status & Roadmap

- [x] **Phase 1**: Base Architecture, Vite+React UI Framework, FastAPI Backend, CORS, & Git Setup
- [ ] **Phase 2**: Synthetic Traffic Generator & Live Data Pipeline
- [ ] **Phase 3**: Predictive ML Model Training & Risk Scoring Engine
- [ ] **Phase 4**: Unsupervised Anomaly & Incident Detection
- [ ] **Phase 5**: Congestion-Aware Graph Route Optimization & Leaflet Map
- [ ] **Phase 6**: Emergency Green Corridor & Bus Priority Simulation
- [ ] **Phase 7**: Digital Twin Scenario Simulation Engine
- [ ] **Phase 8**: RAG Knowledge Base & Vector Indexing (ChromaDB)
- [ ] **Phase 9**: LLM Integration & Operator AI Assistant
- [ ] **Phase 10**: Multi-Agent System Framework
- [ ] **Phase 11**: Explainable AI (XAI) & SHAP Feature Importance
- [ ] **Phase 12**: One-Click Interactive Demo Mode & Full System Integration

---

## 📄 License & Attribution

Developed as a prototype for Smart City Predictive Traffic Management demonstration.  
Connected Repository: [https://github.com/madhupallavi006/Citypulse-AI](https://github.com/madhupallavi006/Citypulse-AI)
