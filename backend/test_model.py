from feature_engine import BatteryFeatureEngine
from shap_engine import BatterySHAP

engine = BatteryFeatureEngine()

for i in range(100):

    engine.add_reading(

        voltage=4.2 - i * 0.003,

        current=0.5,

        temperature=30 + i * 0.05

    )

features = engine.extract_features()

shap_engine = BatterySHAP()

print()

print("=" * 60)

print("Top SHAP Features")

print("=" * 60)

for item in shap_engine.top_features(features):

    print(item)