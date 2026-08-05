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
import json


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

        # Load XGBoost Model via the raw Booster API.
        self.model = xgb.Booster()
        self.model.load_model(MODEL_PATH)

        print("✓ XGBoost Model Loaded")

        # WORKAROUND: this xgboost version does not correctly restore
        # base_score from the saved JSON into the live Booster config
        # (it silently reports 0.5 instead of the trained value). Read
        # the true base_score directly from the JSON file so we can
        # add it back in manually during prediction.
        with open(MODEL_PATH) as f:
            raw_model_json = json.load(f)

        self.correct_base_score = float(
            raw_model_json["learner"]["learner_model_param"]["base_score"]
            .strip("[]")
        )

        print(f"✓ Corrected base_score: {self.correct_base_score}")

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

        dmatrix = xgb.DMatrix(X, feature_names=self.feature_columns)

        # This xgboost version doesn't restore base_score correctly
        # (reports/uses 0.5 instead of the trained 0.8702826), and
        # output_margin=True doesn't reliably strip it either in this
        # version. So: get the normal prediction, remove the wrong
        # base_score, add back the correct one.
        raw_prediction = float(self.model.predict(dmatrix)[0])

        WRONG_BASE_SCORE = 0.5

        soh = raw_prediction - WRONG_BASE_SCORE + self.correct_base_score

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