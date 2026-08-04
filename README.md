# 1. Project Title

# BatteryMind

**An Explainable AI-powered IoT Battery Health Monitoring and Predictive Maintenance Framework.**

---

# 2. Project Overview

BatteryMind addresses a core limitation of conventional battery monitoring systems: they usually report scalar health values but do not explain *why* degradation is occurring or what actions should be taken next.

In many practical setups, battery status is represented as a single value such as:

> **SOH = 85%**

This is useful but incomplete for maintenance and diagnostics. BatteryMind extends this to:

> **SOH = 85% because current stress, temperature behavior, and energy usage patterns are contributing to degradation.**

## Why this matters

- **Battery health prediction is critical** for reliability, safety, warranty planning, and preventive maintenance.
- **Traditional threshold-based monitoring** (voltage alarms, temperature alarms, simple cycle count) is reactive and often too late.
- **AI models** can learn nonlinear relationships between sensor behavior and degradation.
- **Explainability (SHAP)** is required to make predictions auditable for engineering decisions.
- **IoT integration** is required to move from offline analysis to real-time, deployable intelligence.

BatteryMind combines these dimensions into one flow:

**Sense → Analyze → Explain → Recommend → Visualize**

---

# 3. Complete System Architecture

BatteryMind has two connected tracks:

1. **AI Research Pipeline** (dataset, feature design, model selection, evaluation).
2. **Real-Time IoT Deployment Pipeline** (sensor stream, inference API, dashboard).

## Layered architecture

```text
Data Collection Layer
    ↓
Data Processing Layer
    ↓
Feature Engineering Layer
    ↓
Machine Learning Layer
    ↓
Explainable AI Layer
    ↓
Recommendation Engine
    ↓
IoT Deployment Layer
    ↓
Dashboard Layer
```

## Current implementation architecture in this repository

```text
[Simulator or Arduino Serial Stream]
            ↓
 communication/serial_receiver.py (Arduino path only)
            ↓
      backend/app.py  (/battery-data)
            ↓
 backend/feature_engine.py  (windowed feature extraction)
            ↓
 backend/model_predictor.py (XGBoost inference)
            ↓
 backend/shap_engine.py     (TreeExplainer attributions)
            ↓
 backend/recommendation.py  (rule-based guidance)
            ↓
      backend/app.py  (/battery-status)
            ↓
 dashboard/batterymind-dashboard/src/api/client.js
            ↓
 dashboard React UI components
```

---

# 4. Complete Workflow Explanation

## Stage 1: NASA Battery Dataset Acquisition

BatteryMind’s research context is aligned to battery lifecycle modeling practices built around cycle-level charge/discharge behavior. In this repository, the raw NASA dataset files are **not included**, but the design intent and feature naming clearly reflect discharge-cycle style analytics (time, energy, voltage/current/temperature statistics).

Typical battery datasets in this class contain:

- Battery cell identifiers
- Cycle index progression
- Charge/discharge phases
- Voltage, current, temperature traces
- Capacity and degradation progression information

## Stage 2: Data Processing

The runtime code processes live telemetry as fixed-size sliding windows:

- Input stream fields: `voltage`, `current`, `temperature`
- Readings are appended to rolling buffers with timestamps
- Feature extraction runs after the window is full (`window_size`, currently 300 in `app.py`)

This mirrors discharge-cycle feature aggregation in deployment form.

## Stage 3: SOH Calculation

The standard battery SOH definition is:

\[
\text{SOH} = \frac{\text{Current Capacity}}{\text{Rated Capacity}}
\]

In this repository, runtime inference is performed by a trained XGBoost regressor that outputs normalized SOH (`0.0`–`1.0`), plus percentage representation. The frontend converts to display percentage.

## Stage 4: Feature Engineering

`backend/feature_engine.py` computes 28 engineered features from buffered telemetry.

### Voltage Features

- `Voltage_mean`
- `Voltage_max`
- `Voltage_min`
- `Voltage_std`
- `Voltage_median`
- `Voltage_rms`
- `Voltage_range`

**Physical relevance:** captures operating point, ripple, sag profile, and dispersion characteristics linked to internal resistance and discharge behavior.

### Current Features

- `Current_mean`
- `Current_max`
- `Current_min`
- `Current_std`
- `Current_median`
- `Current_rms`
- `Current_range`

**Physical relevance:** reflects load demand, stress amplitude, and variability that accelerate electrochemical wear.

### Temperature Features

- `Temperature_mean`
- `Temperature_max`
- `Temperature_min`
- `Temperature_std`
- `Temperature_median`
- `Temperature_rms`
- `Temperature_range`

**Physical relevance:** thermal stress is strongly correlated with degradation rate and safety risk.

### Time Features

- `Time_duration`
- `Time_samples`

**Physical relevance:** captures cycle segment span and observation density.

