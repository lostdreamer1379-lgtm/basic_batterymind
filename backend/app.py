"""
=========================================================
BatteryMind Backend API
=========================================================

BatteryMind Flask Server

Flow

Sensor Data
      ↓
Feature Engine
      ↓
XGBoost Prediction
      ↓
SHAP Explainability
      ↓
Recommendation Engine
      ↓
JSON Response

Author:
BatteryMind
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from feature_engine import BatteryFeatureEngine
from model_predictor import BatteryPredictor
from shap_engine import BatterySHAP
from recommendation import BatteryRecommendation

#########################################################
# Flask
#########################################################

app = Flask(__name__)
CORS(app)

#########################################################
# BatteryMind Modules
#########################################################

feature_engine = BatteryFeatureEngine(window_size=300)

predictor = BatteryPredictor()

shap_engine = BatterySHAP()

recommendation_engine = BatteryRecommendation()

#########################################################
# Home
#########################################################

@app.route("/")

def home():

    return jsonify({

        "project": "BatteryMind",

        "status": "Running",

        "version": "1.0"

    })

#########################################################
# Health Check
#########################################################

@app.route("/health")

def health():

    return jsonify({

        "status": "OK"

    })

#########################################################
# Live Battery Data
#########################################################

@app.route("/battery-data", methods=["POST"])

def battery_data():

    try:

        data = request.json

        voltage = float(data["voltage"])

        current = float(data["current"])

        temperature = float(data["temperature"])

        #################################################
        # Store Reading
        #################################################

        feature_engine.add_reading(

            voltage,

            current,

            temperature

        )

        #################################################
        # Wait Until Buffer Fills
        #################################################

        if not feature_engine.is_ready():

            return jsonify({

                "status": "Collecting",

                "samples":

                    feature_engine.size(),

                "required":

                    feature_engine.window_size

            })

        #################################################
        # Feature Extraction
        #################################################

        features = feature_engine.extract_features()

        print("\n========== LIVE FEATURES ==========")

        for k, v in features.items():
             print(f"{k:25} : {v}")

        print("===================================\n")

        #################################################
        # Prediction
        #################################################

        prediction = predictor.predict_all(features)

        #################################################
        # SHAP
        #################################################

        shap_features = shap_engine.top_features(

            features,

            top_n=5

        )

        #################################################
        # Recommendation
        #################################################

        report = recommendation_engine.generate(

            soh=prediction["soh"],

            health=prediction["health"],

            risk=prediction["risk"],

            shap_features=shap_features

        )

        #################################################
        # Response
        #################################################

        return jsonify({

            "status": "success",

            "sensor": {

                "voltage": voltage,

                "current": current,

                "temperature": temperature

            },

            "prediction": prediction,

            "shap": shap_features,

            "recommendation": report

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

#########################################################
# Reset Buffer
#########################################################

@app.route("/reset", methods=["POST"])

def reset():

    feature_engine.reset()

    return jsonify({

        "status": "Buffer Reset"

    })

#########################################################
# Buffer Status
#########################################################

@app.route("/buffer")
def buffer():

    return jsonify({

        "samples": feature_engine.size(),

        "required": feature_engine.window_size,

        "ready": feature_engine.is_ready()

    })


#########################################################
# Battery Status (For React Dashboard)
#########################################################

@app.route("/battery-status", methods=["GET"])
def battery_status():

    try:

        # Buffer not full yet
        if not feature_engine.is_ready():

            return jsonify({

                "status": "collecting",

                "samples": feature_engine.size(),

                "required": feature_engine.window_size,

                "ready": False,

                "prediction": None,

                "shap": [],

                "recommendation": None

            })

        #################################################
        # Feature Extraction
        #################################################

        features = feature_engine.extract_features()

        #################################################
        # Prediction
        #################################################

        prediction = predictor.predict_all(features)

        #################################################
        # SHAP
        #################################################

        shap_features = shap_engine.top_features(

            features,

            top_n=5

        )

        #################################################
        # Recommendation
        #################################################

        report = recommendation_engine.generate(

            soh=prediction["soh"],

            health=prediction["health"],

            risk=prediction["risk"],

            shap_features=shap_features

        )

        #################################################
        # Response
        #################################################

        return jsonify({

            "status": "success",

            "ready": True,

            "sensor": {

                "voltage": feature_engine.voltage_buffer[-1],

                "current": feature_engine.current_buffer[-1],

                "temperature": feature_engine.temperature_buffer[-1]

            },

            "prediction": prediction,

            "shap": shap_features,

            "recommendation": report,

            "buffer": {

                "samples": feature_engine.size(),

                "required": feature_engine.window_size

            }

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


#########################################################
# Run
#########################################################

if __name__ == "__main__":

    print("=" * 60)

    print("BatteryMind Backend Started")

    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )