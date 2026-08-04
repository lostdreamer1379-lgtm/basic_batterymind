"""
=========================================================
BatteryMind SHAP Explainability Engine
=========================================================

Generates feature-level explanations for every
BatteryMind prediction.

Author:
BatteryMind
"""

import os
import joblib
import pandas as pd
import shap
import xgboost as xgb


class BatterySHAP:

    def __init__(self):

        BASE_DIR = os.path.dirname(__file__)

        MODEL_PATH = os.path.join(
            BASE_DIR,
            "models",
            "xgboost_model.json"
        )

        FEATURE_PATH = os.path.join(
            BASE_DIR,
            "models",
            "feature_columns.pkl"
        )

        print("=" * 60)
        print("Loading SHAP Engine")
        print("=" * 60)

        self.model = xgb.XGBRegressor()
        self.model.load_model(MODEL_PATH)

        self.feature_columns = joblib.load(
            FEATURE_PATH
        )

        self.explainer = shap.TreeExplainer(self.model)

        print("✓ SHAP Ready")
        print("=" * 60)

    ######################################################
    # Prepare Features
    ######################################################

    def prepare(self, feature_dict):

        df = pd.DataFrame([feature_dict])

        df = df[self.feature_columns]

        return df

    ######################################################
    # SHAP Values
    ######################################################

    def shap_values(self, feature_dict):

        X = self.prepare(feature_dict)

        values = self.explainer.shap_values(X)

        return values[0]

    ######################################################
    # Feature Importance Dictionary
    ######################################################

    def feature_importance(self, feature_dict):

        X = self.prepare(feature_dict)

        shap_values = self.explainer.shap_values(X)[0]

        importance = {}

        for feature, value in zip(
            self.feature_columns,
            shap_values
        ):

            importance[feature] = float(value)

        return importance

    ######################################################
    # Top N Important Features
    ######################################################

    def top_features(self, feature_dict, top_n=5):

        importance = self.feature_importance(feature_dict)

        ranked = sorted(

            importance.items(),

            key=lambda x: abs(x[1]),

            reverse=True

        )

        output = []

        for feature, value in ranked[:top_n]:

            output.append({

                "feature": feature,

                "impact": round(value, 6),

                "direction": (
                    "Increase SOH"
                    if value > 0
                    else "Decrease SOH"
                )

            })

        return output