### Energy and Power Features

- `Energy` (computed as \(\int V \cdot |I| \, dt\) using trapezoidal integration)
- `Average_Power`

**Physical relevance:** integrates electrical work throughput, a direct fatigue proxy.

### Degradation Behavior Features

- `Voltage_Drop_Rate`
- `Temperature_Rise`
- `Current_Stability`

**Physical relevance:** explicitly encodes trend and stress dynamics associated with aging progression.

---

# 5. Machine Learning Models

## Random Forest

In the current repository snapshot, there is **no active Random Forest inference module** used by `app.py`.  
However, `feature_engine.py` docstrings still reference “Random Forest model,” indicating historical baseline usage during experimentation.

## XGBoost (Deployed Model)

XGBoost is the active production model in runtime inference:

- Model loading/inference: `backend/model_predictor.py`
- Artifact files: `backend/models/xgboost_model.json`, `backend/models/feature_columns.pkl`
- Backend integration: `backend/app.py`

### Why XGBoost is selected

- Strong performance on tabular engineered features
- Captures nonlinear interactions
- Stable inference latency for online APIs
- Works well with SHAP TreeExplainer

### Reported performance (project benchmark values)

- **MAE:** `0.006296`
- **RMSE:** `0.014926`
- **R²:** `0.995167`

These values identify XGBoost as the deployed choice for this architecture.

## CNN-LSTM

No active CNN-LSTM training or inference scripts are present in this repository snapshot.  
Conceptually, CNN-LSTM is suitable for direct sequence modeling (CNN for local temporal patterns, LSTM for long-term dependencies), but the current deployment path here is engineered-feature + tree-model based.

---

# 6. Model Evaluation

Model quality should be interpreted through:

- **MAE (Mean Absolute Error):** average absolute prediction deviation; lower is better.
- **RMSE (Root Mean Squared Error):** penalizes larger errors more than MAE; lower is better.
- **R² Score:** variance explained by the model; closer to 1 is better.
- **Training Time:** model build cost (offline concern).
- **Inference Time:** per-request latency (deployment concern).

This repository executes inference using pre-saved artifacts and does not run full training/evaluation loops at API runtime.

---

# 7. Explainable AI Implementation

BatteryMind uses SHAP through `backend/shap_engine.py`.

## Why SHAP

- Converts black-box predictions into interpretable feature contributions.
- Supports both global and per-instance explanation.
- Enables engineering decisions beyond raw SOH percentages.

## Implementation details

- `xgboost.XGBRegressor` model is loaded.
- `shap.TreeExplainer` is initialized.
- Input features are aligned to `feature_columns.pkl`.
- Per-request top contributors are returned via `top_features(...)`.

Each top feature contains:

- `feature`
- `impact` (signed contribution value)
- `direction` (`Increase SOH` or `Decrease SOH`)

## Important features observed in this design

From the engineered feature set and explanation pipeline, dominant factors commonly include:

- `Time_samples`
- `Current_rms`
- `Energy`
- Temperature-derived features
- Voltage-derived features

---

# 8. Battery Intelligence Engine

The decision chain is:

**Prediction → Health Classification → Risk Assessment → SHAP Explanation → Recommendation**

## Health categories (`backend/model_predictor.py`)

- **Excellent** (`soh >= 0.95`)
- **Healthy** (`0.85 <= soh < 0.95`)
- **Moderate** (`0.70 <= soh < 0.85`)
- **Degraded** (`0.50 <= soh < 0.70`)
- **Critical** (`soh < 0.50`)

## Risk categories

- **Low**
- **Medium**
- **High**
- **Critical**

## Recommendation generation (`backend/recommendation.py`)

Recommendations are rule-based and combine:

1. Health-state recommendations
2. SHAP feature-based recommendations
3. Risk messaging

The backend returns recommendation text blocks; frontend maps them into display cards.

---

# 9. IoT Deployment Architecture

BatteryMind is structured for hardware deployment with Arduino-class boards.

## Target hardware context

- Arduino UNO
- 18650 rechargeable cell
- Battery holder
- Voltage divider sensor path (to analog input)
- Current sensor (currently code supports ACS712; INA219 can be integrated with adaptation)
- DHT11/DHT22 digital temperature sensor
- Optional analog temperature sensor extension
- Pause button

## Wiring concept (logical)

```text
Battery (+/-)
   ├── Voltage divider output ──> Arduino Analog Pin (A0 in current sketch)
   ├── Current sensor path   ───> Arduino Analog Pin (A1 in current sketch for ACS712)
   └── Temperature sensor    ───> Arduino Digital Pin (D2 for DHT in current sketch)

Pause Button ───────────────────> Arduino Digital Pin (D3, INPUT_PULLUP)
```

