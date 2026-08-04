"""
=========================================================
BatteryMind Model Predictor
=========================================================

Loads the trained XGBoost model and predicts
Battery State of Health (SOH).

Author: BatteryMind
"""

import os
import joblib
import pandas as pd
import xgboost as xgb


class BatteryPredictor:

    def __init__(self):

        BASE_DIR = os.path.dirname(__file__)

        MODEL_PATH = os.path.join(
            BASE_DIR,
            "models",
            "xgboost_model.json"
        )

        FEATURE_COLUMNS_PATH = os.path.join(
            BASE_DIR,
            "models",
            "feature_columns.pkl"
        )

        print("=" * 60)
        print("Loading BatteryMind XGBoost Model")
        print("=" * 60)

        # Load XGBoost Model
        self.model = xgb.XGBRegressor()
        self.model.load_model(MODEL_PATH)

        print("✓ XGBoost Model Loaded")

        # Load feature order
        self.feature_columns = joblib.load(
            FEATURE_COLUMNS_PATH
        )

        print(f"✓ Loaded {len(self.feature_columns)} Features")

        print("=" * 60)

    ########################################################
    # Prepare Features
    ########################################################

    def prepare_features(self, feature_dict):

        """
        Convert feature dictionary into the exact
        feature order expected by the model.

        NOTE:
        XGBoost was trained on RAW features.
        No scaling is performed.
        """

        df = pd.DataFrame([feature_dict])

        missing = []

        for col in self.feature_columns:

            if col not in df.columns:
                missing.append(col)

        if len(missing) > 0:

            raise ValueError(
                f"Missing Features : {missing}"
            )

        df = df[self.feature_columns]

        return df

    ########################################################
    # Predict SOH
    ########################################################

    def predict(self, feature_dict):

        X = self.prepare_features(feature_dict)

        prediction = self.model.predict(X)

        soh = float(prediction[0])

        soh = max(0.0, min(1.0, soh))

        return soh

    ########################################################
    # Health Classification
    ########################################################

    def classify_health(self, soh):

        if soh >= 0.95:
            return "Excellent"

        elif soh >= 0.85:
            return "Healthy"

        elif soh >= 0.70:
            return "Moderate"

        elif soh >= 0.50:
            return "Degraded"

        return "Critical"

    ########################################################
    # Risk Classification
    ########################################################

    def classify_risk(self, soh):

        if soh >= 0.95:
            return "Low"

        elif soh >= 0.85:
            return "Low"

        elif soh >= 0.70:
            return "Medium"

        elif soh >= 0.50:
            return "High"

        return "Critical"

    ########################################################
    # Predict Everything
    ########################################################

    def predict_all(self, feature_dict):

        soh = self.predict(feature_dict)

        return {

            "soh": round(soh, 4),

            "soh_percentage": round(
                soh * 100,
                2
            ),

            "health": self.classify_health(soh),

            "risk": self.classify_risk(soh)

        }


###########################################################
# Test
###########################################################

if __name__ == "__main__":

    from feature_engine import BatteryFeatureEngine

    engine = BatteryFeatureEngine()

    predictor = BatteryPredictor()

    print()

    print("Generating Dummy Sensor Data...")

    for i in range(100):

        engine.add_reading(

            voltage=4.20 - (i * 0.003),

            current=0.50 + (0.01 * (i % 4)),

            temperature=30 + (i * 0.04)

        )

    features = engine.extract_features()

    result = predictor.predict_all(features)

    print()

    print("=" * 60)
    print(result)
    print("=" * 60)