The exact resistor values and current sensor sensitivity constants are configured in `arduino/batterymind_sensor.ino`.

---

# 10. How Arduino Integration Will Work

## Current system

```text
Python Sensor Simulator
    ↓
Flask Backend
    ↓
XGBoost + SHAP + Recommendation
    ↓
React Dashboard
```

## Future/Hardware system

```text
Arduino UNO
    ↓
Sensor Data Collection
    ↓
Serial Communication (current bridge design)
    ↓
Flask API (/battery-data)
    ↓
Feature Generator
    ↓
XGBoost Prediction
    ↓
SHAP
    ↓
Recommendation
    ↓
Dashboard Polling (/battery-status)
```

## Backend compatibility

No backend architecture change is required if Arduino sends JSON lines in the expected schema:

```json
{
  "voltage": 3.8,
  "current": 0.5,
  "temperature": 32
}
```

## Files involved for hardware path

- `arduino/batterymind_sensor.ino` (firmware)
- `communication/serial_receiver.py` (serial-to-HTTP bridge)
- `backend/app.py` (ingest and inference)
- `dashboard/batterymind-dashboard/src/api/client.js` (dashboard polling + normalization)

---

# 11. Repository Structure

```text
BatteryMind-IoT/
├── README.md
├── .vscode/
│   └── settings.json
├── arduino/
│   └── batterymind_sensor.ino
├── backend/
│   ├── app.py
│   ├── feature_engine.py
│   ├── model_predictor.py
│   ├── shap_engine.py
│   ├── recommendation.py
│   ├── history_buffer.py
│   ├── sensor_buffer.py
│   ├── test_model.py
│   ├── xgboost_predictor.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── xgboost_model.json
│   │   ├── feature_columns.pkl
│   │   └── feature_scaler.pkl
│   └── __pycache__/              (generated)
├── communication/
│   └── serial_receiver.py
├── simulator/
│   └── sensor_simulator.py
└── dashboard/
    └── batterymind-dashboard/
        ├── .gitignore
        ├── index.html
        ├── package.json
        ├── package-lock.json
        ├── postcss.config.js
        ├── tailwind.config.js
        ├── vite.config.js
        ├── public/               (currently empty)
        ├── src/
        │   ├── main.jsx
        │   ├── index.css
        │   ├── App.jsx
        │   ├── api/client.js
        │   ├── hooks/usePolling.js
        │   └── components/
        │       ├── BackgroundFX.jsx
        │       ├── Header.jsx
        │       ├── SOHGauge.jsx
        │       ├── BatteryVisual.jsx
        │       ├── StatusCards.jsx
        │       ├── LiveCharts.jsx
        │       ├── ShapPanel.jsx
        │       └── RecommendationPanel.jsx
        ├── dist/                 (generated build output)
        └── node_modules/         (installed dependencies)
```

## What each key file does

### Backend

- `app.py`: Flask API entry point; handles ingest, status polling, reset, and orchestrates prediction/explanation/recommendation.
- `feature_engine.py`: windowed sensor buffering + 28-feature extraction.
- `model_predictor.py`: loads XGBoost and predicts SOH, health class, risk class.
- `shap_engine.py`: SHAP TreeExplainer wrapper for top feature contributions.
- `recommendation.py`: converts health/risk/shap into actionable guidance.
- `requirements.txt`: Python dependencies for backend/bridge/simulator runtime.
- `models/*`: serialized model and feature metadata.

### Communication

- `serial_receiver.py`: reads Arduino serial lines, parses JSON, posts to `/battery-data`.

### Simulator

- `sensor_simulator.py`: synthetic real-time telemetry generator for testing without hardware.

### Dashboard

- `src/api/client.js`: polls `/battery-status` and normalizes backend payload to frontend schema.
- `src/hooks/usePolling.js`: periodic fetch loop with local rolling history fallback.
- `src/App.jsx`: page composition and status handling.
- `src/components/*`: visualization and UI widgets.

---

# 12. File Usage Analysis

## Active Files (required in normal end-to-end run)

- `backend/app.py`
- `backend/feature_engine.py`
- `backend/model_predictor.py`
- `backend/shap_engine.py`
- `backend/recommendation.py`
- `backend/models/xgboost_model.json`
- `backend/models/feature_columns.pkl`
- `communication/serial_receiver.py` (Arduino path)
- `simulator/sensor_simulator.py` (simulation path)
- `dashboard/batterymind-dashboard/src/**`
- `dashboard/batterymind-dashboard/package.json` and build config files

## Optional Files

- `backend/test_model.py`: manual SHAP smoke test script.
- `backend/xgboost_predictor.py`: utility script printing feature column metadata.
- `dashboard/batterymind-dashboard/dist/**`: prebuilt frontend assets; can be regenerated via `npm run build`.
- `.vscode/settings.json`: editor convenience only.
- `.venv/**`: local virtual environment (machine-specific).

## Unused / Experimental / Outdated in current runtime flow

These files exist but are not imported by `backend/app.py` or dashboard runtime:

- `backend/history_buffer.py` (legacy buffer abstraction; not wired into API path)
- `backend/sensor_buffer.py` (alternative functional buffer implementation; not wired)
- `backend/models/feature_scaler.pkl` (not loaded by `model_predictor.py` or `shap_engine.py`)

Also, docstrings/comments contain historical references to Random Forest while deployment code uses XGBoost.

> Note: This section documents status only. No files are removed.

---

# 13. How To Run The Project

## Prerequisites

- Python 3.x
- Node.js + npm
- (Optional hardware path) Arduino IDE and board drivers

## Environment setup

### Backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Dashboard dependencies

```bash
cd dashboard/batterymind-dashboard
npm install
```

## Run in simulation mode (recommended for first test)

### Terminal 1: Backend

```bash
cd backend
python app.py
```

### Terminal 2: Simulator

```bash
cd simulator
python sensor_simulator.py
```

### Terminal 3: Dashboard

```bash
cd dashboard/batterymind-dashboard
npm run dev
```

Open: `http://localhost:5173`

## Run in Arduino mode

1. Upload `arduino/batterymind_sensor.ino`.
2. Ensure Serial Monitor is closed.
3. Start backend (`python backend/app.py`).
4. Start bridge:

```bash
cd communication
python serial_receiver.py
```

5. Start dashboard (`npm run dev` in dashboard folder).

## Useful API checks

- `GET http://127.0.0.1:5000/health`
- `GET http://127.0.0.1:5000/buffer`
- `POST http://127.0.0.1:5000/reset`

---

# 14. Future Hardware Setup Guide

## Step 1: Procure components

- Arduino UNO
- 18650 battery + holder
- Voltage divider resistors/module
- Current sensor (ACS712 currently supported; INA219 integration possible with code adaptation)
- DHT11/DHT22
- Push button + wires + breadboard

## Step 2: Build circuit

- Route battery voltage through divider to analog-safe range.
- Put current sensor in series with battery/load path.
- Connect DHT data line to configured digital pin.
- Connect button to configured pin with pull-up logic.
- Common ground across all modules.

## Step 3: Upload firmware

- Open `arduino/batterymind_sensor.ino`
- Install DHT library
- Set sensor constants (`sensitivity`, divider ratios, calibration factor)
- Upload to UNO

## Step 4: Connect communication layer

- Update `SERIAL_PORT` in `communication/serial_receiver.py` (e.g., `COM3`)
- Run bridge script

## Step 5: Replace simulator

- Stop `simulator/sensor_simulator.py`
- Keep backend and dashboard running
- Let serial bridge feed `/battery-data`

## Step 6: Validate live prediction

- Confirm `/buffer` sample growth
- Confirm `/battery-status` returns `status: "success"` once window fills
- Confirm dashboard cards/charts/SHAP/recommendations update

## Step 7: Calibrate sensors

- Tune voltage divider correction (`voltageCalibration`)
- Tune current sensor zero offset and sensitivity
- Validate temperature offset against known reference

---

# 15. Research Contribution

BatteryMind’s contribution is the integration of:

1. **SOH prediction** with engineered battery behavior features.
2. **Explainable AI** through SHAP feature attribution.
3. **Deployment-aware architecture** that supports simulator and Arduino telemetry.
4. **Actionable recommendation generation** beyond static health percentages.

The practical value is not only prediction accuracy, but interpretability and operational guidance in one stack.

---

# 16. Limitations

- Hardware validation is still dependent on full physical bench deployment and calibration quality.
- Real-time readings require sensor-specific calibration to avoid drift/noise-induced bias.
- Current repository snapshot does not include NASA raw dataset artifacts or full training notebooks.
- Random Forest and CNN-LSTM research artifacts are not present as active runtime modules here.
- Broader chemistry generalization (different cell types and operating conditions) requires expanded training data.

---

# 17. Future Improvements

- Edge deployment on ESP8266/ESP32 with lightweight inference services.
- Wireless telemetry transport (Wi-Fi/BLE) beyond USB serial bridge.
- Cloud ingestion + long-horizon trend analytics.
- Digital twin integration for cycle forecasting and what-if analysis.
- Mobile app for field diagnostics.
- Multi-pack/fleet analytics with anomaly ranking and maintenance scheduling.

---

## Implementation Notes (Current Snapshot Accuracy)

- Backend polling endpoint is `/battery-status` and ingest endpoint is `/battery-data`.
- Frontend normalizes backend schema in `src/api/client.js` to maintain compatibility.
- Local chart history is built in `usePolling.js` when backend does not return a `history` array.
- `public/` is currently empty in the dashboard project.
